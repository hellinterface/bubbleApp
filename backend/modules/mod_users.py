
#from .bdata import BData
from pydantic import BaseModel
import os
import secrets
import json
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, JSON, Column, Session, select
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Request


SECRET_KEY = "aa171942c2c26d0f39775b861f187a81f43865c0bf917ff58c1acca419d95b5f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 3

class User_CreateRequest(BaseModel):
    handle: str
    visible_name: str
    email: str
    password_hash: str

class User_UpdateRequest(BaseModel):
    id: int
    handle: Optional[str]
    visible_name: Optional[str]
    email: Optional[str]
    password_hash: Optional[str]
    join_date: Optional[int]
    avatar_fileid: Optional[int]
    bio: Optional[str]
    contacts: Optional[list[int]]
    notifications: Optional[list[dict]]
    events: Optional[list[int]]
    fav_users: Optional[list[int]]
    fav_groups: Optional[list[int]]
    folder_id: Optional[int]
    is_admin: Optional[bool]

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
    events: list[int] = Field(default=[], sa_column=Column(JSON))
    fav_users: list[int] = Field(default=[], sa_column=Column(JSON))
    fav_groups: list[int] = Field(default=[], sa_column=Column(JSON))
    folder_id: int
    is_admin: bool = Field(default=False)
    class Config:
        arbitrary_types_allowed = True

class Output_User(BaseModel):
    id: Optional[int]
    handle: str = Field
    visible_name: str
    email: str = Field
    avatar_fileid: Optional[int]
    bio: str
    contacts: list[int]
    notifications: list[dict]
    events: list[int]
    folder_id: int
    fav_users: list[int]
    fav_groups: list[int]

class PublicOutput_User(BaseModel):
    id: Optional[int]
    handle: str = Field
    visible_name: str
    email: str = Field
    avatar_fileid: Optional[int]
    bio: str

class TokenData(BaseModel):
    user_id: int | None = None

### SQL stuff

DIRNAME = os.path.dirname(os.path.dirname(__file__))
DB_USERS_PATH = DIRNAME + '\\data\\db_users.db'
sqlite_url = f"sqlite:///{DB_USERS_PATH}"
engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)

### Conversion

class Convert:
    @staticmethod
    def user(user:User) -> Output_User:
        return Output_User(**user.__dict__)
    @staticmethod
    def userToPublic(user:User) -> PublicOutput_User:
        return PublicOutput_User(**user.__dict__)

### Create

class Create:
    @staticmethod
    def user(request: User_CreateRequest) -> User:
        user_object = User(**request.__dict__)
        user_object.folder_id = 1
        user_object.join_date = datetime.now().strftime("%Y%m%d")

        print("Created user:")
        print(user_object)

        with Session(engine) as session:
            session.add(user_object)
            session.commit()
            session.refresh(user_object)
            return user_object

### Select

class Select:
    ### Select # Raw
    @staticmethod
    def __select(targetType, *expressions) -> list:
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
    def __select_one(targetType, *expressions):
        with Session(engine) as session:
            statement = select(targetType)
            if len(expressions) != 0:
                statement = statement.where(*expressions)
            results = session.exec(statement)
            return results.one()
    @staticmethod
    def users(*expressions) -> list[User]:
        return Select.__select(User, *expressions)
    @staticmethod
    def oneUser(*expressions) -> User:
        return Select.__select_one(User, *expressions)

class List:
    @staticmethod
    def users() -> list[User]:
        return Select.users()

class Update:
    @staticmethod
    def user(request: User_UpdateRequest) -> User:
        print(" ################## UPDATING USER ##################")
        print(request)
        user = Select.oneUser(User.id == request.id)
        for (key, value) in iter(request):
            if (value != None):
                print(key, value)
                setattr(user, key, value)
        print(user)
        with Session(engine) as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        
            

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
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_from_token(token: str) -> User:
    if (token == None):
        print("NO TOKEN")
        raise Exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        print("USER ID:", user_id)
        if user_id is None:
            raise Exception
    except JWTError:
        raise Exception
    try:
        user = Select.oneUser(User.id == user_id)
    except:
        raise Exception
        
    if user == None:
        raise Exception
    return user

async def get_token_header(req: Request):
    print(req.cookies)
    token = req.cookies.get('access_token')
    if token == None:
        token = req.headers.get("X-Access-Token")
    print("TOKEN COOKIE:", token)
    if token == None:
        return False
    try:
        user = get_user_from_token(token)
        print(user)
        req.state.current_user = user
        return user
    except:
        print("GET TOKEN HEADER ERROR")