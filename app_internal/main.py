from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import sqlite3
import secrets
from typing import Annotated
from pydantic import BaseModel
import httpx

from .routers import router_users, router_auth #, router_groups, router_files

app = FastAPI()
app.include_router(router_users.router)
app.include_router(router_auth.router)
#app.include_router(router_groups.router)
#app.include_router(router_files.router)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:7000",
    "http://localhost:7070",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/test")
async def get_test():
    return {"testing": "ok"}
