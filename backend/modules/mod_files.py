
from pydantic import BaseModel, Field
import os
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, JSON, Column, Session, select
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, date
from time import mktime
from fastapi import File as FastAPI_File
from fastapi import UploadFile as FastAPI_UploadFile
from ..modules import mod_users as UsersModule
from ..modules import mod_groups as GroupsModule
from ..modules import exceptions

###
###   Entites :: Output
###

class Output_UserEntry(BaseModel):
    user_information: UsersModule.PublicOutput_User
    can_view: bool
    can_edit: bool
    
class Output_GroupEntry(BaseModel):
    group_information: GroupsModule.Output_Group
    can_view: bool
    can_edit: bool

class Output_File(BaseModel):
    id: int
    title: str
    date_added: int
    date_modified: int
    owner: UsersModule.PublicOutput_User
    user_modified: UsersModule.PublicOutput_User
    share_link: str
    parent_folder_id: Optional[int]
    users: list[Output_UserEntry]
    groups: list[Output_GroupEntry]

class Output_Folder(BaseModel):
    id: int
    title: str
    owner: UsersModule.PublicOutput_User
    max_size: int
    share_link: str
    parent_folder_id: Optional[int]
    users: list[Output_UserEntry]
    groups: list[Output_GroupEntry]

###
###   Entites :: SQL/Raw
###

class File(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field()
    date_added: int = Field()
    date_modified: int = Field()
    owner_id: int = Field()
    user_modified_id: int = Field()
    share_link: str = Field()
    parent_folder_id: int = Field()
    unrestricted_view_access: bool = Field(default=False)
    unrestricted_edit_access: bool = Field(default=False)
    
class Folder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field()
    max_size: int = Field()
    owner_id: int = Field()
    share_link: str = Field()
    parent_folder_id: Optional[int] = Field()
    unrestricted_view_access: bool = Field(default=False)
    unrestricted_edit_access: bool = Field(default=False)
    # is_root_folder: bool = Field(default=False)

class FolderUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field()
    folder_id: int = Field()
    can_view: bool = Field()
    can_edit: bool = Field()

class FileUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field()
    file_id: int = Field()
    can_view: bool = Field()
    can_edit: bool = Field()

class FolderGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field()
    folder_id: int = Field()
    can_view: bool = Field()
    can_edit: bool = Field()

class FileGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field()
    file_id: int = Field()
    can_view: bool = Field()
    can_edit: bool = Field()


# GROUP/CHANNEL ACCESS I THINK

###
###   Requests :: Create
###

class File_CreateRequest(BaseModel):
    title: str
    owner_id: int
    parent_folder_id: int
    users_can_view: list[int] = Field(default=[])
    users_can_edit: list[int] = Field(default=[])
    groups_can_view: list[int] = Field(default=[])
    groups_can_edit: list[int] = Field(default=[])
    unrestricted_view_access: bool = Field(default=False)
    unrestricted_edit_access: bool = Field(default=False)
    file: FastAPI_File

class File_CreateRequestForExisting(BaseModel):
    title: str
    owner_id: int
    parent_folder_id: int
    users_can_view: list[int] = Field(default=[])
    users_can_edit: list[int] = Field(default=[])
    groups_can_view: list[int] = Field(default=[])
    groups_can_edit: list[int] = Field(default=[])
    unrestricted_view_access: bool = Field(default=False)
    unrestricted_edit_access: bool = Field(default=False)
    filename: str

class Folder_CreateRequest(BaseModel):
    title: str
    max_size: Optional[int]
    owner_id: int
    parent_folder_id: Optional[int]
    users_can_view: list[int] = Field(default=[])
    users_can_edit: list[int] = Field(default=[])
    groups_can_view: list[int] = Field(default=[])
    groups_can_edit: list[int] = Field(default=[])
    unrestricted_view_access: bool = Field(default=False)
    unrestricted_edit_access: bool = Field(default=False)

class FolderUser_CreateRequest(BaseModel):
    folder_id: int
    user_id: int
    can_view: bool
    can_edit: bool

class FileUser_CreateRequest(BaseModel):
    file_id: int
    user_id: int
    can_view: bool
    can_edit: bool

class FolderGroup_CreateRequest(BaseModel):
    folder_id: int
    group_id: int
    can_view: bool
    can_edit: bool
    
class FileGroup_CreateRequest(BaseModel):
    file_id: int
    group_id: int
    can_view: bool
    can_edit: bool

###
###   Requests :: Modify
###

class File_UpdateRequest(BaseModel):
    title: str
    owner_id: Optional[int]
    parent_folder_id: Optional[int]
    users_can_view: Optional[list[int]]
    users_can_edit: Optional[list[int]]
    groups_can_view: Optional[list[int]]
    groups_can_edit: Optional[list[int]]
    unrestricted_view_access: Optional[bool]
    unrestricted_edit_access: Optional[bool]
    file: FastAPI_File

class Folder_UpdateRequest(BaseModel):
    title: Optional[str]
    max_size: Optional[int]
    owner_id: Optional[int]
    parent_folder_id: Optional[int]
    users_can_view: Optional[list[int]]
    users_can_edit: Optional[list[int]]
    groups_can_view: Optional[list[int]]
    groups_can_edit: Optional[list[int]]
    unrestricted_view_access: Optional[bool]
    unrestricted_edit_access: Optional[bool]

class FolderUser_UpdateRequest(BaseModel):
    folder_id: int
    user_id: int
    can_view: Optional[bool]
    can_edit: Optional[bool]

class FileUser_UpdateRequest(BaseModel):
    file_id: int
    user_id: int
    can_view: Optional[bool]
    can_edit: Optional[bool]

class FolderGroup_UpdateRequest(BaseModel):
    folder_id: int
    group_id: int
    can_view: Optional[bool]
    can_edit: Optional[bool]

class FileGroup_UpdateRequest(BaseModel):
    file_id: int
    group_id: int
    can_view: Optional[bool]
    can_edit: Optional[bool]

###
###   SQL Database Engine
###

DIRNAME = os.path.dirname(os.path.dirname(__file__))
DB_PATH = DIRNAME + '\\data\\db_files.db'
print(DB_PATH)
sqlite_url = f"sqlite:///{DB_PATH}"
engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)

