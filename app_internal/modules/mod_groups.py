
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
    user_id: int = Field()
    visible_name: str = Field()
    handle: str = Field()
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
    handle: str|None
    avatar_fileid: str|None
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
    handle: str|None
    avatar_fileid: str|None
    permissions: dict = Field(sa_column=Column(JSON))
    folder_id: str
    color: str = Field()
    invite_link: str = Field()
    invite_link_refresh_time: int = Field(sa_column=Column(JSON))
    class Config:
        arbitrary_types_allowed = True

class Group_CreateRequest(BaseModel):
    title: str = Field()
    handle: str|None = Field()

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

class GroupUserRecord(SQLModel, table=True):
    user_id: int = Field(primary_key=True)
    group_id: int = Field()
    permission_level: str = Field(default="user")
    banned: bool = Field(default=False)

class ChannelUserRecord(SQLModel, table=True):
    user_id: int = Field(primary_key=True)
    channel_id: int = Field()
    permission_level: str = Field(default="user")
    banned: bool = Field(default=False)

DIRNAME = os.path.dirname(os.path.dirname(__file__))
DB_USERS_PATH = DIRNAME + '\\data\\db_groups.db'
print(DB_USERS_PATH)
sqlite_url = f"sqlite:///{DB_USERS_PATH}"
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

def convertUserRecordToOutput(user: ChannelUserRecord|GroupUserRecord) -> Output_UserEntry:
    user_list = UsersModule.select_users(UsersModule.User.id == user.user_id)
    user_publicInfo = UsersModule.convertUserToPublic(user_list[0])
    return Output_UserEntry(user_id=user.user_id, visible_name=user_publicInfo.visible_name, handle=user_publicInfo.handle, permission_level=user.permission_level, banned=user.banned)
    
def convertGroupToOutput(group: Group) -> Output_Group:
    print(group.__dict__)
    return Output_Group(**group.__dict__, users=[], channels=[])

