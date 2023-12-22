
from pydantic import BaseModel, Field
import os
import secrets
import json
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, JSON, Column, Session, select
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, date
from time import mktime
from ..modules import mod_users as UsersModule
from ..modules import mod_messaging as MessagingModule

class Output_UserEntry(BaseModel):
    user_information: UsersModule.Output_User
    permission_level: str = Field(default="user")
    banned: bool = Field(default=False)

class Output_Channel(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field()
    title: str = Field()
    private: bool = Field()
    permissions: dict = Field()
    taskboard_ids: list[int] = Field(default=[])
    planned_events: list[int] = Field(default=[])
    is_primary: bool = Field()
    users: list[Output_UserEntry] = Field(default=[])

class Output_Group(BaseModel):
    id: Optional[int] = Field(default=None)
    title: str
    handle: Optional[str]
    avatar_fileid: Optional[int]
    permissions: dict
    folder_id: str
    color: str
    invite_link: str
    invite_link_refresh_time: int
    users: list[Output_UserEntry] = Field(default=[])
    channels: list[Output_Channel] = Field(default=[])

class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    handle: Optional[str]
    avatar_fileid: Optional[int]
    permissions: dict = Field(sa_column=Column(JSON))
    folder_id: str
    color: str = Field()
    invite_link: str = Field()
    invite_link_refresh_time: int = Field(sa_column=Column(JSON))
    class Config:
        arbitrary_types_allowed = True

class Group_CreateRequest(BaseModel):
    title: str = Field()
    handle: Optional[str] = Field()
    owner_id: int

class Channel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field()
    title: str = Field()
    private: bool = Field()
    permissions: dict = Field(sa_column=Column(JSON))
    taskboard_ids: list[int] = Field(sa_column=Column(JSON))
    planned_events: list[int] = Field(sa_column=Column(JSON))
    is_primary: bool = Field()

class Channel_CreateRequest(BaseModel):
    title: str = Field()
    group_id: int = Field()
    private: int = Field()
    owner_id: int
    is_primary: bool

class GroupUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field()
    group_id: int = Field()
    permission_level: str = Field(default="user")
    banned: bool = Field(default=False)

class GroupUser_CreateRequest(BaseModel):
    user_id: int
    group_id: int
    permission_level: str

class ChannelUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field()
    channel_id: int = Field()
    permission_level: str = Field(default="user")
    banned: bool = Field(default=False)

class ChannelUser_CreateRequest(BaseModel):
    user_id: int
    channel_id: int
    permission_level: str

DIRNAME = os.path.dirname(os.path.dirname(__file__))
DB_GROUPS_PATH = DIRNAME + '\\data\\db_groups.db'
print(DB_GROUPS_PATH)
sqlite_url = f"sqlite:///{DB_GROUPS_PATH}"
engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)

defaultGroupPermissionsObject = {
    "user": {
        "view_channels": 1, "manage_channels": 0, "manage_roles": 0, "create_invites": 1,
        "change_nickname": 1, "manage_nicknames": 0, "kick_members": 0, "ban_members": 0,
        "manage_server": 0,
        "send_messages": 1, "attach_files": 0, "delete_messages": 0, "mention_users": 1, "mention_groups": 0,
        "start_meetings": 1, "plan_meetings": 0, "speak": 1, "video": 1, "manage_meetings": 0
    },
    "mod": {
        "view_channels": 1, "manage_channels": 0, "manage_roles": 0, "create_invites": 1,
        "change_nickname": 1, "manage_nicknames": 1, "kick_members": 1, "ban_members": 1,
        "manage_server": 0,
        "send_messages": 1, "attach_files": 1, "delete_messages": 1, "mention_users": 1, "mention_groups": 1,
        "start_meetings": 1, "plan_meetings": 1, "speak": 1, "video": 1, "manage_meetings": 1
    },
    "owner": {
        "view_channels": 1, "manage_channels": 1, "manage_roles": 1, "create_invites": 1,
        "change_nickname": 1, "manage_nicknames": 1, "kick_members": 1, "ban_members": 1,
        "manage_server": 1,
        "send_messages": 1, "attach_files": 1, "delete_messages": 1, "mention_users": 1, "mention_groups": 1,
        "start_meetings": 1, "plan_meetings": 1, "speak": 1, "video": 1, "manage_meetings": 1
    },
}