def getFileStoragePath():
    return DIRNAME + "\\data\\file_storage"

def getPermanentFilesPath():
    return DIRNAME + "\\data\\permanent_files"

###
###   Data :: Convert
###

class Convert:
    @staticmethod
    def userEntry(user: FolderUser|FileUser) -> Output_UserEntry:
        user = UsersModule.RawSelect.oneUser(UsersModule.User.id == user.user_id)
        user_publicInfo = UsersModule.convertUserToPublic(user)
        return Output_UserEntry(user_information=user_publicInfo, can_view=user.can_view, can_edit=user.can_edit)
    @staticmethod
    def file(file: File) -> Output_File:
        res = Output_File(**file.__dict__)
        res.owner = UsersModule.Convert.userToPublic(
            UsersModule.RawSelect.oneUser(UsersModule.User.id == file.owner_id)
        )
        res.user_modified = UsersModule.Convert.userToPublic(
            UsersModule.RawSelect.oneUser(UsersModule.User.id == file.user_modified_id)
        )
        return res
    @staticmethod
    def folder(folder: Folder) -> Output_Folder:
        res = Output_Folder(**folder.__dict__)
        res.owner = UsersModule.Convert.userToPublic(
            UsersModule.RawSelect.oneUser(UsersModule.User.id == folder.owner_id)
        )
        res.user_modified = UsersModule.Convert.userToPublic(
            UsersModule.RawSelect.oneUser(UsersModule.User.id == folder.user_modified_id)
        )
        return res

###
###   Data :: Create
###

