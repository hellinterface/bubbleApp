

from fastapi import APIRouter, Depends, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel, Field
import sqlite3
import os
import secrets
import json
from ..bdata import BData

router = APIRouter(
    prefix="/api/groups",
    tags=["groups"],
    responses={404: {"description": "Not found"}},
)

# class PermissionsObject(BaseModel):

class Group(BaseModel):
    id: str = Field(allow_mutation=False, bdata_unique=True)
    title: str = Field()
    handle: str = Field()
    avatar_fileid: str = Field()
    invite_link: str = Field()
    invite_link_refresh_time: int = Field()
    folder_id: str = Field()
    color: str = Field()
    permissions: str = Field()
    users: list[str] = Field(bdata_type=str)

class Group_CreateRequest(BaseModel):
    title: str = Field()
    handle: str|None = Field()

class Channel(BaseModel):
    id: str = Field(allow_mutation=False, bdata_unique=True)
    title: str = Field()
    private: int = Field()
    permissions: dict = Field(bdata_type=str)
    users: list[str] = Field(bdata_type=str)
    taskboard_ids: list[str] = Field(bdata_type=str)
    planned_events: list[str] = Field(bdata_type=str)
    is_primary: int = Field()

class Channel_CreateRequest(BaseModel):
    title: str = Field()
    private: int = Field()

class UserOfGroup(BaseModel):
    id: str = Field(allow_mutation=False, bdata_unique=True)
    user_level: int = Field()

def group_factory(cursor, row):
    # print(u"current directory: %s" % os.getcwd())
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    print(d)
    resultObject = Group(**d)
    return resultObject

defaultGroupPermissionsObject = {
    "users": {
        "view_channels": 1, "manage_channels": 0, "manage_roles": 0, "create_invites": 1,
        "change_nickname": 1, "manage_nicknames": 0, "kick_members": 0, "ban_members": 0,
        "manage_server": 0,
        "send_messages": 1, "attach_files": 0, "delete_messages": 0, "mention_users": 1, "mention_groups": 0,
        "start_meetings": 1, "plan_meetings": 0, "speak": 1, "video": 1, "manage_meetings": 0
    },
    "mods": {
        "view_channels": 1, "manage_channels": 0, "manage_roles": 0, "create_invites": 1,
        "change_nickname": 1, "manage_nicknames": 1, "kick_members": 1, "ban_members": 1,
        "manage_server": 0,
        "send_messages": 1, "attach_files": 1, "delete_messages": 1, "mention_users": 1, "mention_groups": 1,
        "start_meetings": 1, "plan_meetings": 1, "speak": 1, "video": 1, "manage_meetings": 1
    }
}

DB_GROUPS_PATH = os.path.dirname(os.path.dirname(__file__)) + '\\groups_db.db'
print(DB_GROUPS_PATH)
bdata = BData(DB_GROUPS_PATH, group_factory)

tables = bdata.get_tables()
print("Tables:")
print(tables)
if ("Groups" not in tables):
    bdata.create("Groups", Group)

@router.post("/create_group", response_class=JSONResponse)
async def post_create_group(request: Group_CreateRequest):
    print(request)
    id = secrets.token_urlsafe(6)
    groupToCreate = Group(**request)
    groupToCreate.id = id
    groupToCreate.permissions = defaultGroupPermissionsObject
    print(groupToCreate)
    try:
        # targetUserList = bdata.insert("Boards", groupToCreate)
        return {"response": "success", "group_id": id} 
    except:
        return {"response": "failure"}
        
    
@router.get("/list", response_class=JSONResponse)
async def read_items():
    res = bdata.select('Groups', '*')
    print("Group list: " + str(len(res)))
    for i in res:
        print(i)
    return {"response": "success"}