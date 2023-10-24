
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

def groupInList_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    groupObject = GroupInList(**d)
    return groupObject

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
def getDBConnection(filepath, factory = groupInList_factory):
    conn = sqlite3.connect(filepath)
    conn.row_factory = factory
    if not checkDB(filepath):
        createGroupsTable(conn)
    return conn

class GroupCreateInfo(BaseModel):
    title: str
    handle: str | None = None

class GroupInList(BaseModel):
    id: str
    title: str
    handle: str

@router.get("/list", response_class=JSONResponse)
async def get_list():
    dbc = getDBConnection(DB_GROUP_LIST)
    grouplist = dbc.execute("SELECT * FROM Group_List").fetchall()
    print(grouplist)
    return {"hello": "none"}

def addGroupToDB(groupObject: GroupInList):
    dbc = getDBConnection(DB_GROUP_LIST, int)
    ###################################################################################
    check_string = f'SELECT COUNT(*) FROM Group_List WHERE id="{groupObject.id}" OR handle="{groupObject.handle}"'
    if (dbc.execute(check_string).fetchone() != 0):
        return False
    dbc.close()
    dbc = getDBConnection(DB_GROUP_LIST)
    cur = dbc.cursor()
    string = f'INSERT INTO Group_List (id, title, handle) VALUES ("{groupObject.id}", "{groupObject.title}", "{groupObject.handle}")'
    cur.execute(string)
    dbc.commit()
    dbc.close()
    return True

@router.get("/create", response_class=HTMLResponse)
async def post_create():
    f = open("app_internal/svc_groups/create_group.html", "r", encoding="utf-8")
    return f.read()

@router.post("/create", response_class=JSONResponse)
async def post_create(request: Request):
    data = await request.json()
    data["id"] = secrets.token_urlsafe(6)
    object = GroupInList(**data)
    print(object)
    addGroupToDB(object)
    return {"hello": "none"}