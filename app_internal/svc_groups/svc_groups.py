
from fastapi import APIRouter, Depends, Request
from fastapi.responses import PlainTextResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from ..dependencies import get_token_header
from pydantic import BaseModel
import sqlite3
import os
import secrets
import json

router = APIRouter(
    prefix="/api/groups",
    tags=["groups"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

router.mount("/static", StaticFiles(directory="app_internal/svc_groups/"), name="static")

def createGroupsTable(dbc):
    dbc.execute('''CREATE TABLE "Group_List" (
	"id"	TEXT NOT NULL UNIQUE,
	"title"	TEXT NOT NULL,
	"handle"	TEXT,
	"handle"	TEXT,
	"handle"	TEXT,
	"handle"	TEXT,
	"handle"	TEXT,
	PRIMARY KEY("id")
    );''')


# проверка файла базы данных на валидность
def checkDB(filepath):
    conn = sqlite3.connect(filepath)
    conn.row_factory = sqlite3.Row
    tables = conn.execute("SELECT * FROM sqlite_master WHERE type='table'").fetchall()
    if len(tables) == 0:
        return False
    else:
        return True

DB_GROUP_LIST = 'group_list.db'

# подключение к базе данных
def getDBConnection(filepath):
    conn = sqlite3.connect(filepath)
    conn.row_factory = sqlite3.Row
    if not checkDB(filepath):
        createGroupsTable(conn)
    return conn

class GroupCreateInfo(BaseModel):
    title: str
    handle: str | None = None

class GroupInList(BaseModel):
    id: str
    title: str
    handle: str | None

@router.get("/list", response_class=JSONResponse)
async def get_list():
    dbc = getDBConnection(DB_GROUP_LIST)
    grouplist = dbc.execute("SELECT * FROM Group_List").fetchall()
    print(grouplist)
    return {"hello": "none"}

@router.get("/create", response_class=HTMLResponse)
async def post_create():
    f = open("app_internal/svc_groups/create_group.html", "r", encoding="utf-8")
    return f.read()

@router.post("/create", response_class=JSONResponse)
async def post_create(request: Request):
    data = await request.json()
    data["id"] = secrets.token_urlsafe(6)
    print(data)
    #dbc = getDBConnection(DB_GROUP_LIST)
    #grouplist = dbc.execute("SELECT * FROM Group_List").fetchall()
    return {"hello": "none"}