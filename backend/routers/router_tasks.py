

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated, Optional
import sqlite3
import os
import secrets
import json
from ..modules import mod_users as UsersModule
from ..modules import mod_groups as GroupsModule
from ..modules import mod_messaging as MessagingModule
from ..modules import mod_tasks as TasksModule

###
###   Routers
###

router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
    dependencies=[Depends(UsersModule.get_token_header)],
    responses={404: {"description": "Not found"}},
)

router_ws = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)

###
###   Requests :: Create
###

class RouterRequest_CreateBoard(BaseModel):
    title: str
    handle:  Optional[str]

class RouterRequest_CreateColumn(BaseModel):
    title: str
    board_id: int
    position_x: int

class RouterRequest_CreateCard(BaseModel):
    title: str
    description: str
    column_id: int
    position_y: int
    color: str = Field(default="#579")

class RouterRequest_CreateSubtask(BaseModel):
    text: str
    card_id: int
    position: int

###
###   Requests :: Update
###

class RouterRequest_UpdateBoard(BaseModel):
    id: int
    title: Optional[str]
    owner_id: Optional[int]

class RouterRequest_UpdateColumn(BaseModel):
    id: int
    board_id: Optional[int]
    title: Optional[str]
    position_x: Optional[int]

class RouterRequest_UpdateCard(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    column_id: Optional[int]
    position_y: Optional[int]
    color: Optional[str]
    owner_id: Optional[int]
    deadline: Optional[int]
    attached_files: Optional[list[int]]

class RouterRequest_UpdateSubtask(BaseModel):
    id: int
    text: Optional[str]
    card_id: Optional[int]
    position: Optional[int]
    is_done: Optional[bool]

class RouterRequest_UpdateBoardUser(BaseModel):
    board_id: int
    user_id: int
    can_view: Optional[bool]
    can_edit: Optional[bool]

class RouterRequest_UpdateBoardGroup(BaseModel):
    board_id: int
    group_id: int
    can_view: Optional[bool]
    can_edit: Optional[bool]

class RouterRequest_UpdateCardUser(BaseModel):
    card_id: int
    user_id: int
    can_edit: Optional[bool]

###
###   Endpoints :: Create
###

@router.post("/create_board", response_class=JSONResponse)
async def post_create_board(createRequest: RouterRequest_CreateBoard, req: Request):
    if (not req.state.current_user):
        raise HTTPException(status_code=401, detail="Not logged in")
    print(createRequest.__dict__)
    newBoard = TasksModule.Create.board(
        TasksModule.Board_CreateRequest(**createRequest.__dict__, owner_id=req.state.current_user.id)
    )
    return TasksModule.Convert.board(newBoard)

@router.post("/create_column", response_class=JSONResponse)
async def post_create_column(createRequest: RouterRequest_CreateColumn, req: Request):
    if (not req.state.current_user):
        raise HTTPException(status_code=401, detail="Not logged in")
    print(createRequest.__dict__)
    newColumn = TasksModule.Create.column(
        TasksModule.Column_CreateRequest(**createRequest.__dict__)
    )
    return TasksModule.Convert.column(newColumn)

@router.post("/create_card", response_class=JSONResponse)
async def post_create_card(createRequest: RouterRequest_CreateCard, req: Request):
    if (not req.state.current_user):
        raise HTTPException(status_code=401, detail="Not logged in")
    print(createRequest.__dict__)
    newCard = TasksModule.Create.card(
        TasksModule.Card_CreateRequest(**createRequest.__dict__, owner_id=req.state.current_user.id)
    )
    return TasksModule.Convert.card(newCard)

@router.post("/create_subtask", response_class=JSONResponse)
async def post_create_subtask(createRequest: RouterRequest_CreateSubtask, req: Request):
    if (not req.state.current_user):
        raise HTTPException(status_code=401, detail="Not logged in")
    print(createRequest.__dict__)
    newSubtask = TasksModule.Create.subtask(
        TasksModule.Subtask_CreateRequest(**createRequest.__dict__)
    )
    return TasksModule.Convert.subtask(newSubtask)

###
###   Endpoints :: Select by ID
###

@router.get("/getBoardById/{id}")
async def get_board_by_id(id: int):
    return TasksModule.Select.oneBoard(TasksModule.Board.id == id)

@router.get("/getColumnById/{id}")
async def get_card_by_id(id: int):
    return TasksModule.Select.oneColumn(TasksModule.Column.id == id)

@router.get("/getCardById/{id}")
async def get_card_by_id(id: int):
    return TasksModule.Select.oneCard(TasksModule.Card.id == id)

@router.get("/getSubtaskById/{id}")
async def get_card_by_id(id: int):
    return TasksModule.Select.oneSubtask(TasksModule.Subtask.id == id)

#
#   Update
#

@router.post("/update/board")
async def post_update_board(updateRequest: RouterRequest_UpdateBoard):
    try:
        return TasksModule.Update.board(
            TasksModule.Board_UpdateRequest(**updateRequest.__dict__)
        )
    except:
        return

@router.post("/update/column")
async def post_update_column(updateRequest: RouterRequest_UpdateColumn):
    try:
        return TasksModule.Update.column(
            TasksModule.Column_UpdateRequest(**updateRequest.__dict__)
        )
    except:
        return

@router.post("/update/card")
async def post_update_column(updateRequest: RouterRequest_UpdateColumn):
    try:
        return TasksModule.Update.column(
            TasksModule.Column_UpdateRequest(**updateRequest.__dict__)
        )
    except:
        return

@router.post("/update/subtask")
async def post_update_column(updateRequest: RouterRequest_UpdateColumn):
    try:
        return TasksModule.Update.column(
            TasksModule.Column_UpdateRequest(**updateRequest.__dict__)
        )
    except:
        return

@router.post("/update/boardGroup")
async def post_update_board_group(updateRequest: RouterRequest_UpdateBoardGroup):
    try:
        return TasksModule.Update.boardUser(
            TasksModule.BoardGroup_UpdateRequest(**updateRequest.__dict__)
        )
    except:
        return

@router.post("/update/boardUser")
async def post_update_board_user(updateRequest: RouterRequest_UpdateBoardUser):
    try:
        return TasksModule.Update.boardUser(
            TasksModule.BoardUser_UpdateRequest(**updateRequest.__dict__)
        )
    except:
        return

@router.post("/update/cardUser")
async def post_update_card_user(updateRequest: RouterRequest_UpdateCardUser):
    try:
        return TasksModule.Update.cardUser(
            TasksModule.CardUser_UpdateRequest(**updateRequest.__dict__)
        )
    except:
        return

#
#   Delete
#