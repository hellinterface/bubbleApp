

from fastapi import APIRouter, Depends, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel, Field
import sqlite3
import os
import secrets
import json
from ..bdata import BData

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)

class TaskBoard(BaseModel):
    id: str = Field(allow_mutation=False, bdata_unique=True)
    title: str = Field()
    users_can_view: str = Field()
    users_can_edit: str = Field()

class TaskBoard_CreateRequest(BaseModel):
    title: str = Field()
    users_can_view: str|None = Field()
    users_can_edit: str|None = Field()

def board_factory(cursor, row):
    # print(u"current directory: %s" % os.getcwd())
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    print(d)
    resultObject = TaskBoard(**d)
    return resultObject


DB_TASKBOARDS_PATH = os.path.dirname(os.path.dirname(__file__)) + '\\taskboards_db.db'
print(DB_TASKBOARDS_PATH)
bdata = BData(DB_TASKBOARDS_PATH, board_factory)

tables = bdata.get_tables()
print("Tables:")
print(tables)
if ("Boards" not in tables):
    bdata.create("Boards", TaskBoard)

@router.post("/create_board", response_class=JSONResponse)
async def try_login(request: TaskBoard_CreateRequest):
    print(request)
    id = secrets.token_urlsafe(6)
    board = TaskBoard(**request)
    board.id = id
    try:
        targetUserList = bdata.insert("Boards", board)
        return {"response": "success", "board_id": id} 
    except:
        return {"response": "failure"}
        
    
@router.get("/list", response_class=JSONResponse)
async def read_items():
    boardlist = bdata.select('Boards', '*')
    print("Board list: " + str(len(boardlist)))
    for i in boardlist:
        print(i)
    return {"response": "success"}