
from fastapi import APIRouter, Depends, Request, Body, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated
from ..modules import mod_users as UsersModule
from ..modules import mod_groups as GroupsModule
from ..modules import mod_messaging as MessagingModule

router = APIRouter(
    prefix="/api/messaging",
    tags=["Messaging"],
    dependencies=[Depends(UsersModule.get_token_header)],
    responses={404: {"description": "Not found"}},
)
router_ws = APIRouter(
    prefix="/api/messaging",
    tags=["Messaging"],
    # dependencies=[Depends(UsersModule.get_token_header)],
    responses={404: {"description": "Not found"}},
)
"""
Не стоит давать доступ пользователю, лишь админу.

@router.post('/create_conversation', response_class=JSONResponse)
async def post_create_conversation():
    return {"some": "stuff"}
"""

class SendMessageRequest(BaseModel):
    conversation_id: int = Field()
    text: str = Field()
    media_ids: list[int] = Field()

class Query_ConversationChannel(BaseModel):
    channel_id: int

class Query_Message(BaseModel):
    id: int|None
    conversation_id: int|None
    user_id: str|None
    time: int|None

@router.post('/get_conversation_channel', response_class=JSONResponse)
async def post_get_conversation_channel(query: Query_ConversationChannel, req: Request):
    conversation = MessagingModule.Select.oneConversation(MessagingModule.Conversation.allowed_from1 == query.channel_id, MessagingModule.Conversation.type == "channel")
    if conversation == None:
        raise HTTPException(detail="Couldn't find conversation with specified ID", status_code=400)
    else:
        return conversation


@router.post('/send_message', response_class=JSONResponse)
async def post_send_message(sendRequest: SendMessageRequest, req: Request):
    conversation = MessagingModule.Select.oneConversation(MessagingModule.Conversation.id == sendRequest.conversation_id)
    if conversation == None:
        raise HTTPException(detail="Couldn't find conversation with specified ID", status_code=400)
    if (conversation.type == "personal"):
        user_to = conversation.allowed_from1
        if (user_to == req.state.current_user.id):
            user_to = conversation.allowed_from2
        user_to_object = UsersModule.Select.oneUser(UsersModule.User.id == user_to)
        if user_to_object != None:
            try:
                print("SENDING!!!")
                message = MessagingModule.Create.message(
                    MessagingModule.Message_createRequest(conversation_id=conversation.id, text=sendRequest.text, media_ids=sendRequest.media_ids, sender_id=req.state.current_user.id)
                )
                await websocket_broadcast_update(sendRequest.conversation_id)
                return message
            except:
                raise HTTPException(detail="Couldn't find conversation for specified user", status_code=400)
        else:
            raise HTTPException(detail="Couldn't find user", status_code=400)
    elif (conversation.type == "channel"):
        channel = GroupsModule.Select.oneChannel(GroupsModule.Channel.id == conversation.allowed_from1)
        if channel != None:
            permissions = GroupsModule.get_channel_permissions_of_user(user_id=req.state.current_user.id, channel_id=conversation.allowed_from1)
            if (not permissions.get('send_messages')):
                raise HTTPException(detail="No permission for sending messages in specified channel", status_code=403)
            print("SENDING!!!")
            message = MessagingModule.Create.message(
                MessagingModule.Message_createRequest(conversation_id=conversation.id, text=sendRequest.text, media_ids=sendRequest.media_ids, sender_id=req.state.current_user.id)
            )
            await websocket_broadcast_update(sendRequest.conversation_id)
            return message
            try:
                pass
            except:
                raise HTTPException(detail="Couldn't find conversation for specified channel", status_code=400)
        else:
            raise HTTPException(detail="Couldn't find channel", status_code=400)
    else:
        raise HTTPException(detail="Invalid request", status_code=400)

@router.post('/get_messages', response_class=JSONResponse)
async def post_get_messages(query: Query_Message):
    if (query.conversation_id):
        return MessagingModule.Select.messages(MessagingModule.Message.conversation_id == query.conversation_id)
    return []

    
@router.get('/list_conversations', response_class=JSONResponse)
async def get_list_conversations():
    return MessagingModule.List.conversations()


class Connection:
    def __init__(self):
        self.socket = 0
        self.chat_id = 0
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
    def getConnectionWithChatId(self, chat_id: int):
        result = []
        for i in self.active_connections:
            if i.chat_id == chat_id:
                result.append(i)
        return result
    async def connect(self, websocket: WebSocket, chat_id: int):
        await websocket.accept()
        newConnection = Connection()
        newConnection.socket = websocket
        newConnection.socket_id = self.getMaxSocketID()+1
        newConnection.chat_id = chat_id
        print(newConnection.chat_id)
        self.active_connections.append(newConnection)
        print("New connection!")
        print(*self.active_connections)
        return newConnection
    def disconnect(self, conn: Connection):
        self.active_connections.remove(conn)
        print(*self.active_connections)
    async def send_personal_message(self, message: str, connection: Connection):
        print(*self.active_connections)
        print("SENDING PERSONAL")
        await connection.socket.send_text(message)
    async def broadcast(self, message: str):
        print(*self.active_connections)
        for conn in self.active_connections:
            await conn.socket.send_text(message)

ws_manager = ConnectionManager()

@router_ws.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    newconn = await ws_manager.connect(websocket, chat_id)
    while True:
        try:
            data = await websocket.receive_text()
            conn = ws_manager.getConnectionWithSocket(websocket)
        except WebSocketDisconnect:
            conn = ws_manager.getConnectionWithSocket(websocket)
            ws_manager.disconnect(conn)

async def websocket_broadcast_update(chat_id: int):
    print("SENDING UPDATE MESSAGE TO", chat_id)
    result = ws_manager.getConnectionWithChatId(chat_id)
    for i in result:
        await ws_manager.send_personal_message("update", i)