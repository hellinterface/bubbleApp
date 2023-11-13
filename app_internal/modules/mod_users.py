
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


SECRET_KEY = "aa171942c2c26d0f39775b861f187a81f43865c0bf917ff58c1acca419d95b5f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 3

# position 0 = default profile
class UserProfile(BaseModel):
    position: int
    title: str
    visible_name: str
    avatar_fileid: str | None = None
    bio: str
    contacts: list[str]
    groups: list[str]
    notifications: list[str]
    events: list[str]

class SignupData(BaseModel):
    #id: Optional[int]
    handle: str
    visible_name: str
    email: str
    password_hash: str
    class Config:
        arbitrary_types_allowed = True

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    handle: str = Field(unique=True)
    visible_name: str
    email: str = Field(unique=True)
    password_hash: str
    join_date: int
    profiles: list[dict] = Field(sa_column=Column(JSON))
    folder_id: str
    class Config:
        arbitrary_types_allowed = True


class TokenData(BaseModel):
    user_id: str | None = None

DIRNAME = os.path.dirname(os.path.dirname(__file__))
DB_USERS_PATH = DIRNAME + '\\data\\db_users.db'
print(DB_USERS_PATH)
#bdata = BData(DB_USERS_PATH, user_factory)
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{DB_USERS_PATH}"
engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)

def checkDatabase():
    return

def create_user(signup_data: SignupData) -> User:
    default_profile = {
        "position": 0,
        "title": "Default",
        "visible_name": signup_data.visible_name,
        "bio": "",
        "contacts": list(),
        "groups": list(),
        "notifications": list(),
        "events": list()
    }
    new_profile = UserProfile(**default_profile)

    user_object = User(**signup_data.__dict__)

    user_object.profiles = list()
    user_object.profiles.append(new_profile.__dict__)
    user_object.folder_id = secrets.token_urlsafe(8)
    user_object.join_date = datetime.now().strftime("%Y%m%d")

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    #print(profiles_str)
    print(user_object)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    with Session(engine) as session:
        session.add(user_object)
        session.commit()
        return user_object

    raise Exception

def list_users() -> list[User]:
    with Session(engine) as session:
        statement = select(User)
        results = session.exec(statement)
        userlist = results.all()
        print("Userlist:")
        print(userlist)
        return userlist

def select_users(*expressions) -> list[User]:
    with Session(engine) as session:
        statement = select(User).where(*expressions)
        results = session.exec(statement)
        userlist = results.all()
        print("Select users:")
        print(userlist)
        return userlist

class LoginData(BaseModel):
    email: str
    password_hash: str

def login(req: LoginData) -> User:
    targetUser = select_users(User.email == req.email, User.password_hash == req.password_hash)
    print("MOD LOGIN")
    print(targetUser)
    if len(targetUser) != 0:
        return targetUser[0]
    else:
        return None

def create_token_for_user_id(user_id: str) -> str:
    print("DAAAAAAAAAAAAAAAAAAAAAAAAAAAAATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print(user_id)
    print("DAAAAAAAAAAAAAAAAAAAAAAAAAAAAATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
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
    print("WOOOOOOOOOOOOOOOOOOOOO")
    if (token == None):
        print("NO TOKEN")
        raise Exception
    try:
        print("JWT")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        print(user_id)
        if user_id is None:
            raise Exception
        print("USER ID:", user_id)
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise Exception
    try:
        user = select_users(User.id == user_id)
    except:
        raise Exception
        
    if len(user) == 0:
        raise Exception
    return user[0]

print("!!! CREATING")
#create_user( SignupData(handle="owoman", visible_name="IAmOWOman", email="owo@dvfu.ru", password_hash="fake_password_hash", join_date=20231107) )
print("!!! LISTING")
list_users()