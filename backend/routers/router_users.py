
from fastapi import APIRouter, Depends, Request, status, Response, Body
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.exceptions import HTTPException
from datetime import timedelta
from ..modules import mod_users as UsersModule
from pydantic import BaseModel
from typing import Annotated, Optional
import datetime

class Message(BaseModel):
    message: str

class RouterRequest_UpdateUser(BaseModel):
    handle: Optional[str]
    visible_name: Optional[str]
    email: Optional[str]
    password_hash: Optional[str]
    avatar_fileid: Optional[int]
    bio: Optional[str]
    contacts: Optional[list[int]]
    notifications: Optional[list[dict]]
    events: Optional[list[int]]
    fav_users: Optional[list[int]]
    fav_groups: Optional[list[int]]

    
class AdminRequest_UpdateUser(BaseModel):
    # it could use the UsersModule request object directly i think
    directly: bool = True

class AdminRequest_DeleteUser(BaseModel):
    id: int

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
    dependencies=[Depends(UsersModule.get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/list", response_class=JSONResponse,
    response_model=list[UsersModule.Output_User],
    responses={
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": [{"id": 128, "handle": "somehandle", "other": "stuff..."}, "..."]
                }
            },
        },
    }
)
async def get_list():
    """Получение списка всех пользователей."""
    userlist = UsersModule.List.users()
    return userlist

@router.get("/getById/{user_id}", response_class=JSONResponse,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {"id": 128, "handle": "somehandle", "other": "stuff..."}
                }
            },
        },
    })
async def get_by_id(user_id: int):
    """Получение пользователя, которому соответствует ID, указанный в поле id."""
    targetUser = UsersModule.Select.oneUser(UsersModule.User.id == user_id)
    print(targetUser)
    if targetUser != None:
        return UsersModule.Convert.userToPublic(targetUser)
    else:
        raise HTTPException(status_code=404, detail="Couldn't find user")

        
@router.get("/getByHandle/{handle}", response_class=JSONResponse,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {"id": 128, "handle": "somehandle", "other": "stuff..."}
                }
            },
        },
    })
async def get_by_handle(handle: str):
    """Получение пользователя, которому соответствует ID, указанный в поле id."""
    targetUser = UsersModule.Select.oneUser(UsersModule.User.handle == handle)
    print(targetUser)
    if targetUser != None:
        return UsersModule.Convert.userToPublic(targetUser)
    else:
        raise HTTPException(status_code=404, detail="Couldn't find user")

@router.get("/me")
async def get_current_user(req: Request):
    """Получение объекта текущего пользователя (на основе токена из cookie)."""
    print(req.state)
    try:
        return req.state.current_user
    except:
        raise HTTPException(status_code=404, detail="Couldn't find user")

@router.post("/update")
async def post_update(updateRequest: RouterRequest_UpdateUser, req: Request):
    try:
        return UsersModule.Update.user(
            UsersModule.User_UpdateRequest(**updateRequest.__dict__, id=req.state.current_user.id)
        )
    except:
        return

"""
failException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)
    

@router.post("/edit", response_class=JSONResponse)
async def post_edit(req: dict):
    # dbc = getDBConnection()
    # cur = dbc.cursor()
    # cur.execute("UPDATE Users SET ? WHERE id = ?")
    print(req)
    for key,value in req.items():
        print(f" --- {key}: {value}")
    
"""

@router.get("/test")
async def test():
    dt = datetime.datetime.now()
    return dt.strftime("%Y%m%d")
# ----------------------------------------------------------------------------
