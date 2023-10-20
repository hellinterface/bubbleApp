from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Cookie
from fastapi.responses import HTMLResponse, Response, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
import json
import sqlite3
import secrets
from typing import Annotated
from pydantic import BaseModel

from .routers import internal_router
from .bbmodules import userapi

app = FastAPI()

app = FastAPI()
app.mount("/static", StaticFiles(directory="app_external/static"), name="static")
app.include_router(internal_router.router)

templates = Jinja2Templates(directory="app_external/templates")

@app.get('/app')
@app.get("/app/{path}", response_class=HTMLResponse)
async def catch_all(request: Request, path: str = ""):
    access_token_cookie = request.cookies.get('access_token')
    if (access_token_cookie == None or userapi.get_current_user(access_token_cookie) == None):
        return RedirectResponse("/login")
    return templates.TemplateResponse("app.html", {"request": request})
        

#################################

"""
class IDCreator():
    def __init__(self):
        pass
    @staticmethod
    def forUser():
        return secrets.token_urlsafe(6)
"""

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

@app.get("/login", response_class=HTMLResponse)
async def login_get(access_token: Annotated[str | None, Cookie()] = None):
    if (access_token != None and userapi.get_current_user(access_token) != None):
        return RedirectResponse("/app")
    f = open("app_external/login.html", "r", encoding="utf-8")
    return f.read()

@app.get("/signup", response_class=HTMLResponse)
async def signup_get():
    f = open("app_external/signup.html", "r", encoding="utf-8")
    return f.read()

