
from fastapi import APIRouter, Depends, Request, status, Response
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.exceptions import HTTPException
from datetime import timedelta
from ..modules import mod_users as MainModule
from pydantic import BaseModel
import datetime

router = APIRouter(
    prefix="/api/auth",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.post("/login", response_class=JSONResponse)
async def post_login(req: MainModule.LoginData, response: Response):
    print(req)
    targetUser = MainModule.login(req)
    if targetUser != None:
        access_token = MainModule.create_token_for_user_id(targetUser.id)
        # response.set_cookie(key="access_token", value=access_token)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        return {"response": "failure"}

@router.post("/signup", response_class=JSONResponse)
async def get_create(signup_data: MainModule.SignupData): #new_user: User
    print(signup_data)
    created_user = MainModule.create_user(signup_data)
    return {"response": "success", "user_id": created_user.id} 