defaultChannelPermissionsObject = {
    "user": {
        "kick_members": 0, "ban_members": 0,
        "send_messages": 1, "attach_files": 0, "delete_messages": 0, "mention_users": 1, "mention_groups": 0,
        "start_meetings": 1, "plan_meetings": 0, "speak": 1, "video": 1, "manage_meetings": 0
    },
    "mod": {
        "kick_members": 0, "ban_members": 0,
        "send_messages": 1, "attach_files": 0, "delete_messages": 0, "mention_users": 1, "mention_groups": 0,
        "start_meetings": 1, "plan_meetings": 0, "speak": 1, "video": 1, "manage_meetings": 0
    },
}

class Convert:
    @staticmethod
    def group(group: Group) -> Output_Group:
        return Output_Group(
            **group.__dict__,
            users = Select.groupUsers(GroupUser.group_id == group.id),
            channels = Select.channels(Channel.group_id == group.id)
            )
    @staticmethod
    def channel(channel: Channel) -> Output_Channel:
        return Output_Channel(
            **channel.__dict__,
            users = Select.channelUsers(ChannelUser.channel_id == channel.id)
            )
    @staticmethod
    def groupUser(userEntry: GroupUser) -> Output_UserEntry:
        return Output_UserEntry(
            **userEntry.__dict__, 
            user_information = UsersModule.Select.oneUser(UsersModule.User.id == userEntry.user_id)
            )
    @staticmethod
    def channelUser(userEntry: ChannelUser) -> Output_UserEntry:
        return Output_UserEntry(
            **userEntry.__dict__,
            user_information = UsersModule.Select.oneUser(UsersModule.User.id == userEntry.user_id)
            )

class Create:
    @staticmethod
    def group(request: Group_CreateRequest) -> Group:
        print(request)
        print(request.dict())
        print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
        groupToCreate = Group(**request.dict())
        groupToCreate.permissions = defaultGroupPermissionsObject
        groupToCreate.avatar_fileid = None
        groupToCreate.folder_id = secrets.token_urlsafe(8)
        groupToCreate.invite_link = secrets.token_urlsafe(20)
        groupToCreate.color = "#6699ee"
        inviteLinkRefreshTime = datetime.now() + timedelta(hours=6)
        inviteLinkRefreshTime = mktime(inviteLinkRefreshTime.timetuple())
        print(inviteLinkRefreshTime)
        groupToCreate.invite_link_refresh_time = inviteLinkRefreshTime
        print(groupToCreate)

        with Session(engine) as session:
            session.add(groupToCreate)
            session.commit()
            session.refresh(groupToCreate)

            groupUser = Create.groupUser(GroupUser_CreateRequest(user_id=request.owner_id, group_id=groupToCreate.id, permission_level="owner"))
            channelToCreate = Create.channel(Channel_CreateRequest(group_id=groupToCreate.id, title="Primary channel", private=False, owner_id=request.owner_id, is_primary=True, permissions=generate_channel_permissions_from_group(groupToCreate)))
            
            return groupToCreate
    def channel(request: Channel_CreateRequest) -> Channel:
        permissions = get_group_permissions_of_user(group_id=request.group_id, user_id=request.owner_id)
        if (not permissions.get("manage_channels")):
            raise Exception()
        with Session(engine) as session:
            channelToCreate = Channel(
                **request.__dict__,
                permissions=generate_channel_permissions_from_group(Select.select_one(Group, Group.id == request.group_id)),
                taskboard_ids=[], planned_events=[])
            print(channelToCreate)
            session.add(channelToCreate)
            session.commit()
            session.refresh(channelToCreate)
            newConversation = MessagingModule.Create.conversation(MessagingModule.Conversation_createRequest(type="channel", allowed_from1=channelToCreate.id))
            for i in Select.groupUsers(GroupUser.group_id == request.group_id):
                permission_level = "user"
                if (i.permission_level == "owner" or i.user_information.id == request.owner_id):
                    permission_level = "owner"
                Create.channelUser(
                    ChannelUser_CreateRequest(user_id=i.user_information.id, channel_id=channelToCreate.id, permission_level=permission_level)
                    )
            return channelToCreate
    def channelUser(request: ChannelUser_CreateRequest)-> ChannelUser:    
        with Session(engine) as session:
            newGroupUser = ChannelUser(**request.__dict__, banned=False)
            session.add(newGroupUser)
            session.commit()
            session.refresh(newGroupUser)
            return newGroupUser
    def groupUser(request: GroupUser_CreateRequest) -> GroupUser:    
        with Session(engine) as session:
            newGroupUser = GroupUser(**request.__dict__, banned=False)
            session.add(newGroupUser)
            session.commit()
            session.refresh(newGroupUser)
            return newGroupUser