class Create:
    @staticmethod
    def file(request: File_CreateRequest) -> File:
        currentTimestamp = mktime(datetime.now().timetuple())
        toCreate = File(
            title=request.title,
            owner_id=request.owner_id,
            user_modified_id=request.owner_id,
            date_added=currentTimestamp,
            date_modified=currentTimestamp,
            unrestricted_view_access=request.unrestricted_view_access,
            unrestricted_edit_access=request.unrestricted_edit_access,
            parent_folder_id=request.parent_folder_id
        )
        print(toCreate)
        with Session(engine) as session:
            session.add(toCreate)
            session.commit()
            session.refresh(toCreate)

        userIdList = set()
        for i in request.users_can_view: userIdList.add(i)
        for i in request.users_can_edit: userIdList.add(i)
        for i in userIdList:
            can_view = False
            can_edit = False
            if i in request.users_can_view: can_view = True
            if i in request.users_can_edit: can_edit = True
            Create.fileUser(FileUser_CreateRequest(file_id=toCreate.id, user_id=i, can_view=can_view, can_edit=can_edit))

        groupIdList = set()
        for i in request.groups_can_view: groupIdList.add(i)
        for i in request.groups_can_edit: groupIdList.add(i)
        for i in groupIdList:
            can_view = False
            can_edit = False
            if i in request.groups_can_view: can_view = True
            if i in request.groups_can_edit: can_edit = True
            Create.fileGroup(FileGroup_CreateRequest(file_id=toCreate.id, group_id=i, can_view=can_view, can_edit=can_edit))

        try:
            with open(f"{getFileStoragePath}\\{toCreate.id}", 'wb') as f:
                while contents := request.file.file.read(1024 * 1024 * 64): # 64 MB chunks
                    f.write(contents)
                f.close()
        except:
            print('oops')
        finally:
            request.file.file.close()
            # TRY TO WRITE AN ACTUAL FILE FROM request.file

        return toCreate
    @staticmethod
    def fileForExisting(request: File_CreateRequestForExisting) -> File:
        currentTimestamp = mktime(datetime.now().timetuple())
        toCreate = File(
            title=request.title,
            owner_id=request.owner_id,
            user_modified_id=request.owner_id,
            date_added=currentTimestamp,
            date_modified=currentTimestamp,
            unrestricted_view_access=request.unrestricted_view_access,
            unrestricted_edit_access=request.unrestricted_edit_access,
            parent_folder_id=request.parent_folder_id
        )
        print(toCreate)
        with Session(engine) as session:
            session.add(toCreate)
            session.commit()
            session.refresh(toCreate)

        userIdList = set()
        for i in request.users_can_view: userIdList.add(i)
        for i in request.users_can_edit: userIdList.add(i)
        for i in userIdList:
            can_view = False
            can_edit = False
            if i in request.users_can_view: can_view = True
            if i in request.users_can_edit: can_edit = True
            Create.fileUser(FileUser_CreateRequest(file_id=toCreate.id, user_id=i, can_view=can_view, can_edit=can_edit))

        groupIdList = set()
        for i in request.groups_can_view: groupIdList.add(i)
        for i in request.groups_can_edit: groupIdList.add(i)
        for i in groupIdList:
            can_view = False
            can_edit = False
            if i in request.groups_can_view: can_view = True
            if i in request.groups_can_edit: can_edit = True
            Create.fileGroup(FileGroup_CreateRequest(file_id=toCreate.id, group_id=i, can_view=can_view, can_edit=can_edit))

        try:
            inputFile = open(request.filename, "rb")
            with open(f"{getFileStoragePath}\\{toCreate.id}", 'wb') as f:
                while contents := inputFile.read(1024 * 1024 * 64): # 64 MB chunks
                    f.write(contents)
                f.close()
        except:
            print('oops')
        finally:
            request.file.file.close()
    @staticmethod
    def folder(request: Folder_CreateRequest) -> Folder:
        toCreate = Folder(
            title=request.title,
            owner_id=request.owner_id,
            unrestricted_view_access=request.unrestricted_view_access,
            unrestricted_edit_access=request.unrestricted_edit_access,
            parent_folder_id=request.parent_folder_id
        )
        print(toCreate)
        with Session(engine) as session:
            session.add(toCreate)
            session.commit()
            session.refresh(toCreate)

            # CREATE USER RECORDS FROM users_can_****

            # ALSO ADD FIELDS FOR GROUPS

            return toCreate
    @staticmethod
    def folderUser(request: FolderUser_CreateRequest) -> FolderUser:
        toCreate = FolderUser(
            folder_id=request.folder_id,
            user_id=request.user_id,
            can_edit=request.can_edit,
            can_view=request.can_view
        )
        print(toCreate)
        with Session(engine) as session:
            session.add(toCreate)
            session.commit()
            session.refresh(toCreate)
            return toCreate
    @staticmethod
    def fileUser(request: FileUser_CreateRequest) -> FileUser:
        toCreate = FileUser(
            file_id=request.file_id,
            user_id=request.user_id,
            can_edit=request.can_edit,
            can_view=request.can_view
        )
        print(toCreate)
        with Session(engine) as session:
            session.add(toCreate)
            session.commit()
            session.refresh(toCreate)
            return toCreate
    @staticmethod
    def folderGroup(request: FolderGroup_CreateRequest) -> FolderGroup:
        toCreate = FolderGroup(
            folder_id=request.folder_id,
            group_id=request.group_id,
            can_edit=request.can_edit,
            can_view=request.can_view
        )
        print(toCreate)
        with Session(engine) as session:
            session.add(toCreate)
            session.commit()
            session.refresh(toCreate)
            return toCreate
    @staticmethod
    def fileGroup(request: FileGroup_CreateRequest) -> FileGroup:
        toCreate = FileGroup(
            file_id=request.file_id,
            group_id=request.group_id,
            can_edit=request.can_edit,
            can_view=request.can_view
        )
        print(toCreate)
        with Session(engine) as session:
            session.add(toCreate)
            session.commit()
            session.refresh(toCreate)
            return toCreate

