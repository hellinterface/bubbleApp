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

from .services import svc_users
from .services import svc_groups

app = FastAPI()
app.include_router(svc_users.router)
app.include_router(svc_groups.router)

@app.get("/api/test")
async def list_users():
    return {"testing": "ok"}
