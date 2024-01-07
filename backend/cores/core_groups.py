
import secrets
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, JSON, Column, Session, select
from datetime import datetime, timedelta, date
from time import mktime
from .. import config
from ..models import Output_Group, Output_Channel, PublicOutput_User
from ..requests import Group_CreateRequest, GroupUser_CreateRequest, Channel_CreateRequest, Conversation_CreateRequest

class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    avatar_fileid: Optional[int]
    owner_id: int
    folder_id: str
    color: str = Field()
    class Config:
        arbitrary_types_allowed = True

class Channel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field()
    title: str = Field()
    is_primary: bool = Field()

class GroupUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field()
    group_id: int = Field()

sqlite_url = f"sqlite:///{config.DB_PATH}"
engine = create_engine(sqlite_url, echo=config.SQL_ECHO)
SQLModel.metadata.create_all(engine)

class Convert:
    @staticmethod
    def group(group: Group) -> Output_Group:
        from ..cores import core_users as UsersModule
        return Output_Group(
            **group.__dict__,
            users = Select.groupUsers(GroupUser.group_id == group.id),
            channels = Select.channels(Channel.group_id == group.id),
            owner=UsersModule.Select.oneUser(UsersModule.User.id == group.owner_id)
            )
    @staticmethod
    def channel(channel: Channel) -> Output_Channel:
        return Output_Channel(**channel.__dict__)
    @staticmethod
    def groupUser(userEntry: GroupUser) -> PublicOutput_User:
        from ..cores import core_users as UsersModule
        return UsersModule.Select.oneUser(UsersModule.User.id == userEntry.user_id)

class Create:
    @staticmethod
    def group(request: Group_CreateRequest) -> Group:
        from ..cores import core_files as FilesModule
        print(request)
        print(request.dict())
        print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
        groupToCreate = Group(**request.dict())
        groupToCreate.owner_id = request.owner_id
        groupToCreate.avatar_fileid = None
        groupToCreate.folder_id = -1
        groupToCreate.color = "#6699ee"
        print(groupToCreate)

        with Session(engine) as session:
            session.add(groupToCreate)
            session.commit()
            session.refresh(groupToCreate)

            groupUser = Create.groupUser(GroupUser_CreateRequest(user_id=request.owner_id, group_id=groupToCreate.id, permission_level="owner"))
            channelToCreate = Create.channel(Channel_CreateRequest(group_id=groupToCreate.id, title="Primary channel", owner_id=request.owner_id, is_primary=True))
            
            folder = FilesModule.Create.folder(
                FilesModule.Folder_CreateRequest(title="Хранилище группы " + request.title, owner_id=request.owner_id, groups_can_view=[groupToCreate.id])
            )
            groupToCreate.folder_id = folder.id
            session.add(groupToCreate)
            session.commit()
            session.refresh(groupToCreate)

            return groupToCreate
    def channel(request: Channel_CreateRequest) -> Channel:
        if (request.owner_id != RawSelect.oneGroup(Group.id == request.group_id).owner_id):
            raise Exception()
        with Session(engine) as session:
            from ..cores import core_messaging as MessagingModule
            channelToCreate = Channel(**request.__dict__)
            print(channelToCreate)
            session.add(channelToCreate)
            session.commit()
            session.refresh(channelToCreate)
            newConversation = MessagingModule.Create.conversation(Conversation_CreateRequest(type="channel", allowed_from1=channelToCreate.id))
            return channelToCreate
    def groupUser(request: GroupUser_CreateRequest) -> GroupUser:    
        with Session(engine) as session:
            newGroupUser = GroupUser(**request.__dict__, banned=False)
            session.add(newGroupUser)
            session.commit()
            session.refresh(newGroupUser)
            return newGroupUser

class RawSelect:
    @staticmethod
    def select(targetType, *expressions) -> list:
        with Session(engine) as session:
            statement = select(targetType)
            if len(expressions) != 0:
                statement = statement.where(*expressions)
            results = session.exec(statement)
            result_list = results.all()
            print(f"USERS :: Select <{targetType.__name__}>:")
            print(result_list)
            return result_list
    @staticmethod
    def select_one(targetType, *expressions):
        with Session(engine) as session:
            statement = select(targetType)
            if len(expressions) != 0:
                statement = statement.where(*expressions)
            result = session.exec(statement).one_or_none()
            print(f"USERS :: Select one <{targetType.__name__}>:")
            print(result)
            return result
    @staticmethod
    def groups(*expressions) -> list[Group]:
        return RawSelect.select(Group, *expressions)
    @staticmethod
    def channels(*expressions) -> list[Channel]:
        return RawSelect.select(Channel, *expressions)
    @staticmethod
    def groupUsers(*expressions) -> list[GroupUser]:
        return RawSelect.select(GroupUser, *expressions)
    @staticmethod
    def oneGroup(*expressions) -> Group:
        return RawSelect.select_one(Group, *expressions)
    @staticmethod
    def oneChannel(*expressions) -> Channel:
        return RawSelect.select_one(Channel, *expressions)
    @staticmethod
    def oneGroupUser(*expressions) -> GroupUser:
        return RawSelect.select_one(GroupUser, *expressions)


class Select:
    ### Select # Output_*
    @staticmethod
    def groups(*expressions) -> list[Output_Group]:
        return list(map(Convert.group, RawSelect.select(Group, *expressions)))
    @staticmethod
    def channels(*expressions) -> list[Output_Channel]:
        return list(map(Convert.channel, RawSelect.select(Channel, *expressions)))
    @staticmethod
    def groupUsers(*expressions) -> list[PublicOutput_User]:
        return list(map(Convert.groupUser, RawSelect.select(GroupUser, *expressions)))
    @staticmethod
    def groupsOfUser(user_id: int) -> list[Output_Group]:
        group_user_list = RawSelect.select(GroupUser, GroupUser.user_id == user_id)
        result_list = []
        for i in group_user_list:
            try:
                group = Select.oneGroup(Group.id == i.group_id)
            except:
                print(f"Board with id {i.group_id} doesn't exist")
                continue
            result_list.append(group)
        return result_list
    @staticmethod
    def oneGroup(*expressions) -> Output_Group:
        return Convert.group(RawSelect.select_one(Group, *expressions))
    @staticmethod
    def oneChannel(*expressions) -> Output_Channel:
        return Convert.channel(RawSelect.select_one(Channel, *expressions))
    @staticmethod
    def oneGroupUser(*expressions) -> PublicOutput_User:
        return Convert.groupUser(RawSelect.select_one(GroupUser, *expressions))
