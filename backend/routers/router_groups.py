

from fastapi import APIRouter, Depends, Request, Body, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from ..cores import core_users as UsersModule
from ..cores import core_groups as GroupsModule

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
    group_id: int

class RouterRequest_AddUserToGroup(BaseModel):
    user_handle: str
    group_id: int

class IDQuery(BaseModel):
    id: int = Field()

@router.post("/createGroup", response_class=JSONResponse)
async def post_create_group(createRequest: RouterRequest_CreateGroup, req: Request):
    if (not req.state.current_user):
        raise HTTPException(status_code=401, detail="Not logged in")
    print(createRequest.__dict__)
    newGroup = GroupsModule.Create.group(
        GroupsModule.Group_CreateRequest(**createRequest.__dict__, owner_id=req.state.current_user.id)
    )
    return GroupsModule.Convert.group(newGroup)
    try:    
        pass
    except:
        raise HTTPException(status_code=500, detail="Couldn't create group.")
        

@router.post("/createChannel", response_class=JSONResponse)
async def post_create_channel(createRequest: RouterRequest_CreateChannel, req: Request):
    if (not req.state.current_user):
        raise HTTPException(status_code=401, detail="Not logged in")
    newChannel = GroupsModule.Create.channel(
        GroupsModule.Channel_CreateRequest(**createRequest.__dict__, owner_id=req.state.current_user.id, is_primary=False)
    )
    return GroupsModule.Convert.channel(newChannel)
    try:    
        pass
    except:
        raise HTTPException(status_code=500, detail="Couldn't create channel.")
    
@router.get("/listGroups", response_class=JSONResponse)
async def get_list_groups():
    return GroupsModule.List.groups()

@router.get("/listChannels", response_class=JSONResponse)
async def get_list_channels():
    return GroupsModule.List.channel()

@router.get("/listMine", response_class=JSONResponse)
async def get_list_mine(req: Request):
    if (not req.state.current_user):
        raise HTTPException(status_code=401, detail="Not logged in")
    return GroupsModule.Select.groupsOfUser(req.state.current_user.id)

@router.get("/getGroupById/{id}", response_class=JSONResponse)
async def get_group_by_id(id: int):
    return GroupsModule.Select.oneGroup(GroupsModule.Group.id == id)

@router.post("/addUserToGroup", response_class=JSONResponse)
async def post_add_user_to_group(req: RouterRequest_AddUserToGroup):
    group = GroupsModule.Select.oneGroup(GroupsModule.Group.id == req.group_id)
    user = UsersModule.Select.oneUser(UsersModule.User.handle == req.user_handle)
    groupUser = GroupsModule.Create.groupUser(
        GroupsModule.GroupUser_CreateRequest(user_id=user.id, group_id=req.group_id)
        )
    #channel = GroupsModule.Select.oneChannel(GroupsModule.Channel.is_primary == True, GroupsModule.Channel.group_id == req.group_id)
    for channel in group.channels:
        channelUser = GroupsModule.Create.channelUser(
            GroupsModule.ChannelUser_CreateRequest(user_id=user.id, channel_id=channel.id)
            )
    return groupUser