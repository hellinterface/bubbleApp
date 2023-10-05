from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
import os
import json
import sqlite3
import secrets
from typing import Annotated
from pydantic import BaseModel
import httpx

from .svc_users import svc_users

app = FastAPI()
app.include_router(svc_users.router)

@app.get("/api/test")
async def list_users():
    return {"testing": "ok"}
