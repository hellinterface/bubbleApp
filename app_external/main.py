from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Cookie
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from datetime import datetime, timedelta
import json
import sqlite3
import secrets
from typing import Annotated
from pydantic import BaseModel
import httpx

app = FastAPI()
app.mount("/static", StaticFiles(directory="app_external/static"), name="static")

templates = Jinja2Templates(directory="app_external/templates")

@app.get('/app')
@app.get("/app/{path}", response_class=HTMLResponse)
async def catch_all(request: Request, path: str = ""):
    print("full_path: "+path)
    return templates.TemplateResponse("app.html", {"request": request})

@app.get("/users/list")
async def list_users():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get('http://127.0.0.1:8080/api/users/list')
            return r.read()
        except:
            return "Error..."

#################################


class IDCreator():
    def __init__(self):
        pass
    @staticmethod
    def forUser():
        return secrets.token_urlsafe(6)

# подключение к базе данных
def getDBConnection():
    conn = sqlite3.connect('main.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/rtc", response_class=HTMLResponse)
async def read_root():
    f = open("app_external/index.html", "r", encoding="utf-8")
    return f.read()

class Connection:
    def __init__(self):
        self.socket = 0
        self.user_id = secrets.token_urlsafe(6)
        self.socket_id = 0

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[Connection] = []
    def getMaxSocketID(self):
        maxid = 0
        for i in self.active_connections:
            if int(i.socket_id) > maxid:
                maxid = int(i.socket_id)
        return maxid
    def getConnectionWithSocket(self, websocket):
        for i in self.active_connections:
            if i.socket == websocket:
                return i
        return -1
    def getConnectionWithUsername(self, name):
        for i in self.active_connections:
            if i.user_id == name:
                return i
        return -1
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        newConnection = Connection()
        newConnection.socket = websocket
        newConnection.socket_id = manager.getMaxSocketID()+1
        #newConnection.user_id = f"USER_{str(newConnection.socket_id)}"
        print(newConnection.user_id)
        self.active_connections.append(newConnection)
        print("New connection!")
        print(*self.active_connections)
        return newConnection
    def disconnect(self, conn: Connection):
        self.active_connections.remove(conn)
        print(*self.active_connections)
    async def send_personal_message(self, message: str, connection: Connection):
        print(*self.active_connections)
        await connection.socket.send_text(message)
    async def broadcast(self, message: str):
        print(*self.active_connections)
        for conn in self.active_connections:
            await conn.socket.send_text(message)

manager = ConnectionManager()

def JSONWS(msgtype: str, body: str):
    return f"[\"{msgtype}\", \"{body}\"]"

ws_userlist = list()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    newconn = await manager.connect(websocket)
    ws_userlist.append(newconn.user_id)
    await manager.broadcast(JSONWS("userlist_update", json.dumps(ws_userlist).replace('"', '\\"')))
    while True:
        try:
            data = await websocket.receive_text()
            conn = manager.getConnectionWithSocket(websocket)
            # await manager.send_personal_message(JSONWS("message", f"You wrote {data}"), conn)
            # await manager.broadcast(JSONWS("message", f"Client #{conn.user_id} says: {data}"))
            await manager.send_personal_message(JSONWS("message", f"You wrote something."), conn)
            obj = json.loads(data)
            if obj[0] == "RTC_Offer":
                print(obj[1])
                targetPeer = manager.getConnectionWithUsername(obj[1]['targetPeer'])
                if targetPeer != -1:
                    obj[1]['targetPeer'] = conn.user_id
                    await targetPeer.socket.send_text(json.dumps(obj))
                else:
                    await targetPeer.socket.send_text(json.dumps({"failure": "ohno"}))
            if obj[0] == "RTC_Answer":
                targetPeer = manager.getConnectionWithUsername(obj[1]['targetPeer'])
                if targetPeer != -1:
                    obj[1]['targetPeer'] = conn.user_id
                    await targetPeer.socket.send_text(json.dumps(obj))
            if obj[0] == "RTC_Candidate":
                print("CANDIDATE")
                print("CANDIDATE")
                print(obj[1])
                print("CANDIDATE")
                print("CANDIDATE")
                targetPeer = manager.getConnectionWithUsername(obj[1]['targetPeer'])
                if targetPeer != -1:
                    await targetPeer.socket.send_text(data)
            if obj[0] == "chat_message":
                await manager.broadcast(obj[1])
        except WebSocketDisconnect:
            conn = manager.getConnectionWithSocket(websocket)
            ws_userlist.remove(conn.user_id)
            manager.disconnect(conn)
            await manager.broadcast(JSONWS("userlist_update", json.dumps(ws_userlist).replace('"', '\\"')))

# LOGIN LOGIC

SECRET_KEY = "aa171942c2c26d0f39775b861f187a81f43865c0bf917ff58c1acca419d95b5f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 3

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str | None = None
    
class User(BaseModel):
    username: str
    email: str | None = None
    visiblename: str | None = None

class UserInDB(User):
    password_hash: str

class LogInRequest(BaseModel):
    email: str
    password_hash: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(user_id: str):
    async with httpx.AsyncClient() as client:
        try:
            objectToSend = {"id": user_id }
            r = await client.post('http://127.0.0.1:8080/api/users/getByID', json=objectToSend)
            backendOutput = r.json()
            if (backendOutput["response"] == "success"):
                return backendOutput["data"]
            else:   
                raise HTTPException(status_code=400, detail="Incorrect username or password")
        except:
            raise HTTPException(status_code=402, detail="Something went wrong...")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if (token == None):
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        print("USER ID: " + user_id)
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    user = await get_user(user_id=token_data.user_id)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(user)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if user is None:
        raise credentials_exception
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    print("77777777777777777777777777777777 CREATING TOKEN")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(email: str, passwordHash: str):
    async with httpx.AsyncClient() as client:
        try:
            objectToSend = {"email": email, "password_hash": passwordHash}
            r = await client.post('http://127.0.0.1:8080/api/users/try_login', json=objectToSend)
            backendOutput = r.json()
            if (backendOutput["response"] == "success"):
                return backendOutput["user_id"]
            else:   
                raise HTTPException(status_code=400, detail="Incorrect username or password")
        except:
            return HTTPException(status_code=402, detail="Something went wrong...")
    
@app.post("/token", response_model=Token)
async def login_for_access_token(request: Request, response: Response):
    request = await request.json()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(request)
    user_id = await authenticate_user(request["email"], request["password_hash"])
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$ AUTHED")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"user_id": user_id}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=access_token)
    return {"access_token": access_token, "token_type": "bearer"}

#, current_user: Annotated[User, Depends(get_current_user)]
@app.get("/testauth")
async def read_own_items(access_token: Annotated[str | None, Cookie()] = None):
    print(access_token)
    data = await get_current_user(access_token)
    print(access_token)
    print(data)
    #return [{"item_id": "Foo", "owner": }]
    return data

@app.get("/login", response_class=HTMLResponse)
async def login_get():
    f = open("app_external/login.html", "r", encoding="utf-8")
    return f.read()

@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request):
    requestBody = await request.json()
    print(requestBody)
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post('http://127.0.0.1:8080/api/users/try_login', json=requestBody)
            return r.read()
        except:
            return "Error..."

@app.get("/signup", response_class=HTMLResponse)
async def signup_get():
    f = open("app_external/signup.html", "r", encoding="utf-8")
    return f.read()

    
@app.post("/signup", response_class=HTMLResponse)
async def signup_post(request: Request):
    requestBody = await request.json()
    print(requestBody)
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post('http://127.0.0.1:8080/api/users/try_signup', json=requestBody)
            backendOutput = r.json()
            if (backendOutput["response"] == "success"):
                return {"access_token": user.username, "token_type": "bearer"}
            else:   
                raise HTTPException(status_code=400, detail="Incorrect username or password")
            return 
        except:
            return "Error..."
