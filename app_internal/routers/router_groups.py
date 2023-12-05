

from fastapi import APIRouter, Depends, Request, Body, HTTPException
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated
from ..modules import mod_users as UsersModule
from ..modules import mod_groups as GroupsModule

router = APIRouter(
    prefix="/api/groups",
    tags=["groups"],
    dependencies=[Depends(UsersModule.get_token_header)],
    responses={404: {"description": "Not found"}},
)

class IDQuery(BaseModel):
    id: int = Field()

@router.post("/create_group", response_class=JSONResponse)
async def post_create_group(creationRequest: GroupsModule.Group_CreateRequest, request: Request):
    print("==============================")
    print(creationRequest)
    print("==============================")
    newGroup = GroupsModule.create_group(creationRequest, request.state.current_user)
    try:
        return {"response": "success", "group_id": newGroup.id} 
    except:
        return {"response": "failure"}
        
    
@router.get("/list_groups", response_class=JSONResponse)
async def get_list_groups():
    res = GroupsModule.list_groups()
    print("Group list: " + str(len(res)))
    for i in res:
        print(i)
    return res

@router.get("/list_channels", response_class=JSONResponse)
async def get_list_channels():
    res = GroupsModule.list_channels()
    print("Channel list: " + str(len(res)))
    for i in res:
        print(i)
    return res

@router.get("/list_mine", response_class=JSONResponse)
async def get_list_mine(req: Request):
    res = GroupsModule.list_mine(req.state.current_user)
    print("Group list: " + str(len(res)))
    print(res)
    return res

@router.post("/get_by_id", response_class=JSONResponse)
async def post_get_by_id(req: Annotated[IDQuery, Body(examples=[{"id": 128}])]):
    res = GroupsModule.select_groups(GroupsModule.Group.id == req.id)
    print(res)
    if len(res) > 0:
        return res[0]
    else:
        return {"response": "failure"}

class Request_AddUserToGroup(BaseModel):
    user_handle: str
    group_id: int

@router.post("/add_user_to_group", response_class=JSONResponse)
async def post_add_user_to_group(req: Request_AddUserToGroup):
    user = UsersModule.select_users(UsersModule.User.handle == req.user_handle)
    group = GroupsModule.select_groups(GroupsModule.Group.id == req.group_id)
    if (len(user) <= 0) or (len(group) <= 0):
        return HTTPException(status_code=400, detail="Invalid request")
    return GroupsModule.add_user_to_group(user=user[0], group=group[0])