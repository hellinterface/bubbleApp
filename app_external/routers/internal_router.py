
from fastapi import APIRouter, Depends, Request, HTTPException, status, Response, Cookie
from fastapi.responses import PlainTextResponse, JSONResponse
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Annotated
import httpx
from .. import exceptions

from ..bbmodules import userapi

router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)

async def getCurrentUser(access_token: str):
    return await userapi.get_current_user(access_token)

@router.get("/users/list")
async def list_users():
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get('http://127.0.0.1:8080/api/users/list')
            return r.read()
        except:
            return "Error..."

@router.get("/users/me")
async def get_current_user_information(access_token: Annotated[str | None, Cookie()] = None):
    '''Get JSON information about the current user.'''
    print(access_token)
    data = await getCurrentUser(access_token)
    print(data)
    return data

@router.post("/users/edit")
async def edit_current_user_information(request: Request, access_token: Annotated[str | None, Cookie()] = None):
    '''Edit current user's information.'''
    requestBody = await request.json()
    print(requestBody)
    print(access_token)
    await getCurrentUser(access_token)
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post('http://127.0.0.1:8080/api/users/edit', json=requestBody)
            return r.read()
        except:
            return "Error..."


def create_token_for_user_id(user_id: str) -> str:
    print("DAAAAAAAAAAAAAAAAAAAAAAAAAAAAATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print(user_id)
    print("DAAAAAAAAAAAAAAAAAAAAAAAAAAAAATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    access_token_expires = timedelta(days=userapi.ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = userapi.create_access_token(
        data={"user_id": user_id}, expires_delta=access_token_expires
    )
    return access_token

@router.post("/users/signup", response_class=JSONResponse)
async def signup_post(request: Request, response: Response):
    requestBody = await request.json()
    print(requestBody)
    async with httpx.AsyncClient() as client:
        try:
            r = await client.post('http://127.0.0.1:8080/api/users/signup', json=requestBody)
            backendOutput = r.json()
            if (backendOutput["response"] == "success"):
                access_token = create_token_for_user_id(backendOutput["user_id"])
                response.set_cookie(key="access_token", value=access_token)
                return {"access_token": access_token, "token_type": "bearer"}
            else:   
                raise HTTPException(status_code=400, detail="Incorrect username or password")
            return 
        except:
            return "Error..."


@router.post("/users/login", response_model=userapi.Token)
async def login_for_access_token(request: Request, response: Response):
    failException = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    request = await request.json()
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(request)
    try:
        user_id = await userapi.authenticate_user(request["email"], request["password_hash"])
    except:
        raise failException
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$ AUTHED")
    if not user_id:
        raise failException
    access_token = create_token_for_user_id(user_id)
    response.set_cookie(key="access_token", value=access_token)
    return {"access_token": access_token, "token_type": "bearer"}