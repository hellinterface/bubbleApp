
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import config
from . import requests
from .routers import router_files, router_users, router_auth, router_groups, router_messaging, router_meetings, router_tasks

app = FastAPI()
app.include_router(router_files.router)
app.include_router(router_users.router)
app.include_router(router_auth.router)
app.include_router(router_groups.router)
app.include_router(router_messaging.router)
app.include_router(router_messaging.router_ws)
app.include_router(router_meetings.router)
app.include_router(router_meetings.router_ws)
app.include_router(router_tasks.router)
app.include_router(router_tasks.router_ws)

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

    "https://localhost:8080",
    "https://localhost:8000",
    "https://localhost:7000",
    "https://localhost:7070",
    "https://localhost",
    "https://127.0.0.1:8080",
    "https://127.0.0.1:8000",
    "https://127.0.0.1:7000",
    "https://127.0.0.1:7070",
    "https://127.0.0.1",
]

#origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def setup():
    from .cores import core_files, core_users, core_groups, core_messaging, core_tasks
    ###   Admin
    ###################################################################################################
    admin = core_users.RawSelect.oneUser(core_users.User.id == 1)
    print("#################################################################################")
    print(admin)
    print("#################################################################################")
    if (admin == None):
        # Password = "admin"
        admin = core_users.Create.user(requests.User_CreateRequest(handle="ADMIN", visible_name="ADMIN", email="admin@bubble.net", password_hash="8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"))
    if (admin.is_admin == False):
        admin = core_users.Update.user(requests.User_UpdateRequest(id=admin.id, is_admin=True))

    ###   $SYSTEM folder & permanent files
    ###################################################################################################
    systemFolder = core_files.RawSelect.select_one(core_files.Folder, core_files.Folder.id == 1)
    print("########################################################################")
    print(systemFolder)
    print("########################################################################")
    if (systemFolder == None): 
        systemFolder = core_files.Create.folder(core_files.Folder_CreateRequest(title="$SYSTEM", owner_id=1))
    filesInsideSystemFolder = core_files.RawSelect.select(core_files.File, core_files.File.parent_folder_id == systemFolder.id)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(filesInsideSystemFolder)
    print(len(filesInsideSystemFolder))
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    if len(filesInsideSystemFolder) == 0:
        permanentFilesPath = core_files.getPermanentFilesPath()
        files = [f for f in os.listdir(permanentFilesPath) if os.path.isfile(os.path.join(permanentFilesPath, f))]
        for i in files:
            path = os.path.join(permanentFilesPath, i)
            core_files.Create.fileForExisting(core_files.File_CreateRequestForExisting(
                title=i, owner_id=1, parent_folder_id=1, unrestricted_view_access=True, filepath=path
            ))


setup()

if config.PREPOPULATE:
    from .cores import core_files, core_users, core_groups, core_messaging, core_tasks
    for (key, value) in config.PREPOPULATE_USERS.items():
        print(key, value)
        if (core_users.RawSelect.oneUser(core_users.User.id == key) == None):
            core_users.Create.user(value)
    for (key, value) in config.PREPOPULATE_GROUPS.items():
        if (core_groups.RawSelect.oneGroup(core_groups.Group.id == key) == None):
            core_groups.Create.group(value)
