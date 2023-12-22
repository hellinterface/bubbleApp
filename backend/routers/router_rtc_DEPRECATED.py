
from fastapi import APIRouter, Depends, Request, status, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.exceptions import HTTPException
from datetime import timedelta
from ..modules import mod_users as MainModule
from pydantic import BaseModel
import datetime
import json

async def get_token_header(req: Request):
    token = req.headers.get("X-Access-Token")
    print(token)
    if token == None:
        return False
    try:
        user = MainModule.get_user_from_token(token)
        print(user)
        req.state.current_user = user
        return user
    except:
        print("GET TOKEN HEADER ERROR ###")

router = APIRouter(
    prefix="/api/rtc",
    tags=["users"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

class Connection:
    def __init__(self):
        self.socket = 0
        self.user_id = 0
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

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    newconn = await manager.connect(websocket)
    ws_userlist.append(newconn.user_id)
    await manager.broadcast(JSONWS("userlist_update", json.dumps(ws_userlist).replace('"', '\\"')))
    while True:
        try:
            data = await websocket.receive_text()
            conn = manager.getConnectionWithSocket(websocket)
            # await manager.send_personal_message(JSONWS("message", f"You wrote something."), conn)
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
                print(obj[1])
                targetPeer = manager.getConnectionWithUsername(obj[1]['targetPeer'])
                if targetPeer != -1:
                    obj[1]['targetPeer'] = conn.user_id
                    await targetPeer.socket.send_text(json.dumps(obj))
            if obj[0] == "chat_message":
                await manager.broadcast(obj[1])
        except WebSocketDisconnect:
            conn = manager.getConnectionWithSocket(websocket)
            ws_userlist.remove(conn.user_id)
            manager.disconnect(conn)
            await manager.broadcast(JSONWS("userlist_update", json.dumps(ws_userlist).replace('"', '\\"')))