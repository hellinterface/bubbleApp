
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, JSON, Column, Session, select, or_, and_
from datetime import datetime, timedelta, date
from time import mktime

from .. import config
from ..models import Output_Message, Output_PersonalConversation

from ..requests import Message_CreateRequest, Message_UpdateRequest, Conversation_CreateRequest

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str = Field(default="personal")
    allowed_from1: int = Field()
    allowed_from2: Optional[int] = Field(default=None)

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int
    text: str = Field()
    edited: bool = Field(default=False)
    sender_id: int = Field()
    time: int = Field()
    shared_message_id: Optional[int] = Field()

class MessageMedia(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_id: int
    message_id: int

###
###   SQL Database Engine
###

sqlite_url = f"sqlite:///{config.DB_PATH}"
engine = create_engine(sqlite_url, echo=config.SQL_ECHO)
SQLModel.metadata.create_all(engine)

def get_current_time():
    creation_time = datetime.now()
    creation_time = mktime(creation_time.timetuple())
    return creation_time

class Convert:
    @staticmethod
    def message(message: Message) -> Output_Message:
        from ..cores import core_users as UsersModule
        result = Output_Message(
            id = message.id,
            text = message.text,
            edited = message.edited,
            sender = UsersModule.Convert.userToPublic(UsersModule.Select.oneUser(message.sender_id==UsersModule.User.id)),
            time = message.time,
            media_ids = [i.id for i in RawSelect.select(MessageMedia, MessageMedia.message_id==message.id)],
            shared_message = Select.oneMessage(Message.id == message.shared_message_id)
        )
        return result
    @staticmethod
    def personalConversation(conversation: Conversation, requesting_user_id: int) -> Output_PersonalConversation:
        from ..cores import core_users as UsersModule
        user_to = conversation.allowed_from1
        if (user_to == requesting_user_id):
            user_to = conversation.allowed_from2
        result = Output_PersonalConversation(
            id=conversation.id,
            other_user=UsersModule.Convert.userToPublic(UsersModule.Select.oneUser(UsersModule.User.id==user_to)),
        )
        return result
        

class Create:
    @staticmethod
    def conversation(request: Conversation_CreateRequest) -> Conversation:
        debugPrefix = "MESSAGING :: Creating conversation ::"
        print(f"{debugPrefix} Request:")
        print(request)
        new_conversation = Conversation(**request.__dict__)
        print(f"{debugPrefix} Object:")
        print(new_conversation)
        with Session(engine) as session:
            session.add(new_conversation)
            session.commit()
            session.refresh(new_conversation)
            print(f"{debugPrefix} Success.")
            return new_conversation
    @staticmethod
    def message(request: Message_CreateRequest) -> Message:
        from ..cores import core_users as UsersModule
        debugPrefix = "MESSAGING :: Creating message object ::"
        print(f"{debugPrefix} Request:")
        print(request)
        sender = UsersModule.Select.oneUser(UsersModule.User.id == request.sender_id)
        if sender == None:
            raise Exception()
        if len(request.new_media) > 0:
            from ..cores import core_files as FilesModule
            for i in request.new_media:
                FilesModule.Create.file(FilesModule.File_CreateRequest(owner_id=request.sender_id, parent_folder_id=sender.sent_media_folder_id, unrestricted_view_access=True))
        new_message = Message(**request.__dict__, time=get_current_time(), edited=False)
        print(f"{debugPrefix} Object:")
        print(new_message)
        with Session(engine) as session:
            session.add(new_message)
            session.commit()
            session.refresh(new_message)
            print(f"{debugPrefix} Success.")
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
    def extendedSelect(type, expressions:list, order_by=None, offset:int=0, limit:int=10**100) -> list:
        with Session(engine) as session:
            statement = select(type)
            if len(expressions) != 0:
                statement = statement.where(*expressions)
            print(order_by)
            print(order_by.__class__)
            if order_by is not None:
                statement = statement.order_by(order_by)
            statement = statement.offset(offset).limit(limit)
            results = session.exec(statement)
            result_list = results.all()
            print("Select (extended):")
            print(result_list)
            return result_list
    @staticmethod
    def select_one(targetType, *expressions):
        with Session(engine) as session:
            statement = select(targetType)
            if len(expressions) != 0:
                statement = statement.where(*expressions)
            results = session.exec(statement)
            return results.one_or_none()
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
        result = RawSelect.oneMessage(*expressions)
        if result == None: return None
        return Convert.message(result)
    @staticmethod
    def personalConversations(requesting_user_id: int, *expressions):
        arr = RawSelect.conversations(Conversation.type == "personal", or_(Conversation.allowed_from1 == requesting_user_id, Conversation.allowed_from2 == requesting_user_id), *expressions)
        resultArray = []
        for i in arr:
            resultArray.append(Convert.personalConversation(requesting_user_id=requesting_user_id, conversation=i))
        return resultArray
    @staticmethod
    def oneConversation(*expressions) -> Conversation:
        result = RawSelect.oneConversation(*expressions)
        if result == None: return None
        return result
    @staticmethod
    def messages_extended(expressions: list, offset: int, limit: int, order_by: Column):
        result = RawSelect.extendedSelect(type=Message, expressions=expressions, offset=offset, limit=limit, order_by=order_by)
        return list(map(Convert.message, result))

class List:
    @staticmethod
    def conversations():
        return Select.conversations()
    @staticmethod
    def messages():
        return Select.messages()

class Update:
    @staticmethod
    def message(request: Message_UpdateRequest) -> Message:
        print(request)
        targetObject = RawSelect.oneMessage(Message.id == request.id)
        if (targetObject.text == request.text) or (request.text == None):
            return targetObject
        targetObject.text = request.text
        with Session(engine) as session:
            session.add(targetObject)
            session.commit()
            session.refresh(targetObject)
            return targetObject

class Delete:
    @staticmethod
    def message(target_id: int) -> Message:
        target = RawSelect.select_one(Message, Message.id == target_id)
        if (target != None):
            with Session(engine) as session:
                session.delete(target)  
                session.commit()
                return target
        else:
            raise Exception()