
from pydantic import BaseModel, Field
import os
import secrets
import json
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, JSON, Column, Session, select, or_, and_
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, date
from time import mktime
from ..modules import mod_users as UsersModule

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str = Field(default="personal")
    allowed_from1: int = Field()
    allowed_from2: Optional[int] = Field(default=None)

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: Optional[int] = Field(default=None, foreign_key="conversation.id")
    text: str = Field()
    media_ids: list = Field(sa_column=Column(JSON))
    edited: bool = Field(default=False)
    #sender: UsersModule.User_Public = Field(sa_column=Column(JSON))
    sender: dict = Field(sa_column=Column(JSON))
    time: int = Field()
    class Config:
        arbitrary_types_allowed = True


DIRNAME = os.path.dirname(os.path.dirname(__file__))
DB_PATH = DIRNAME + '\\data\\db_messaging.db'
print(DB_PATH)
sqlite_url = f"sqlite:///{DB_PATH}"
engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)

def create_conversation(type, allowed_from1, allowed_from2 = None):
    """
    if (type == "personal") and (isinstance(allowed_from, list)):
        new_conversation = Conversation(type=type, allowed_from=json.dumps(allowed_from))
    if (type == "channel") and (isinstance(allowed_from, str)):
        new_conversation = Conversation(type=type, allowed_from=allowed_from)
    else:
        return Exception()
    """
    if (type == "personal"):
        new_conversation = Conversation(type=type, allowed_from1=allowed_from1, allowed_from2=allowed_from2)
    elif (type == "channel"):
        new_conversation = Conversation(type=type, allowed_from1=allowed_from1)
    else:
        return Exception()
    with Session(engine) as session:
        session.add(new_conversation)
        session.commit()
        session.refresh(new_conversation)
        return new_conversation

def select_conversations(*expressions) -> list[Conversation]:
    with Session(engine) as session:
        statement = select(Conversation)
        if len(expressions) > 0:
            statement = statement.where(*expressions)
        results = session.exec(statement)
        result_list = results.all()
        print("Select conversations:")
        print(result_list)
        return result_list

def list_conversations() -> list[Conversation]:
    return select_conversations()

def create_message(user_id: str, conversation_id: int, text: str, media_ids: list[int], time: int):
    user_list = UsersModule.select_users(UsersModule.User.id == user_id)
    sender = UsersModule.convertUserToPublic(user_list[0])
    print("SENDER IS")
    print(sender)
    new_message = Message(
        sender=sender.__dict__, 
        conversation_id=conversation_id,
        text=text,
        media_ids=media_ids,
        time=time,
        edited=False)
    print(new_message)
    with Session(engine) as session:
        session.add(new_message)
        session.commit()
        session.refresh(new_message)
        return new_message

def create_message_channel(user_from: str, channel_id: int, text: str, media_ids: list[int], time: int):
    conversation_list = select_conversations(Conversation.allowed_from1 == channel_id)
    if len(conversation_list) <= 0:
        return Exception()
    return create_message(user_id=user_from, conversation_id=conversation_list[0].id, text=text, media_ids=media_ids, time=time)

def create_message_personal(user_from: str, user_to: int, text: str, media_ids: list[int], time: int):
    conversation_list = select_conversations(
        or_(
            and_(Conversation.allowed_from1 == user_from, Conversation.allowed_from2 == user_to),
            and_(Conversation.allowed_from1 == user_to, Conversation.allowed_from2 == user_from)
        )
    )
    if len(conversation_list) <= 0:
        return Exception()
    return create_message(user_id=user_from, conversation_id=conversation_list[0].id, text=text, media_ids=media_ids, time=time)

def select_messages(*expressions) -> list[Message]:
    with Session(engine) as session:
        statement = select(Message)
        if len(expressions) > 0:
            statement = statement.where(*expressions)
        results = session.exec(statement)
        result_list = results.all()
        print("Select messages:")
        print(result_list)
        return result_list

def list_messages() -> list[Message]:
    return select_messages()