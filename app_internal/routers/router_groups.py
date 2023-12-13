

from fastapi import APIRouter, Depends, Request, Body, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from ..modules import mod_users as UsersModule
from ..modules import mod_groups as GroupsModule

router = APIRouter(
    prefix="/api/groups",
    tags=["groups"],
    dependencies=[Depends(UsersModule.get_token_header)],
    responses={404: {"description": "Not found"}},
)

class RouterRequest_CreateGroup(BaseModel):
    title: str
    handle: str

class RouterRequest_CreateChannel(BaseModel):
    title: str
    handle: Optional[str]

class RouterRequest_AddUserToGroup(BaseModel):
    user_id: int
    group_id: int

class IDQuery(BaseModel):
    id: int = Field()

@router.post("/create_group", response_class=JSONResponse)
async def post_create_group(req: RouterRequest_CreateGroup, request: Request):
    if (not req.state.current_user):
        raise HTTPException(status_code=401, detail="Not logged in")
    try:    
        newGroup = GroupsModule.Create.group(
            GroupsModule.Group_CreateRequest(**req.__dict__, owner_id=request.state.current_user)
        )
        return GroupsModule.Convert.group(newGroup)
    except:
        raise HTTPException(detail="Couldn't create group.")
        

@router.post("/create_channel", response_class=JSONResponse)
async def post_create_channel(req: RouterRequest_CreateChannel, request: Request):
    if (not req.state.current_user):
        raise HTTPException(status_code=401, detail="Not logged in")
    try:    
        newChannel = GroupsModule.Create.channel(
            GroupsModule.Chanel_CreateRequest(**req.__dict__, owner_id=request.state.current_user)
        )
        return GroupsModule.Convert.channel(newChannel)
    except:
        raise HTTPException(detail="Couldn't create channel.")
    
@router.get("/list_groups", response_class=JSONResponse)
async def get_list_groups():
    return GroupsModule.List.groups()

@router.get("/list_channels", response_class=JSONResponse)
async def get_list_channels():
    return GroupsModule.List.channel()

@router.get("/list_mine", response_class=JSONResponse)
async def get_list_mine(req: Request):
    if (not req.state.current_user):
        raise HTTPException(status_code=401, detail="Not logged in")
    return GroupsModule.Select.groupsOfUser(req.state.current_user.id)

@router.post("/get_by_id", response_class=JSONResponse)
async def post_get_by_id(req: Annotated[IDQuery, Body(examples=[{"id": 128}])]):
    return GroupsModule.Select.oneGroup(GroupsModule.Group.id == req.id)

@router.post("/add_user_to_group", response_class=JSONResponse)
async def post_add_user_to_group(req: RouterRequest_AddUserToGroup):
    return GroupsModule.Create.groupUser(
        GroupsModule.GroupUser_CreateRequest(**req.__dict__)
        )
