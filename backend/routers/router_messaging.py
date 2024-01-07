
from fastapi import APIRouter, Depends, Request, Body, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated
from sqlmodel import col
from ..cores import core_users as UsersModule
from ..cores import core_groups as GroupsModule
from ..cores import core_messaging as MessagingModule
from ..models import Output_Message, Output_PersonalConversation
from ..requests import Message_CreateRequest, Message_UpdateRequest

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

class RouterRequest_SendMessage(BaseModel):
    conversation_id: int = Field()
    text: str = Field()
    media_ids: list[int] = Field()

class RouterRequest_SelectConversationChannel(BaseModel):
    channel_id: int

class RouterRequest_Delete(BaseModel):
    id: int

@router.post('/getConversationChannel', response_class=JSONResponse)
async def post_get_conversation_channel(query: RouterRequest_SelectConversationChannel, req: Request):
    conversation = MessagingModule.Select.oneConversation(MessagingModule.Conversation.allowed_from1 == query.channel_id, MessagingModule.Conversation.type == "channel")
    if conversation == None:
        raise HTTPException(detail="Couldn't find conversation with specified ID", status_code=404)
    else:
        return conversation

@router.get('/getPersonalChatWithUser/{user_id}', response_class=JSONResponse, response_model=Output_PersonalConversation)
async def get_personal_chat_with_user(user_id: int, req: Request):
    conversation = MessagingModule.Select.oneConversation(MessagingModule.Conversation.allowed_from1 == req.state.current_user.id, MessagingModule.Conversation.allowed_from2 == user_id, MessagingModule.Conversation.type == "personal")
    if conversation == None:
        conversation = MessagingModule.Select.oneConversation(MessagingModule.Conversation.allowed_from1 == user_id, MessagingModule.Conversation.allowed_from2 == req.state.current_user.id, MessagingModule.Conversation.type == "personal")
    if conversation == None:
        # Создать, если не существует
        conversation = MessagingModule.Create.conversation(
            MessagingModule.Conversation_CreateRequest(type="personal", allowed_from1=req.state.current_user.id, allowed_from2=user_id)
        )
    return MessagingModule.Convert.personalConversation(conversation=conversation, requesting_user_id=req.state.current_user.id)


@router.post('/sendMessage', response_class=JSONResponse, response_model=Output_Message)
async def post_send_message(sendRequest: RouterRequest_SendMessage, req: Request):
    debugPrefix = "MESSAGING :: Sending message ::"
    print(f"{debugPrefix} Request:")
    print(sendRequest)
    conversation = MessagingModule.Select.oneConversation(MessagingModule.Conversation.id == sendRequest.conversation_id)
    if conversation == None:
        print(f"{debugPrefix} ERROR :: Couldn't find conversation with specified ID = {sendRequest.conversation_id}")
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
                    Message_CreateRequest(conversation_id=conversation.id, text=sendRequest.text, media_ids=sendRequest.media_ids, sender_id=req.state.current_user.id)
                )
                await websocket_broadcast_update(sendRequest.conversation_id)
                return MessagingModule.Convert.message(message)
            except:
                print(f"{debugPrefix} ERROR :: Couldn't find conversation for specified user")
                raise HTTPException(detail="Couldn't find conversation for specified user", status_code=400)
        else:
            print(f"{debugPrefix} ERROR :: Couldn't find user")
            raise HTTPException(detail="Couldn't find user", status_code=400)
    elif (conversation.type == "channel"):
        channel = GroupsModule.Select.oneChannel(GroupsModule.Channel.id == conversation.allowed_from1)
        if channel != None:
            message = MessagingModule.Create.message(
                Message_CreateRequest(conversation_id=conversation.id, text=sendRequest.text, media_ids=sendRequest.media_ids, sender_id=req.state.current_user.id)
            )
            print(f"{debugPrefix} Sending broadcast websocket message.")
            await websocket_broadcast_update(sendRequest.conversation_id)
            return MessagingModule.Convert.message(message)
        else:
            print(f"{debugPrefix} ERROR :: Couldn't find channel")
            raise HTTPException(detail="Couldn't find channel", status_code=400)
    else:
        print(f"{debugPrefix} ERROR :: Invalid request")
        raise HTTPException(detail="Invalid request", status_code=400)

@router.get('/getMessages/{chat_id}', response_class=JSONResponse, response_model=list[Output_Message])
async def get_messages(chat_id: int, time_start: int = 0, time_end: int = 10 ** 16, containing_string: str = ""):
    if (chat_id):
        return MessagingModule.Select.messages(
            MessagingModule.Message.conversation_id == chat_id,
            MessagingModule.Message.time <= time_end,
            MessagingModule.Message.time >= time_start,
            col(MessagingModule.Message.text).contains(containing_string)
        )
    raise HTTPException(detail="Couldn't find conversation with specified ID", status_code=404)

@router.get('/getLastMessage/{chat_id}', response_class=JSONResponse, response_model=Output_Message)
async def get_last_message(chat_id: int):
    if (chat_id):
        resultList = MessagingModule.Select.messages_extended(expressions=[MessagingModule.Message.conversation_id == chat_id], offset=0, limit=1, order_by=MessagingModule.Message.id.desc())
        #resultList.sort(lambda x => x.id)
        if len(resultList) == 0:
            raise HTTPException(status_code=404)
        return resultList[-1]

    raise HTTPException(detail="Couldn't find conversation with specified ID", status_code=404)

@router.get('/listConversations', response_class=JSONResponse)
async def get_list_conversations():
    return MessagingModule.List.conversations()

@router.get('/getMyPersonalChats', response_class=JSONResponse)
async def get_list_conversations(req: Request):
    return MessagingModule.Select.personalConversations(requesting_user_id=req.state.current_user.id)

@router.post('/editMessage', response_class=JSONResponse, response_model=Output_Message)
async def post_edit_message(request: Message_UpdateRequest, req: Request):
    targetMessage = MessagingModule.RawSelect.oneMessage(MessagingModule.Message.id == request.id)
    if (targetMessage.sender_id != req.state.current_user.id):
        raise HTTPException(status_code=403)
    raw_result = MessagingModule.Update.message(request)
    result = MessagingModule.Convert.message(raw_result)
    await websocket_broadcast_update(raw_result.conversation_id)
    return result

@router.post('/deleteMessage', response_class=JSONResponse, response_model=Output_Message)
async def post_delete_message(request: RouterRequest_Delete, req: Request):
    try:
        result = MessagingModule.Delete.message(request.id)
    except:
        raise HTTPException(status_code=403)
    
    await websocket_broadcast_update(result.conversation_id)
    return MessagingModule.Convert.message(result)

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
            break

async def websocket_broadcast_update(chat_id: int):
    print("SENDING UPDATE MESSAGE TO", chat_id)
    result = ws_manager.getConnectionWithChatId(chat_id)
    for i in result:
        await ws_manager.send_personal_message("update", i)