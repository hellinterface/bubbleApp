
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

class Conversation_createRequest(BaseModel):
    type: str
    allowed_from1: int
    allowed_from2: Optional[int]

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: Optional[int] = Field(default=None, foreign_key="conversation.id")
    text: str = Field()
    media_ids: list = Field(sa_column=Column(JSON))
    edited: bool = Field(default=False)
    sender_id: int = Field()
    time: int = Field()
    class Config:
        arbitrary_types_allowed = True

class Message_createRequest(BaseModel):
    conversation_id: int
    text: str
    media_ids: Optional[list]
    sender_id: int

DIRNAME = os.path.dirname(os.path.dirname(__file__))
DB_PATH = DIRNAME + '\\data\\db_messaging.db'
print(DB_PATH)
sqlite_url = f"sqlite:///{DB_PATH}"
engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)

def get_current_time():
    creation_time = datetime.now()
    creation_time = mktime(creation_time.timetuple())
    return creation_time

class Create:
    @staticmethod
    def conversation(request: Conversation_createRequest) -> Conversation:
        with Session(engine) as session:
            new_conversation = Conversation(**request.__dict__)
            print(new_conversation)
            session.add(new_conversation)
            session.commit()
            session.refresh(new_conversation)
            return new_conversation
    @staticmethod
    def message(request: Message_createRequest):
        new_message = Message(**request.__dict__, time=get_current_time(), edited=False)
        print(new_message)
        with Session(engine) as session:
            session.add(new_message)
            session.commit()
            session.refresh(new_message)
            return new_message

class Select:
    @staticmethod
    def __select(targetType, *expressions) -> list:
        with Session(engine) as session:
            statement = select(targetType)
            if len(expressions) != 0:
                statement = statement.where(*expressions)
            results = session.exec(statement)
            result_list = results.all()
            print("Select:")
            print(result_list)
            return result_list
    @staticmethod
    def __select_one(targetType, *expressions):
        with Session(engine) as session:
            statement = select(targetType)
            if len(expressions) != 0:
                statement = statement.where(*expressions)
            results = session.exec(statement)
            return results.one()
    @staticmethod
    def conversations(*expressions):
        return Select.__select(Conversation, *expressions)
    @staticmethod
    def messages(*expressions):
        return Select.__select(Message, *expressions)
    @staticmethod
    def oneConversation(*expressions):
        return Select.__select_one(Conversation, *expressions)
    @staticmethod
    def oneMessage(*expressions):
        return Select.__select_one(Message, *expressions)

class List:
    @staticmethod
    def conversations():
        return Select.conversations()
    @staticmethod
    def messages():
        return Select.messages()

