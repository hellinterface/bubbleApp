
from fastapi import APIRouter, Depends, Request, Body, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime, timedelta, date
from time import mktime
from ..modules import mod_users as UsersModule
from ..modules import mod_groups as GroupsModule
from ..modules import mod_messaging as MessagingModule

router = APIRouter(
    prefix="/api/messaging",
    tags=["Messaging"],
    dependencies=[Depends(UsersModule.get_token_header)],
    responses={404: {"description": "Not found"}},
)
"""
Не стоит давать доступ пользователю, лишь админу.

@router.post('/create_conversation', response_class=JSONResponse)
async def post_create_conversation():
    return {"some": "stuff"}
"""

class SendMessageRequest_Channel(BaseModel):
    channel_id: str = Field()
    text: str = Field()
    media_ids: list[int] = Field()

class SendMessageRequest_Personal(BaseModel):
    user_id: str = Field()
    text: str = Field()
    media_ids: list[int] = Field()

class SendMessageRequest(BaseModel):
    conversation_id: int = Field()
    conversation_type: str = Field()
    #recipient_id: str = Field()
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
    result_list = MessagingModule.select_conversations(MessagingModule.Conversation.allowed_from1 == query.channel_id)
    if len(result_list) > 0:
        return result_list[0]
    else:
        raise Exception()

def get_current_time():
    creation_time = datetime.now()
    creation_time = mktime(creation_time.timetuple())
    return creation_time

@router.post('/send_message', response_class=JSONResponse)
async def post_send_message(sendRequest: SendMessageRequest, req: Request):
    conversation = MessagingModule.select_conversations(MessagingModule.Conversation.id == sendRequest.conversation_id)
    if len(conversation) <= 0:
        return JSONResponse(content={"description": "Couldn't find conversation with specified ID"}, status_code=400)
    conversation = conversation[0]
    if (sendRequest.conversation_type == "personal"):
        user_to = conversation.allowed_from1
        if (user_to == req.state.current_user.id):
            user_to = conversation.allowed_from2
        user_list = UsersModule.select_users(UsersModule.User.id == user_to)
        if len(user_list) > 0:
            try:
                creation_time = get_current_time()
                MessagingModule.create_message_personal(user_from=req.state.current_user.id, user_to=user_to, text=sendRequest.text, media_ids=sendRequest.media_ids, time=creation_time)
            except:
                return JSONResponse(detail="Couldn't find conversation for specified user", status_code=400)
        else:
            return HTTPException(detail="Couldn't find user", status_code=400)
    elif (sendRequest.conversation_type == "channel"):
        channel_list = GroupsModule.select_channels(GroupsModule.Channel.id == conversation.allowed_from1)
        if len(channel_list) > 0:
            permissions = GroupsModule.get_channel_permissions_of_user(user_id=req.state.current_user.id, channel_id=conversation.allowed_from1)
            if (not permissions.get('send_messages')):
                return HTTPException(detail="No permission for sending messages in specified channel", status_code=403)
            try:
                print("SENDING!!!")
                creation_time = get_current_time()
                message = MessagingModule.create_message_channel(user_from=req.state.current_user.id, channel_id=conversation.allowed_from1, text=sendRequest.text, media_ids=sendRequest.media_ids, time=creation_time)
                return message
            except:
                return HTTPException(detail="Couldn't find conversation for specified channel", status_code=400)
        else:
            return HTTPException(detail="Couldn't find channel", status_code=400)
    else:
        return HTTPException(detail="Invalid request", status_code=400)

@router.post('/get_messages', response_class=JSONResponse)
async def post_get_messages(query: Query_Message):
    if (query.conversation_id):
        return MessagingModule.select_messages(MessagingModule.Message.conversation_id == query.conversation_id)
    return []

    
@router.get('/list_conversations', response_class=JSONResponse)
async def get_list_conversations():
    return MessagingModule.list_conversations()