def convertChannelToOutput(channel: Channel) -> Output_Channel:
    print("GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print(channel.__dict__)
    print("GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    return Output_Channel(**channel.__dict__, users=[])

def create_group(request: Group_CreateRequest, owner: UsersModule.User) -> Group:
    print(request)
    print(request.dict())
    print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP")
    print(owner)
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

        groupUserRecord = GroupUserRecord(user_id=owner.id, group_id=groupToCreate.id, permission_level="owner", banned=False)
        print(groupUserRecord)
        session.add(groupUserRecord)
        session.commit()
        session.refresh(groupUserRecord)

        channelToCreate = Channel(group_id=groupToCreate.id, title="Primary channel", private=False, permissions=generate_channel_permissions_from_group(groupToCreate), taskboard_ids=[], planned_events=[], is_primary=True)
        print(channelToCreate)
        session.add(channelToCreate)
        session.commit()
        session.refresh(channelToCreate)

        channelUserRecord = ChannelUserRecord(user_id=owner.id, channel_id=channelToCreate.id, permission_level="owner", banned=False)
        print(channelUserRecord)
        session.add(channelUserRecord)
        session.commit()
        session.refresh(channelUserRecord)
        
        newConversation = MessagingModule.create_conversation(type="channel", allowed_from1=channelToCreate.id)

        return groupToCreate

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

def create_channel(request: Channel_CreateRequest, owner: UsersModule.User) -> Channel:
    permissions = get_group_permissions_of_user(group_id=request.group_id, user_id=owner.id)
    if (not permissions.get("manage_channels")):
        raise Exception()
    with Session(engine) as session:
        channelToCreate = Channel(group_id=request.group_id, title=request.title, private=request.private, permissions=generate_channel_permissions_from_group, taskboard_ids=[], planned_events=[], is_primary=False)
        print(channelToCreate)
        session.add(channelToCreate)
        session.commit()
        session.refresh(channelToCreate)
        newConversation = MessagingModule.create_conversation(type="channel", allowed_from1=channelToCreate.id)

def __select_groups(*expressions) -> list[Group]:
    with Session(engine) as session:
        print("WWWWWWWWWWWW", len(expressions))
        statement = select(Group)
        if len(expressions) != 0:
            statement = statement.where(*expressions)
        results = session.exec(statement)
        result_list = results.all()
        print("Select groups:")
        print(result_list)
        return result_list

def select_groups(*expressions) -> list[Output_Group]:
    selected_list = __select_groups(*expressions)
    result_list = []
    with Session(engine) as session:
        for i in selected_list:
            output_group_object = convertGroupToOutput(i)
            output_group_object.users = []
            statement = select(GroupUserRecord).where(GroupUserRecord.group_id == i.id)
            results = session.exec(statement)
            for j in results:
                converted = convertUserRecordToOutput(j)
                output_group_object.users.append(converted)
            output_group_object.channels = select_channels(Channel.group_id == i.id)
            result_list.append(output_group_object)
    return result_list

def list_groups() -> list[Output_Group]:
    return select_groups()

def list_mine(user: UsersModule.User) -> list[Output_Group]:
    with Session(engine) as session:
        statement = select(GroupUserRecord).where(GroupUserRecord.user_id==user.id)
        results = session.exec(statement)
        groupUserRecordList = results.all()
        result_list = []
        for i in groupUserRecordList:
            group = select_groups(Group.id==i.group_id)[0]
            result_list.append(group)
        print("grouplist:")
        print(result_list)
        return result_list

def __select_channels(*expressions) -> list[Channel]:
    with Session(engine) as session:
        statement = select(Channel).where(*expressions)
        results = session.exec(statement)
        result_list = results.all()
        print("Select channels:")
        print(result_list)
        return result_list

def select_channels(*expressions) -> list[Output_Channel]:
    select_list = __select_channels(*expressions)
    result_list = []
    with Session(engine) as session:
        for i in select_list:
            output_channel_object = convertChannelToOutput(i)
            output_channel_object.users = []
            statement = select(ChannelUserRecord).where(ChannelUserRecord.channel_id == i.id)
            results = session.exec(statement)
            for j in results:
                converted = convertUserRecordToOutput(j)
                output_channel_object.users.append(converted)
            result_list.append(output_channel_object)
    return result_list

def list_channels() -> list[Output_Channel]:
    return select_channels()

def select_channelUserRecord(*expressions) -> list[ChannelUserRecord]:
    with Session(engine) as session:
        statement = select(ChannelUserRecord).where(*expressions)
        results = session.exec(statement)
        result_list = results.all()
        print("Select channels:")
        print(result_list)
        return result_list

def get_group_permissions_of_user(user_id: int, group_id: int):
    group_list = select_groups(Channel.id == group_id)
    if len(group_list) <= 0:
        raise Exception()
    for i in group_list[0].users:
        if (i.user_id == user_id):
            return_object = group_list[0].permissions.get(i.permission_level)
            if (return_object):
                return return_object
            raise Exception()

def get_channel_permissions_of_user(user_id: int, channel_id: int):
    channel_list = select_channels(Channel.id == channel_id)
    if len(channel_list) <= 0:
        raise Exception()
    for i in channel_list[0].users:
        if (i.user_id == user_id):
            return_object = channel_list[0].permissions.get(i.permission_level)
            if (return_object):
                return return_object
            raise Exception()

def add_user_to_group(user: UsersModule.User, group: Group, permission_level: str):
    with Session(engine) as session:
        newGroupUserRecord = GroupUserRecord(user_id=user.id, group_id=group.id, permission_level=permission_level, banned=False)
        session.add(newGroupUserRecord)
        session.commit()
        session.refresh(newGroupUserRecord)
        return newGroupUserRecord

"""

class GroupUserRecord(SQLModel, table=True):
    user_id: int = Field(primary_key=True)
    group_id: int = Field()
    permission_level: str = Field(default="user")
    banned: bool = Field(default=False)
    
"""