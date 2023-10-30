

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

class Group(BaseModel):
    id: str = Field(allow_mutation=False, bdata_unique=True)
    title: str = Field()
    handle: str = Field()
    avatar_fileid: str = Field()
    invite_link: str = Field()
    invite_link_refresh_time: int = Field()
    folder_id: str = Field()
    color: str = Field()
    permissions_owner: int = Field()
    permissions_admins: int = Field()
    permissions_mods: int = Field()
    permissions_users: int = Field()
    users: list[str] = Field(bdata_type=str)

class Group_CreateRequest(BaseModel):
    title: str = Field()
    handle: str|None = Field()

class Channel(BaseModel):
    id: str = Field(allow_mutation=False, bdata_unique=True)
    title: str = Field()
    private: int = Field()
    permissions_channelmods: int = Field()
    permissions_users: int = Field()
    users: list[str] = Field(bdata_type=str)
    taskboard_ids: list[str] = Field(bdata_type=str)
    planned_events: list[str] = Field(bdata_type=str)

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


DB_GROUPS_PATH = os.path.dirname(os.path.dirname(__file__)) + '\\groups_db.db'
print(DB_GROUPS_PATH)
bdata = BData(DB_GROUPS_PATH, group_factory)

tables = bdata.get_tables()
print("Tables:")
print(tables)
if ("Groups" not in tables):
    bdata.create("Boards", Group)

@router.post("/create_board", response_class=JSONResponse)
async def post_create_group(request: Group_CreateRequest):
    print(request)
    id = secrets.token_urlsafe(6)
    board = Group(**request)
    board.id = id
    print(board)
    try:
        # targetUserList = bdata.insert("Boards", board)
        return {"response": "success", "board_id": id} 
    except:
        return {"response": "failure"}
        
    
@router.get("/list", response_class=JSONResponse)
async def read_items():
    res = bdata.select('Groups', '*')
    print("Group list: " + str(len(res)))
    for i in res:
        print(i)
    return {"response": "success"}