class Select:
    ### Select # Raw
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

    ### Select # Output_*
    @staticmethod
    def groups(*expressions) -> list[Output_Group]:
        return list(map(Convert.group, Select.select(Group, *expressions)))
    @staticmethod
    def channels(*expressions) -> list[Output_Channel]:
        return list(map(Convert.channel, Select.select(Channel, *expressions)))
    @staticmethod
    def groupUsers(*expressions) -> list[Output_UserEntry]:
        return list(map(Convert.groupUser, Select.select(GroupUser, *expressions)))
    @staticmethod
    def channelUsers(*expressions) -> list[Output_UserEntry]:
        return list(map(Convert.channelUser, Select.select(ChannelUser, *expressions)))
    @staticmethod
    def groupsOfUser(user_id: int) -> list[Output_UserEntry]:
        group_user_list = Select.select(GroupUser, GroupUser.user_id == user_id)
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
        return Convert.group(Select.select_one(Group, *expressions))
    @staticmethod
    def oneChannel(*expressions) -> Output_Channel:
        return Convert.channel(Select.select_one(Channel, *expressions))
    @staticmethod
    def oneGroupUser(*expressions) -> Output_UserEntry:
        return Convert.groupUser(Select.select_one(GroupUser, *expressions))
    @staticmethod
    def oneChannelUser(*expressions) -> Output_UserEntry:
        return Convert.channelUser(Select.select_one(ChannelUser, *expressions))

"""
class Channel_CreateRequest(BaseModel):
    title: str = Field()
    group_id: int = Field()
    private: int = Field()
    
    
    "owner": {
        "view_channels": 1, "manage_channels": 1, "manage_roles": 1, "create_invites": 1,
        "change_nickname": 1, "manage_nicknames": 1, "kick_members": 1, "ban_members": 1,
        "manage_server": 1,
        "send_messages": 1, "attach_files": 1, "delete_messages": 1, "mention_users": 1, "mention_groups": 1,
        "start_meetings": 1, "plan_meetings": 1, "speak": 1, "video": 1, "manage_meetings": 1
defaultChannelPermissionsObject = {
    "user": {
        "kick_members": 0, "ban_members": 0,
        "send_messages": 1, "attach_files": 0, "delete_messages": 0, "mention_users": 1, "mention_groups": 0,
        "start_meetings": 1, "plan_meetings": 0, "speak": 1, "video": 1, "manage_meetings": 0
    },
    """

def generate_channel_permissions_from_group(group: Group):
    new_permissions = {}
    to_ignore = ["view_channels", "manage_channels", "manage_roles", "create_invites", "change_nickname", "manage_nicknames", "manage_server"]
    for (key, value) in group.permissions.items():
        new_permissions[key] = {}
        for (i_key, i_value) in value.items():
            if i_key != new_permissions[key]:
                new_permissions[key][i_key] = i_value
    return new_permissions


def get_group_permissions_of_user(user_id: int, group_id: int):
    group = Select.oneGroup(Group.id == group_id)
    groupUser = Select.oneGroupUser(GroupUser.group_id == group_id, GroupUser.user_id == user_id)
    print(group.permissions)
    return group.permissions.get(groupUser.permission_level)

def get_channel_permissions_of_user(user_id: int, channel_id: int):
    channel = Select.oneChannel(Channel.id == channel_id)
    channelUser = Select.oneChannelUser(ChannelUser.channel_id == channel_id, ChannelUser.user_id == user_id)
    print(channel.permissions)
    return channel.permissions.get(channelUser.permission_level)
