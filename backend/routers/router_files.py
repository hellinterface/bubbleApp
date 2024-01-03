
from fastapi import APIRouter, Depends, Request, HTTPException, File, UploadFile, Form
from fastapi.responses import PlainTextResponse, JSONResponse, FileResponse
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from ..modules import mod_users as UsersModule
from ..modules import mod_files as FilesModule

router = APIRouter(
    prefix="/api/files",
    tags=["files"],
    dependencies=[Depends(UsersModule.get_token_header)],
    responses={404: {"description": "Not found"}},
)

fileStoragePath = FilesModule.getFileStoragePath()

@router.get("/download/{id}", response_class=FileResponse)
async def get_by_id(id: str):
    print(id)
    result = FilesModule.Select.oneFile(FilesModule.File.id == id)
    if result == None:
        raise HTTPException(status_code=404)
    filepath = fileStoragePath + id
    return filepath

@router.get("/getFileById/{id}", response_class=JSONResponse)
async def get_file_by_id(id: int):
    return FilesModule.Select.oneFile(FilesModule.File.id == id)

@router.get("/getFolderById/{id}", response_class=JSONResponse)
async def get_folder_by_id(id: int):
    return FilesModule.Select.oneFolder(FilesModule.Folder.id == id)

class RouterRequest_UploadOptions(BaseModel):
    parent_folder_id: int
    users_can_view: list[int]
    users_can_edit: list[int]
    groups_can_view: list[int]
    groups_can_edit: list[int]
    unrestricted_view_access: bool
    unrestricted_edit_access: bool

@router.post("/upload", response_class=JSONResponse)
async def post_upload(upload_options: Annotated[RouterRequest_UploadOptions, Form()], files: list[UploadFile]):
    return_value = []
    for i in files:
        res = FilesModule.Create.file(
            FilesModule.File_CreateRequest(**upload_options.__dict__, file=i)
        )
        return_value.append(FilesModule.Convert.file(res))
    return return_value