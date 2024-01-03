
from pydantic import BaseModel, Field
import os
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, JSON, Column, Session, select, or_, and_
from datetime import datetime, timedelta, date
from time import mktime
from ..modules import mod_users as UsersModule
from ..modules import mod_files as FilesModule
from fastapi import File as FastAPI_File

class Output_Message(BaseModel):
    id: int
    text: str
    edited: bool
    sender_id: UsersModule.PublicOutput_User
    time: int
    media_ids: list[int]
    shared_message: Output_Message

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str = Field(default="personal")
    allowed_from1: int = Field()
    allowed_from2: Optional[int] = Field(default=None)

class Conversation_CreateRequest(BaseModel):
    type: str
    allowed_from1: int
    allowed_from2: Optional[int]

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int
    text: str = Field()
    edited: bool = Field(default=False)
    sender_id: int = Field()
    time: int = Field()
    shared_message_id: Optional[int] = Field()

class Message_CreateRequest(BaseModel):
    conversation_id: int
    text: str
    new_media: Optional[list[FastAPI_File]]
    existing_media: Optional[list[int]]
    sender_id: int
    shared_message_id: Optional[int]

class MessageMedia(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_id: int
    message_id: int

class Message_UpdateRequest(BaseModel):
    id: int
    text: Optional[str]


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

class Convert:
    @staticmethod
    def message(message: Message) -> Output_Message:
        result = Output_Message(
            id = message.id,
            text = message.text,
            edited = message.edited,
            sender = UsersModule.Convert.userToPublic(UsersModule.Select.oneUser(message.sender_id==UsersModule.User.id)),
            time = message.time,
            media_ids = [i.id for i in RawSelect.select(MessageMedia, MessageMedia.message_id==message.id)],
            shared_message = Select.message(Message.id == message.shared_message_id)
        )
        return result

class Create:
    @staticmethod
    def conversation(request: Conversation_CreateRequest) -> Conversation:
        with Session(engine) as session:
            new_conversation = Conversation(**request.__dict__)
            print(new_conversation)
            session.add(new_conversation)
            session.commit()
            session.refresh(new_conversation)
            return new_conversation
    @staticmethod
    def message(request: Message_CreateRequest) -> Message:
        sender = UsersModule.Select.oneUser(UsersModule.User.id == request.sender_id)
        if sender == None:
            raise Exception()
        if len(request.new_media) > 0:
            for i in request.new_media:
                FilesModule.Create.file(FilesModule.File_CreateRequest(owner_id=request.sender_id, parent_folder_id=sender.sent_media_folder_id, unrestricted_view_access=True))
        new_message = Message(**request.__dict__, time=get_current_time(), edited=False)
        print(new_message)
        with Session(engine) as session:
            session.add(new_message)
            session.commit()
            session.refresh(new_message)
            return new_message

class RawSelect:
    @staticmethod
    def select(targetType, *expressions) -> list:
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
    def select_one(targetType, *expressions):
        with Session(engine) as session:
            statement = select(targetType)
            if len(expressions) != 0:
                statement = statement.where(*expressions)
            results = session.exec(statement)
            return results.one()
    @staticmethod
    def conversations(*expressions) -> list[Conversation]:
        return RawSelect.select(Conversation, *expressions)
    @staticmethod
    def messages(*expressions) -> list[Message]:
        return RawSelect.select(Message, *expressions)
    @staticmethod
    def oneConversation(*expressions) -> Conversation:
        return RawSelect.select_one(Conversation, *expressions)
    @staticmethod
    def oneMessage(*expressions) -> Message:
        return RawSelect.select_one(Message, *expressions)

class Select:
    @staticmethod
    def messages(*expressions) -> list[Output_Message]:
        return list(map(Convert.message, RawSelect.messages(*expressions)))
    @staticmethod
    def oneMessage(*expressions) -> Output_Message:
        return Convert.message(RawSelect.oneMessage(*expressions))

class List:
    @staticmethod
    def conversations():
        return Select.conversations()
    @staticmethod
    def messages():
        return Select.messages()

class Update:
    @staticmethod
    def message(request:Message_UpdateRequest) -> Message:
        print(request)
        targetObject = Select.oneMessage(Message.id == request.id)
        for (key, value) in iter(request):
            if (value != None):
                print(key, value)
                setattr(targetObject, key, value)
        print(targetObject)
        with Session(engine) as session:
            session.add(targetObject)
            session.commit()
            session.refresh(targetObject)
            return targetObject