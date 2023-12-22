
from fastapi import APIRouter, Depends, Request, status, Response, Body
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.exceptions import HTTPException
from datetime import timedelta
from ..modules import mod_users as UsersModule
from pydantic import BaseModel
from typing import Annotated
import datetime

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

class LoginData(BaseModel):
    email: str
    password_hash: str

@router.post("/login", response_class=JSONResponse)
async def post_login(login_data: Annotated[
        LoginData,
        Body(examples=[{
                    "email": "example@example.com",
                    "password_hash": "fake_password_hash"
                }])
    ], response: Response):
    """Эндпоинт получения токена пользователя."""
    print(login_data)
    targetUser = UsersModule.Select.oneUser(
        UsersModule.User.email == login_data.email, 
        UsersModule.User.password_hash == login_data.password_hash)
    if targetUser != None:
        access_token = UsersModule.create_token_for_user_id(targetUser.id)
        response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
        # response.set_cookie("access_token", access_token, samesite="none", secure=True)
        return response
    else:
        raise HTTPException(status_code=401, detail="Couldn't find user with specified credentials")

@router.post("/signup", response_class=JSONResponse)
async def get_create(signup_data: Annotated[
        UsersModule.User_CreateRequest,
        Body(examples=[{
                    "handle": "somehandle",
                    "visible_name": "SomeVisibleName",
                    "email": "example@example.com",
                    "password_hash": "fake_password_hash"
                }])
    ]):
    """Эндпоинт регистрации пользователя."""
    print(signup_data)
    created_user = UsersModule.Create.user(signup_data)
    access_token = UsersModule.create_token_for_user_id(created_user.id)
    return {"access_token": access_token, "token_type": "bearer"}