###
###   Data :: RawSelect
###

class RawSelect:
    @staticmethod
    def select(targetType, *expressions) -> list:
        with Session(engine) as session:
            statement = select(targetType)
            if len(expressions) != 0:
                statement = statement.where(*expressions)
            results = session.exec(statement)
            result_list = results.all()
            print("Select:")
            print(result_list)
            return result_list
    @staticmethod
    def select_one(targetType, *expressions):
        with Session(engine) as session:
            statement = select(targetType)
            if len(expressions) != 0:
                statement = statement.where(*expressions)
            results = session.exec(statement)
            return results.one()

###
###   Data :: Select
###

class Select:
    @staticmethod
    def folders(*expressions) -> list[Output_Folder]:
        return list(map(Convert.folder, RawSelect.select(Folder, *expressions)))
    @staticmethod
    def files(*expressions) -> list[Output_File]:
        return list(map(Convert.file, RawSelect.select(File, *expressions)))
    @staticmethod
    def oneFolder(*expressions) -> Output_Folder:
        return Convert.folder(RawSelect.select_one(Folder, *expressions))
    @staticmethod
    def oneFile(*expressions) -> Output_File:
        return Convert.file(RawSelect.select_one(File, *expressions))


###
###   Data :: Update
###

class Update:
    @staticmethod
    def folder(request: Folder_UpdateRequest) -> Folder:
        debugPrefix = "FILES :: Updating folder ::"
        print(f"{debugPrefix} Request:")
        print(request)
        targetObject = RawSelect.select_one(Folder, Folder.id == request.id)
        for (key, value) in iter(request):
            if (value != None):
                print(key, value)
                setattr(targetObject, key, value)
        print(f"{debugPrefix} Updating to:")
        print(targetObject)
        with Session(engine) as session:
            session.add(targetObject)
            session.commit()
            session.refresh(targetObject)
            print(f"{debugPrefix} Success.")
            return targetObject
    @staticmethod
    def file(request: File_UpdateRequest) -> File:
        debugPrefix = "FILES :: Updating file ::"
        print(f"{debugPrefix} Request:")
        print(request)
        targetObject = RawSelect.select_one(File, File.id == request.id)
        for (key, value) in iter(request):
            if (value != None):
                print(key, value)
                setattr(targetObject, key, value)
        print(f"{debugPrefix} Updating to:")
        print(targetObject)
        with Session(engine) as session:
            session.add(targetObject)
            session.commit()
            session.refresh(targetObject)
            print(f"{debugPrefix} Success.")
            return targetObject
    @staticmethod
    def fileUser(request: FileUser_UpdateRequest) -> FileUser:
        debugPrefix = "FILES :: Updating file ::"
        print(f"{debugPrefix} Request:")
        print(request)
        targetObject = RawSelect.select_one(File, File.id == request.id)
        for (key, value) in iter(request):
            if (value != None):
                print(key, value)
                setattr(targetObject, key, value)
        print(f"{debugPrefix} Updating to:")
        print(targetObject)
        with Session(engine) as session:
            session.add(targetObject)
            session.commit()
            session.refresh(targetObject)
            print(f"{debugPrefix} Success.")
            return targetObject

def setup():
    systemFolder = RawSelect.select_one(Folder, Folder.id == 0)
    if (systemFolder == None): 
        systemFolder = Create.folder(Folder_CreateRequest(title="$SYSTEM", owner_id=0))
    filesInsideSystemFolder = RawSelect.select(File, File.parent_folder_id == systemFolder.id)
    if len(filesInsideSystemFolder) == 0:
        permanentFilesPath = getPermanentFilesPath()
        files = [f for f in os.listdir(permanentFilesPath) if os.path.isfile(os.path.join(permanentFilesPath, f))]
        for i in files:
            with open(i, "rb") as file:
                Create.fileForExisting(File_CreateRequestForExisting(
                    title=i, owner_id=0, parent_folder_id=0, unrestricted_view_access=True, filename=os.path.join(permanentFilesPath, file)
                ))

setup()