from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import router_users, router_auth, router_groups, router_messaging, router_meetings #  router_files

app = FastAPI()
app.include_router(router_users.router)
app.include_router(router_auth.router)
app.include_router(router_groups.router)
app.include_router(router_messaging.router)
app.include_router(router_messaging.router_ws)
app.include_router(router_meetings.router)
app.include_router(router_meetings.router_ws)
#app.include_router(router_files.router)

origins = [
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:7000",
    "http://localhost:7070",
    "http://localhost",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:7000",
    "http://127.0.0.1:7070",
    "http://127.0.0.1",
]

#origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)