
from fastapi import APIRouter, Depends, Request, HTTPException, File, UploadFile, Form
from fastapi.responses import PlainTextResponse, JSONResponse, FileResponse, StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, Annotated
from ..cores import core_users as UsersModule
from ..cores import core_files as FilesModule
from .. import models
import json
import magic

router = APIRouter(
    prefix="/api/files",
    tags=["files"],
    dependencies=[Depends(UsersModule.get_token_header)],
    responses={404: {"description": "Not found"}},
)

fileStoragePath = FilesModule.getFileStoragePath()

@router.get("/download/{id}", response_class=StreamingResponse)
async def get_by_id(id: int, req: Request):
    print(id)
    userCanView = FilesModule.getUserPermissionsOfFile(user_id=req.state.current_user.id, file_id=id)["can_view"]
    result = FilesModule.Select.oneFile(FilesModule.File.id == id)
    if result == None:
        raise HTTPException(status_code=404)
    filepath = fileStoragePath + "\\" + str(id)
    print(filepath)
    def iterfile():
        with open(filepath, mode="rb") as file_like:
            yield from file_like
    mime = magic.Magic(mime=True)
    mimetype = mime.from_file(filepath)
    print(mimetype)
    #return FileResponse(path=filepath, media_type=mimetype)
    return StreamingResponse(iterfile(), media_type=mimetype, headers={"Content-Disposition": "inline; filename="+result.title})
    #return filepath

@router.get("/getFileById/{id}", response_class=JSONResponse, response_model=models.Output_File)
async def get_file_by_id(id: int):
    res = FilesModule.Select.oneFile(FilesModule.File.id == id)
    if res == None: raise HTTPException(status_code=404)
    return res

@router.get("/getFolderById/{id}", response_class=JSONResponse, response_model=models.Output_Folder)
async def get_folder_by_id(id: int, req: Request):
    userCanView = FilesModule.getUserPermissionsOfFolder(user_id=req.state.current_user.id, folder_id=id)["can_view"]
    if (userCanView == False): raise HTTPException(status_code=403)
    res = FilesModule.Select.oneFolder(FilesModule.Folder.id == id)
    if res == None: raise HTTPException(status_code=404)
    return res

@router.get("/getFolderContents/{id}", response_class=JSONResponse, response_model=models.Output_FolderContents)
async def get_folder_contents(id: int, req: Request):
    userCanView = FilesModule.getUserPermissionsOfFolder(user_id=req.state.current_user.id, folder_id=id)["can_view"]
    if (userCanView == False): raise HTTPException(status_code=403)
    return FilesModule.getFolderContents(id)

@router.get("/getFolderByLink/{link}", response_class=JSONResponse, response_model=models.Output_Folder)
async def get_folder_by_link(link: str, req: Request):
    res = FilesModule.Select.oneFolder(FilesModule.Folder.share_link == link)
    if res == None: raise HTTPException(status_code=404)
    return res

class RouterRequest_UploadOptions(BaseModel):
    parent_folder_id: int
    users_can_view: Optional[list[int]] = []
    users_can_edit: Optional[list[int]] = []
    groups_can_view: Optional[list[int]] = []
    groups_can_edit: Optional[list[int]] = []
    unrestricted_view_access: Optional[bool] = False
    unrestricted_edit_access: Optional[bool] = False
    inheritView: Optional[bool] = False
    inheritEdit: Optional[bool] = False

@router.post("/upload", response_class=JSONResponse)
async def post_upload(upload_options: Annotated[str, Form()], files: Annotated[list[UploadFile], Form()], req: Request):
    #RouterRequest_UploadOptions
    print("####################################################")
    print(upload_options)
    print(files)
    upload_options = RouterRequest_UploadOptions(**(json.loads(upload_options)))
    print(upload_options)
    print("####################################################")
    return_value = []
    for i in files:
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        res = FilesModule.Create.file(
            FilesModule.File_CreateRequest(**upload_options.__dict__, file=i, owner_id=req.state.current_user.id, title=i.filename)
        )
        return_value.append(FilesModule.Convert.file(res))
    return return_value
    
class RouterRequest_CreateFolder(BaseModel):
    title: str
    parent_folder_id: int

@router.post("/createFolder", response_class=JSONResponse)
async def post_upload(upload_options: RouterRequest_CreateFolder, req: Request):
    userCanEdit = FilesModule.getUserPermissionsOfFolder(user_id=req.state.current_user.id, folder_id=upload_options.parent_folder_id)["can_edit"]
    if (userCanEdit == False): raise HTTPException(status_code=403)
    return_value = FilesModule.Create.folder(
        FilesModule.Folder_CreateRequest(**upload_options.__dict__, owner_id=req.state.current_user.id, inheritEdit=True, inheritView=True)
    )
    return return_value