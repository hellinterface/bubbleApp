
from fastapi import APIRouter, Depends, Request, status, Response, Body
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.exceptions import HTTPException
from datetime import timedelta
from ..modules import mod_users as MainModule
from pydantic import BaseModel
from typing import Annotated
import datetime

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post("/login", response_class=JSONResponse)
async def post_login(login_data: Annotated[
        MainModule.LoginData,
        Body(examples=[{
                    "email": "example@example.com",
                    "password_hash": "fake_password_hash"
                }])
    ], response: Response):
    """Эндпоинт получения токена пользователя."""
    print(login_data)
    targetUser = MainModule.login(login_data)
    if targetUser != None:
        access_token = MainModule.create_token_for_user_id(targetUser.id)
        # response.set_cookie(key="access_token", value=access_token)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        return {"response": "failure"}

@router.post("/signup", response_class=JSONResponse)
async def get_create(signup_data: Annotated[
        MainModule.SignupData,
        Body(examples=[{
                    "handle": "somehandle",
                    "visible_name": "SomeVisibleName",
                    "email": "example@example.com",
                    "password_hash": "fake_password_hash"
                }])
    ]):
    """Эндпоинт регистрации пользователя."""
    print(signup_data)
    created_user = MainModule.create_user(signup_data)
    access_token = MainModule.create_token_for_user_id(created_user.id)
    return {"access_token": access_token, "token_type": "bearer"}
