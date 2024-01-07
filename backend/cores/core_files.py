
import os
from sqlmodel import Field, SQLModel, create_engine, JSON, Column, Session, select
from typing import Optional
from datetime import datetime, timedelta, date
from time import mktime
from secrets import token_urlsafe

from .. import exceptions
from .. import config

from ..models import Output_File, Output_FilesUserEntry, Output_Folder, Output_FileInList, Output_FolderInList, Output_FilesGroupEntry, Output_FolderContents
from ..requests import File_CreateRequest, File_UpdateRequest, Folder_CreateRequest, Folder_UpdateRequest, File_CreateRequestForExisting
from ..requests import FolderGroup_CreateRequest, FolderUser_CreateRequest #, FolderUser_UpdateRequest, FolderGroup_UpdateRequest
from ..requests import FileGroup_CreateRequest, FileUser_CreateRequest, FileUser_UpdateRequest #, FileGroup_UpdateRequest

###
###   Entites :: SQL/Raw
###

print(config.DB_PATH)
sqlite_url = f"sqlite:///{config.DB_PATH}"
engine = create_engine(sqlite_url, echo=config.SQL_ECHO)
SQLModel.metadata.create_all(engine)

class File(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field()
    date_added: int = Field()
    date_modified: int = Field()
    owner_id: int = Field()
    user_modified_id: int = Field()
    share_link: str = Field(unique=True)
    parent_folder_id: int = Field()
    size: int = Field()
    unrestricted_view_access: bool = Field(default=False)
    unrestricted_edit_access: bool = Field(default=False)

class Folder(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field()
    max_size: Optional[int] = Field()
    owner_id: int = Field()
    share_link: str = Field(unique=True)
    parent_folder_id: Optional[int] = Field()
    unrestricted_view_access: bool = Field(default=False)
    unrestricted_edit_access: bool = Field(default=False)

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

###
###   SQL Database Engine
###

def getFileStoragePath():
    return config.FILESTORAGE_PATH

def getPermanentFilesPath():
    return config.PERMFILES_PATH

###
###   Data :: Convert
###

class Convert:
    @staticmethod
    def userEntry(user: FolderUser|FileUser) -> Output_FilesUserEntry:
        from ..cores import core_users as UsersModule
        userInfo = UsersModule.RawSelect.oneUser(UsersModule.User.id == user.user_id)
        user_publicInfo = UsersModule.convertUserToPublic(userInfo)
        return Output_FilesUserEntry(user_information=user_publicInfo, can_view=user.can_view, can_edit=user.can_edit)
    @staticmethod
    def groupEntry(group: FolderGroup|FileGroup) -> Output_FilesUserEntry:
        from ..cores import core_groups as GroupsModule
        groupInfo = GroupsModule.Select.oneGroup(GroupsModule.Group.id == group.group_id)
        return Output_FilesGroupEntry(group_information=groupInfo, can_view=group.can_view, can_edit=group.can_edit)
    @staticmethod
    def file(file: File) -> Output_File:
        from ..cores import core_users as UsersModule
        res = Output_File(
            **file.__dict__,
            owner = UsersModule.Convert.userToPublic(UsersModule.RawSelect.oneUser(UsersModule.User.id == file.owner_id)),
            user_modified = UsersModule.Convert.userToPublic(UsersModule.RawSelect.oneUser(UsersModule.User.id == file.user_modified_id)),
            users = Select.fileUsers(FileUser.file_id == file.id),
            groups = Select.fileGroups(FileGroup.file_id == file.id)
        )
        return res
    @staticmethod
    def folder(folder: Folder) -> Output_Folder:
        from ..cores import core_users as UsersModule
        res = Output_Folder(
            **folder.__dict__,
            owner = UsersModule.Convert.userToPublic(UsersModule.RawSelect.oneUser(UsersModule.User.id == folder.owner_id)),
            users = Select.folderUsers(FolderUser.folder_id == folder.id),
            groups = Select.folderGroups(FolderGroup.folder_id == folder.id)
        )
        return res
    @staticmethod
    def fileInList(file: File) -> Output_FileInList:
        from ..cores import core_users as UsersModule
        res = Output_FileInList(
            **file.__dict__,
            owner = UsersModule.Convert.userToPublic(UsersModule.RawSelect.oneUser(UsersModule.User.id == file.owner_id)),
            user_modified = UsersModule.Convert.userToPublic(UsersModule.RawSelect.oneUser(UsersModule.User.id == file.user_modified_id))
        )
        return res
    @staticmethod
    def folderInList(folder: Folder) -> Output_FolderInList:
        from ..cores import core_users as UsersModule
        res = Output_FolderInList(
            **folder.__dict__,
            owner = UsersModule.Convert.userToPublic(UsersModule.RawSelect.oneUser(UsersModule.User.id == folder.owner_id))
        )
        return res


###
###   Data :: Create
###

class Create:
    @staticmethod
    def file(request: File_CreateRequest) -> File:
        debugPrefix = "FILES :: Creating file ::"
        print(f"{debugPrefix} Request:")
        print(request)
        currentTimestamp = mktime(datetime.now().timetuple())
        toCreate = File(
            title=request.title,
            owner_id=request.owner_id,
            user_modified_id=request.owner_id,
            date_added=currentTimestamp,
            date_modified=currentTimestamp,
            unrestricted_view_access=request.unrestricted_view_access,
            unrestricted_edit_access=request.unrestricted_edit_access,
            parent_folder_id=request.parent_folder_id,
            share_link=token_urlsafe(16),
            size=request.file.size
        )
        print(f"{debugPrefix} Creating File object:")
        print(request)
        with Session(engine) as session:
            session.add(toCreate)
            session.commit()
            session.refresh(toCreate)
            print(f"{debugPrefix} Created File object.")

        userIdList = set()
        inherited_users_can_view = set()
        inherited_users_can_edit = set()
        groupIdList = set()
        inherited_groups_can_view = set()
        inherited_groups_can_edit = set()

        # Наследование владельца родительской папки
        if request.parent_folder_id: 
            inherit_owner_id = RawSelect.select_one(Folder, Folder.id == request.parent_folder_id).owner_id
            if request.owner_id != inherit_owner_id:
                userIdList.add(inherit_owner_id)
                inherited_users_can_view.add(inherit_owner_id)
                inherited_users_can_edit.add(inherit_owner_id)
        # Наследование прав чтения из родительской папки
        if request.inheritView and request.parent_folder_id: 
            # Пользователи
            for i in RawSelect.select(FolderUser, FolderUser.can_view == True, FolderUser.folder_id == request.parent_folder_id): 
                userIdList.add(i.user_id)
                inherited_users_can_view.add(i.user_id)
            # Группы
            for i in RawSelect.select(FolderGroup, FolderGroup.can_view == True, FolderGroup.folder_id == request.parent_folder_id): 
                groupIdList.add(i.group_id)
                inherited_groups_can_view.add(i.group_id)
        # Наследование прав изменения из родительской папки
        if request.inheritEdit and request.parent_folder_id: 
            # Пользователи
            for i in RawSelect.select(FolderUser, FolderUser.can_edit == True, FolderUser.folder_id == request.parent_folder_id): 
                userIdList.add(i.user_id)
                inherited_users_can_edit.add(i.user_id)
            # Группы
            for i in RawSelect.select(FolderGroup, FolderGroup.can_edit == True, FolderGroup.folder_id == request.parent_folder_id): 
                groupIdList.add(i.group_id)
                inherited_groups_can_view.add(i.group_id)

        # Пользователи
        for i in request.users_can_view: userIdList.add(i)
        for i in request.users_can_edit: userIdList.add(i)
        for i in userIdList:
            can_view = False
            can_edit = False
            if i in request.users_can_view: can_view = True
            if i in request.users_can_edit: can_edit = True
            if (i in inherited_users_can_view): can_view = True
            if (i in inherited_users_can_edit): can_edit = True
            Create.fileUser(FileUser_CreateRequest(file_id=toCreate.id, user_id=i, can_view=can_view, can_edit=can_edit))

        # Группы
        for i in request.groups_can_view: groupIdList.add(i)
        for i in request.groups_can_edit: groupIdList.add(i)
        for i in groupIdList:
            can_view = False
            can_edit = False
            if i in request.groups_can_view: can_view = True
            if i in request.groups_can_edit: can_edit = True
            if (i in inherited_groups_can_view): can_view = True
            if (i in inherited_groups_can_edit): can_edit = True
            Create.fileGroup(FileGroup_CreateRequest(file_id=toCreate.id, group_id=i, can_view=can_view, can_edit=can_edit))

        try:
            print(f"{debugPrefix} Filename: {request.file.filename}")
            print(f"{debugPrefix} Writing file to disk...: ({getFileStoragePath()}\\{toCreate.id})")
            with open(f"{getFileStoragePath()}\\{toCreate.id}", 'wb') as f:
                while True:
                    data = request.file.file.read(1024 * 1024 * 64) # 64 MB chunks
                    print(f"{debugPrefix} Wrote chunk. Moving onto the next...")
                    f.write(data)
                    if not data: break
                print(f"{debugPrefix} Done writing file to disk.")
                f.close()
        except:
                print(f"{debugPrefix} ERROR :: Couldn't write file to disk.")
        finally:
            request.file.file.close()
        return toCreate
    @staticmethod
    def fileForExisting(request: File_CreateRequestForExisting) -> File:
        debugPrefix = "FILES :: Creating file (existing) ::"
        currentTimestamp = mktime(datetime.now().timetuple())
        toCreate = File(
            title=request.title,
            owner_id=request.owner_id,
            user_modified_id=request.owner_id,
            date_added=currentTimestamp,
            date_modified=currentTimestamp,
            unrestricted_view_access=request.unrestricted_view_access,
            unrestricted_edit_access=request.unrestricted_edit_access,
            parent_folder_id=request.parent_folder_id,
            share_link=token_urlsafe(16),
            size=os.path.getsize(request.filepath)
        )
        print(f"{debugPrefix} Creating File object:")
        print(request)
        with Session(engine) as session:
            session.add(toCreate)
            session.commit()
            session.refresh(toCreate)
            print(f"{debugPrefix} Created File object.")

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
            print(f"{debugPrefix} Filename: {request.filepath}")
            print(f"{debugPrefix} Writing file to disk...: ({getFileStoragePath()}\\{toCreate.id})")
            inputFile = open(request.filepath, "rb")
            with open(f"{getFileStoragePath()}\{toCreate.id}", 'wb') as f:
                while True:
                    data = inputFile.read(1024 * 1024 * 64) # 64 MB chunks
                    print("WRITING")
                    f.write(data)
                    if not data: break
                f.close()
        except:
            print(f"{debugPrefix} ERROR :: Couldn't write file to disk.")
    @staticmethod
    def folder(request: Folder_CreateRequest) -> Folder:
        toCreate = Folder(
            title=request.title,
            owner_id=request.owner_id,
            unrestricted_view_access=request.unrestricted_view_access,
            unrestricted_edit_access=request.unrestricted_edit_access,
            parent_folder_id=request.parent_folder_id,
            share_link=token_urlsafe(16)
        )
        print(toCreate)
        with Session(engine) as session:
            session.add(toCreate)
            session.commit()
            session.refresh(toCreate)

        userIdList = set()
        inherited_users_can_view = set()
        inherited_users_can_edit = set()
        groupIdList = set()
        inherited_groups_can_view = set()
        inherited_groups_can_edit = set()

        # Наследование владельца родительской папки
        if request.parent_folder_id: 
            inherit_owner_id = RawSelect.select_one(Folder, Folder.id == request.parent_folder_id).owner_id
            if request.owner_id != inherit_owner_id:
                userIdList.add(inherit_owner_id)
                inherited_users_can_view.add(inherit_owner_id)
                inherited_users_can_edit.add(inherit_owner_id)
        # Наследование прав чтения из родительской папки
        if request.inheritView and request.parent_folder_id: 
            # Пользователи
            for i in RawSelect.select(FolderUser, FolderUser.can_view == True, FolderUser.folder_id == request.parent_folder_id): 
                userIdList.add(i.user_id)
                inherited_users_can_view.add(i.user_id)
            # Группы
            for i in RawSelect.select(FolderGroup, FolderGroup.can_view == True, FolderGroup.folder_id == request.parent_folder_id): 
                groupIdList.add(i.group_id)
                inherited_groups_can_view.add(i.group_id)
        # Наследование прав изменения из родительской папки
        if request.inheritEdit and request.parent_folder_id: 
            # Пользователи
            for i in RawSelect.select(FolderUser, FolderUser.can_edit == True, FolderUser.folder_id == request.parent_folder_id): 
                userIdList.add(i.user_id)
                inherited_users_can_edit.add(i.user_id)
            # Группы
            for i in RawSelect.select(FolderGroup, FolderGroup.can_edit == True, FolderGroup.folder_id == request.parent_folder_id): 
                groupIdList.add(i.group_id)
                inherited_groups_can_view.add(i.group_id)

        # Пользователи
        for i in request.users_can_view: userIdList.add(i)
        for i in request.users_can_edit: userIdList.add(i)
        for i in userIdList:
            can_view = False
            can_edit = False
            if i in request.users_can_view: can_view = True
            if i in request.users_can_edit: can_edit = True
            if (i in inherited_users_can_view): can_view = True
            if (i in inherited_users_can_edit): can_edit = True
            Create.folderUser(FolderUser_CreateRequest(folder_id=toCreate.id, user_id=i, can_view=can_view, can_edit=can_edit))

        # Группы
        for i in request.groups_can_view: groupIdList.add(i)
        for i in request.groups_can_edit: groupIdList.add(i)
        for i in groupIdList:
            can_view = False
            can_edit = False
            if i in request.groups_can_view: can_view = True
            if i in request.groups_can_edit: can_edit = True
            if (i in inherited_groups_can_view): can_view = True
            if (i in inherited_groups_can_edit): can_edit = True
            Create.folderGroup(FolderGroup_CreateRequest(folder_id=toCreate.id, group_id=i, can_view=can_view, can_edit=can_edit))

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
            result = session.exec(statement).one_or_none()
            return result

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
    def folderUsers(*expressions) -> list[Output_FilesUserEntry]:
        return list(map(Convert.userEntry, RawSelect.select(FolderUser, *expressions)))
    @staticmethod
    def fileUsers(*expressions) -> list[Output_FilesUserEntry]:
        return list(map(Convert.userEntry, RawSelect.select(FileUser, *expressions)))
    @staticmethod
    def folderGroups(*expressions) -> list[Output_FilesGroupEntry]:
        return list(map(Convert.groupEntry, RawSelect.select(FolderGroup, *expressions)))
    @staticmethod
    def fileGroups(*expressions) -> list[Output_FilesGroupEntry]:
        return list(map(Convert.groupEntry, RawSelect.select(FileGroup, *expressions)))
    @staticmethod
    def oneFolder(*expressions) -> Output_Folder:
        res = RawSelect.select_one(Folder, *expressions)
        if res == None: return None
        return Convert.folder(res)
    @staticmethod
    def oneFile(*expressions) -> Output_File:
        res = RawSelect.select_one(File, *expressions)
        if res == None: return None
        return Convert.file(res)


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

def getFolderContents(id: int):
    folderInfo = RawSelect.select_one(Folder, Folder.id == id)
    folders = RawSelect.select(Folder, Folder.parent_folder_id == id)
    files = RawSelect.select(File, File.parent_folder_id == id)
    out_folders = list(map(Convert.folderInList, folders))
    out_files = list(map(Convert.fileInList, files))
    return Output_FolderContents(folders=out_folders, files=out_files)

def __getPermissions(user_id: int, entity: Output_File|Output_Folder):
    result = {"can_view": False, "can_edit": False}
    if (entity.unrestricted_view_access): result["can_view"] = True
    if (entity.unrestricted_edit_access): result["can_edit"] = True
    if (entity.owner.id == user_id):
        result["can_view"] = True
        result["can_edit"] = True
    else:
        for i in entity.users:
            if (i.user_information.id == user_id):
                result["can_view"] = i.can_view
                result["can_edit"] = i.can_edit
    return result

def getUserPermissionsOfFile(user_id: int, file_id: int):
    fileInfo = Select.oneFile(File.id == file_id)
    return __getPermissions(user_id=user_id, entity=fileInfo)

def getUserPermissionsOfFolder(user_id: int, folder_id: int):
    folderInfo = Select.oneFolder(Folder.id == folder_id)
    return __getPermissions(user_id=user_id, entity=folderInfo)

