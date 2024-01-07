
import os
from pydantic import BaseModel
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, JSON, Column, Session, select
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Request, HTTPException

from .. import config
from ..models import Output_User, PublicOutput_User
from ..requests import User_CreateRequest, User_UpdateRequest

###
###   Entities :: SQL/Raw
###

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    handle: str = Field(unique=True)
    visible_name: str
    email: str = Field(unique=True)
    password_hash: str
    join_date: int
    avatar_fileid: Optional[int] = Field(default=None)
    bio: str = Field(default="")
    contacts: list[int] = Field(default=[], sa_column=Column(JSON))
    notifications: list[dict] = Field(default=[], sa_column=Column(JSON))
    events: list[dict] = Field(default=[], sa_column=Column(JSON))
    fav_users: list[int] = Field(default=[], sa_column=Column(JSON))
    fav_groups: list[int] = Field(default=[], sa_column=Column(JSON))
    folder_id: int
    sent_media_folder_id: int
    is_admin: bool = Field(default=False)
    class Config:
        arbitrary_types_allowed = True

###
###   SQL Database Engine
###

sqlite_url = f"sqlite:///{config.DB_PATH}"
engine = create_engine(sqlite_url, echo=config.SQL_ECHO)
SQLModel.metadata.create_all(engine)

###
###   Data :: Convert
###

class Convert:
    @staticmethod
    def user(user:User) -> Output_User:
        return Output_User(**user.__dict__)
    @staticmethod
    def userToPublic(user:User) -> PublicOutput_User:
        return PublicOutput_User(**user.__dict__)

###
###   Data :: Create
###

class Create:
    @staticmethod
    def user(request: User_CreateRequest) -> User:
        from ..cores import core_files as FilesModule
        debugPrefix = "USERS :: Creating user ::"
        # Создание папок для пользователя
        print(f"{debugPrefix} Creating personal folders...")
        rootFolder = FilesModule.Create.folder(FilesModule.Folder_CreateRequest(owner_id=0, title=f"Персональное хранилище @{request.handle}"))
        sentMediaFolder = FilesModule.Create.folder(FilesModule.Folder_CreateRequest(owner_id=0, parent_folder_id=rootFolder.id, title=f"Прикреплённые файлы"))

        user_object = User(**request.__dict__)
        user_object.folder_id = rootFolder.id
        user_object.sent_media_folder_id = sentMediaFolder.id
        user_object.join_date = datetime.now().strftime("%Y%m%d")
        print(f"{debugPrefix} Object:")
        print(user_object)
        with Session(engine) as session:
            session.add(user_object)
            session.commit()
            session.refresh(user_object)
            print(f"{debugPrefix} Success.")

        # Обновление полей owner_id в созданных папках
        print(f"{debugPrefix} Updating info about personal folders...")
        FilesModule.Update.folder(FilesModule.Folder_UpdateRequest(id=rootFolder.id, owner_id=user_object.id))
        FilesModule.Update.folder(FilesModule.Folder_UpdateRequest(id=sentMediaFolder.id, owner_id=user_object.id))
        print(f"{debugPrefix} Done updating.")

        return user_object

###
###   Data :: Select
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
            print(f"USERS :: Select <{targetType.__name__}>:")
            print(result_list)
            return result_list
    @staticmethod
    def select_one(targetType, *expressions):
        with Session(engine) as session:
            statement = select(targetType)
            if len(expressions) != 0:
                statement = statement.where(*expressions)
            result = session.exec(statement).one_or_none()
            print(f"USERS :: Select one <{targetType.__name__}>:")
            print(result)
            return result
    @staticmethod
    def users(*expressions) -> list[User]:
        return RawSelect.select(User, *expressions)
    @staticmethod
    def oneUser(*expressions) -> User:
        return RawSelect.select_one(User, *expressions)

class Select:
    @staticmethod
    def users(*expressions) -> list[Output_User]:
        return list(map(Convert.user, RawSelect.users(*expressions)))
    @staticmethod
    def oneUser(*expressions) -> Output_User:
        result = RawSelect.oneUser(*expressions)
        if (result == None): return None
        return Convert.user(result)

###
###   Data :: List
###

class List:
    @staticmethod
    def users() -> list[Output_User]:
        return Select.users()


###
###   Data :: Update
###

class Update:
    @staticmethod
    def user(request: User_UpdateRequest) -> User:
        print(f"USERS :: Updating user :: Request:")
        print(request)
        user = RawSelect.oneUser(User.id == request.id)
        for (key, value) in iter(request):
            if (value != None):
                print(key, value)
                setattr(user, key, value)
        print(f"USERS :: Updating user :: Updating to:")
        print(user)
        with Session(engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            print(f"USERS :: Updating user :: Success.")
            return user
        
###
###   Data :: Delete
###

class Delete:
    @staticmethod
    def user(target_id: int) -> Output_User:
        target = RawSelect.select_one(User, User.id == target_id)
        print(f"USERS :: Deleting user :: ID = {target_id}")
        print(target)
        if (target != None):
            with Session(engine) as session:
                session.delete(target)  
                session.commit()
                print(f"USERS :: Deleting user :: Success.")
                return target
        else:
            raise Exception()
            

###
###   Authentication
###

SECRET_KEY = "aa171942c2c26d0f39775b861f187a81f43865c0bf917ff58c1acca419d95b5f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 5

class TokenData(BaseModel):
    user_id: int | None = None

def create_token_for_user_id(user_id: str) -> str:
    print(user_id)
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"user_id": user_id}, expires_delta=access_token_expires
    )
    return access_token

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_from_token(token: str) -> User:
    if (token == None):
        print("NO TOKEN")
        raise Exception()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        print("USER ID:", user_id)
        if user_id is None:
            raise Exception()
    except JWTError:
        raise Exception()
    try:
        user = Select.oneUser(User.id == user_id)
    except:
        raise Exception()
        
    if user == None:
        raise Exception()
    return user

async def get_token_header(req: Request):
    print(f"USERS :: AUTH :: Get token header")
    print(req.cookies)
    token = req.cookies.get('access_token')
    if token == None:
        token = req.headers.get("X-Access-Token")
    print(f"USERS :: AUTH :: Token = {token}")
    if token == None:
        raise HTTPException(status_code=401, detail="Not logged in!")
    try:
        user = get_user_from_token(token)
        print(f"USERS :: AUTH :: {user.id} {user.handle} {user.visible_name}")
        req.state.current_user = user
        return user
    except:
        print(f"USERS :: AUTH :: No user found.")
