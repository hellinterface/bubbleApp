
from fastapi import APIRouter, Depends, Request
from fastapi.responses import PlainTextResponse, JSONResponse, FileResponse
from pydantic import BaseModel, Field
import sqlite3
import os
import secrets
import json
from ..bdata import BData

router = APIRouter(
    prefix="/api/files",
    tags=["files"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

class File(BaseModel):
    id: str = Field(allow_mutation=False, bdata_unique=True)
    filename: str = Field()
    date_added: int = Field()
    date_modified: int = Field()
    owner_id: str = Field()
    lastmodify_id: str = Field()
    users_can_read: list[str] = Field(bdata_type=str)
    users_can_edit: list[str] = Field(bdata_type=str)
    share_link: str = Field()
    
class Folder(BaseModel):
    id: str = Field(allow_mutation=False, bdata_unique=True)
    title: str = Field()
    contents: list[str] = Field(bdata_type=str)
    owner_id: str = Field()
    lastmodify_id: str = Field()
    users_can_read: list[str] = Field(bdata_type=str)
    users_can_edit: list[str] = Field(bdata_type=str)
    max_size: int = Field()


def file_factory(cursor, row):
    # print(u"current directory: %s" % os.getcwd())
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    print(d)
    d['users_can_read'] = ['*'] #json.loads(d['users_can_read'])
    d['users_can_edit'] = []    #json.loads(d['users_can_edit'])
    fileObject = File(**d)
    return fileObject

DIRNAME = os.path.dirname(os.path.dirname(__file__))

DB_FILES_PATH = DIRNAME + '\\data\\files_db.db'
print(DB_FILES_PATH)
bdata = BData(DB_FILES_PATH, file_factory)

filestorage_path = DIRNAME + "\\data\\file_storage\\"

@router.get("/list", response_class=JSONResponse)
async def read_items():
    filelist = bdata.select('Files', '*')
    print("filelist: " + str(len(filelist)))
    for i in filelist:
        print(i)
    return {"response": "success", "userlist": filelist}

@router.get("/get/{req_id}", response_class=FileResponse)
async def get_by_id(req_id: str):
    print(req_id)
    resultList = bdata.select('Files', {'id': req_id})
    print(resultList)
    if len(resultList) == 0:
        return {"response": "failure"}
    filepath = filestorage_path + resultList[0].filename
    return filepath


# ----------------------------------------------------------------------------

permanent_files = [
    File(id="permanent_avatar1", filename="permanent_avatar1.png", date_added=0, date_modified=0, owner_id="NULL", lastmodify_id="NULL", users_can_read=['*'], users_can_edit=[], share_link=""),
    File(id="permanent_avatar2", filename="permanent_avatar2.png", date_added=0, date_modified=0, owner_id="NULL", lastmodify_id="NULL", users_can_read=['*'], users_can_edit=[], share_link=""),
    File(id="permanent_avatar3", filename="permanent_avatar3.png", date_added=0, date_modified=0, owner_id="NULL", lastmodify_id="NULL", users_can_read=['*'], users_can_edit=[], share_link=""),
]

tables = bdata.get_tables()
print("Tables:")
print(tables)
if ("Files" not in tables):
    bdata.create("Files", File)
    for file in permanent_files:
        bdata.insert("Files", file)
if ("Folders" not in tables):
    bdata.create("Folders", Folder)