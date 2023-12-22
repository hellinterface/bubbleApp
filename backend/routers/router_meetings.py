
from fastapi import APIRouter, Depends, Request, status, Response, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.exceptions import HTTPException
from datetime import timedelta
from ..modules import mod_users as MainModule
from pydantic import BaseModel
import datetime
import json
from ..modules import mod_users as UsersModule
import secrets

router = APIRouter(
    prefix="/api/meetings",
    tags=["meetings"],
    # dependencies=[Depends(UsersModule.get_token_header)],
    responses={404: {"description": "Not found"}},
)

class Connection:
    def __init__(self):
        self.socket = None
        self.user = None
        self.socket_id = 0

class MeetingRoom:
    def __init__(self, id):
        self.active_connections: list[Connection] = []
        self.room_id = id
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
    def getConnectionWithUserId(self, user_id):
        for i in self.active_connections:
            if i.user.id == user_id:
                return i
        return -1
    async def connect(self, websocket: WebSocket, user: UsersModule.User):
        await websocket.accept()
        newConnection = Connection()
        newConnection.socket = websocket
        newConnection.socket_id = self.getMaxSocketID()+1
        newConnection.user = user
        self.active_connections.append(newConnection)
        print("New connection!")
        print(newConnection.user)
        print(*self.active_connections)
        return newConnection
    def disconnect(self, conn: Connection):
        print("DISCONNECTING ---")
        print()
        self.active_connections.remove(conn)
        print(*self.active_connections)
    async def send_personal_message(self, message: str, connection: Connection):
        print(*self.active_connections)
        await connection.socket.send_text(message)
    async def broadcast(self, message: str):
        print(*self.active_connections)
        for conn in self.active_connections:
            await conn.socket.send_text(message)

class MeetingRoomManager:
    def __init__(self):
        self.rooms = []
        return
    def createNewRoom(self, channel_id):
        room = MeetingRoom(channel_id)
        self.rooms.append(room)
    def getRoomById(self, room_id):
        for i in self.active_connections:
            if i.user.id == room_id:
                return i
        return -1


roomManager = MeetingRoomManager()

def JSONWS(msgtype: str, body: str):
    return f"[\"{msgtype}\", \"{body}\"]"

ws_userlist = list()

@router.get("/list_rooms")
async def get_list_rooms():
    resultList = []
    for i in roomManager.rooms:
        resultList.append({"id": i.room_id, "connections": len(i.active_connections)})
    return resultList

class RouterRequest_GetRoomById(BaseModel):
    id: int

class RouterRequest_CreateRoom(BaseModel):
    id: int

class Room(BaseModel):
    id: int
    userlist: list[int]

@router.get("/get_room_by_id/{room_id}")
async def get_room_by_id(room_id: int):
    room = None
    for i in roomManager.rooms:
        if (i.id == room_id):
            room = i
            userlist = []
            for k in i.active_connections:
                userlist.append(k.user.id)
            return Room(id=i.id, userlist=userlist)
    raise HTTPException(status_code=404, detail="Not found")

@router.post("/create_room")
async def get_room_by_id(request: RouterRequest_CreateRoom):
    room = None
    for i in roomManager.rooms:
        if (i.id == request.id):
            raise HTTPException(status_code=400, detail="Room with specified ID already active")
    room = roomManager.createNewRoom(request.id)
    userlist = []
    for k in i.active_connections:
        userlist.append(k.user.id)
    return Room(id=i.id, userlist=userlist)
    

@router.websocket("/ws/{channel_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, channel_id: int, user_id: int):
    user = UsersModule.Select.oneUser(UsersModule.User.id == user_id)
    room = roomManager.getRoomById(channel_id)
    if (user == None):
        return
    if (room == None):
        room = roomManager.createNewRoom(channel_id)
    newconn = await room.connect(websocket, user)
    ws_userlist.append(user_id)
    await room.broadcast(JSONWS("userlist_update", json.dumps(ws_userlist).replace('"', '\\"')))
    while True:
        try:
            data = await websocket.receive_text()
            conn = newconn
            #conn = manager.getConnectionWithSocket(websocket)
            # await manager.send_personal_message(JSONWS("message", f"You wrote something."), conn)
            obj = json.loads(data)
            if obj[0] == "RTC_Offer":
                print(obj[1])
                targetPeer = room.getConnectionWithUserId(obj[1]['targetPeer'])
                if targetPeer != -1:
                    obj[1]['targetPeer'] = conn.user.id
                    await targetPeer.socket.send_text(json.dumps(obj))
                else:
                    await targetPeer.socket.send_text(json.dumps({"failure": "ohno"}))
            if obj[0] == "RTC_Answer":
                targetPeer = room.getConnectionWithUserId(obj[1]['targetPeer'])
                if targetPeer != -1:
                    obj[1]['targetPeer'] = conn.user.id
                    await targetPeer.socket.send_text(json.dumps(obj))
            if obj[0] == "RTC_Candidate":
                print("CANDIDATE")
                print(obj[1])
                targetPeer = room.getConnectionWithUserId(obj[1]['targetPeer'])
                if targetPeer != -1:
                    obj[1]['targetPeer'] = conn.user.id
                    await targetPeer.socket.send_text(json.dumps(obj))
            if obj[0] == "chat_message":
                await room.broadcast(obj[1])
        except WebSocketDisconnect:
            #conn = manager.getConnectionWithSocket(websocket)
            conn = newconn
            ws_userlist.remove(conn.user.id)
            room.disconnect(conn)
            await room.broadcast(JSONWS("RTC_PEER_DISCONNECT", conn.user.id))
            await room.broadcast(JSONWS("userlist_update", json.dumps(ws_userlist).replace('"', '\\"')))
            if len(room.active_connections) == 0:
                roomManager.removeById(room.room_id)