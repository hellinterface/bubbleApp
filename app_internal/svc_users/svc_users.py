
from fastapi import APIRouter, Depends, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from ..dependencies import get_token_header
from pydantic import BaseModel
import sqlite3
import os
import secrets
import json

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

def createUsersTable(dbc):
    dbc.execute('''CREATE TABLE "Users" (
	"id"	TEXT NOT NULL UNIQUE,
	"handle"	TEXT NOT NULL UNIQUE,
	"visiblename"	TEXT NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	"password_hash"	TEXT NOT NULL,
	"dob"	INTEGER NOT NULL,
	"signupdate"	INTEGER NOT NULL,
	"profiles"	TEXT NOT NULL,
	PRIMARY KEY("id")
);''')

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    #print(d["profiles"])
    d["profiles"]
    d["profiles"] = json.loads(d["profiles"].replace('\\"', '\"'))
    #print(d["profiles"])
    profileList = list()
    for i in d["profiles"]:
        profileList.append(UserProfile(**i))
    d["profiles"] = profileList 
    #print(d["profiles"])
    userObject = User(**d)
    return userObject

# подключение к базе данных
def getDBConnection():
    conn = sqlite3.connect('users_db.db')
    conn.row_factory = dict_factory
    #ooo = conn.execute("SELECT * FROM sqlite_master WHERE type='table'").fetchall()
    #print(os.path.exists('users_db.db'))
    #print(len(ooo))
    #if len(ooo) == 0:
    #    createUsersTable(conn)
    #    print('Table created.')
    return conn

# position 0 = default profile
class UserProfileNEW(BaseModel):
    position: int
    title: str
    visiblename: str
    avatar_fileid: str
    contacts: list[str]
    groups: list[str]

class UserProfile(BaseModel):
    position: int
    title: str
    contacts: list[str]
    groups: list[str]

class SignUpUserInfo(BaseModel):
    id: str | None = None
    handle: str
    visiblename: str
    email: str
    password_hash: str
    # dob: int
    signupdate: int
    profiles: list[dict] | None = None

class User(BaseModel):
    id: str
    handle: str
    visiblename: str
    email: str
    password_hash: str
    # dob: int
    signupdate: int
    profiles: list[UserProfile]

def convertToUserList(strlist: list[str]):
    for i in strlist:
        User()

def addUserToDB(user: SignUpUserInfo):
    dbc = getDBConnection()
    cur = dbc.cursor()
    profilesString = json.dumps(user.profiles).replace('\"', '\\"')
    #string = f'INSERT INTO Users (id, handle, visiblename, email, password_hash, dob, signupdate, profiles) VALUES ("{user.id}", "{user.visiblename}", "{user.email}", "{user.password_hash}", 19700101, {user.signupdate}, "{profilesString}")'
    #print(string)
    #return string
    cur.execute("INSERT INTO Users (id, handle, visiblename, email, password_hash, dob, signupdate, profiles) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (user.id, user.handle, user.visiblename, user.email, user.password_hash, 19700101, user.signupdate, profilesString))
    dbc.commit()
    dbc.close()

@router.get("/list", response_class=JSONResponse)
async def read_items():
    dbc = getDBConnection()
    userlist = dbc.execute(f'SELECT * FROM Users').fetchall()
    dbc.close()
    print("Userlist: " + str(len(userlist)))
    for i in userlist:
        print(i)
    return {"soon": "yuah"}

@router.post("/getByID", response_class=JSONResponse)
async def getByID(req: dict):
    dbc = getDBConnection()
    targetUser = dbc.execute(f'SELECT * FROM Users WHERE id = "{req["id"]}"').fetchone()
    dbc.close()
    if targetUser != None:
        return {"response": "success", "data": targetUser.model_dump()} 
    else:
        return {"response": "failure"}

@router.post("/try_login", response_class=JSONResponse)
async def try_login(req: dict):
    dbc = getDBConnection()
    print(req)
    print(f'SELECT * FROM Users WHERE email="{req["email"]}" AND password_hash="{req["password_hash"]}"')
    targetUser = dbc.execute(f'SELECT * FROM Users WHERE email="{req["email"]}" AND password_hash="{req["password_hash"]}"').fetchone()
    dbc.close()
    print(targetUser)
    if (targetUser == None):
        return {"response": "failure"}
    else:
        return {"response": "success", "user_id": targetUser.id} 

@router.post("/try_signup", response_class=JSONResponse)
async def get_create(user_info: SignUpUserInfo): #new_user: User
    # print(req)
    default_profile = {
        "position": 0,
        "title": "Default",
        "contacts": list(),
        "groups": list()
    }
    new_profile = UserProfile(**default_profile)

    #print(new_profile.model_dump())
    #return {"fuck": "me"}

    user_info.id = secrets.token_urlsafe(6)
    user_info.profiles = list()
    user_info.profiles.append(new_profile.model_dump())

    addUserToDB(user_info)

    return {"gotcha": "success i guess"}

@router.get("/create_default", response_class=JSONResponse)
async def get_create_default():
    default_profile = {
        "position": 0,
        "title": "Default",
        "contacts": list(),
        "groups": list()
    }
    new_profile = UserProfile(**default_profile)

    print(json.dumps(default_profile))
    print(new_profile.model_dump())

    default_user = {
        "id": secrets.token_urlsafe(6),
        "handle": "cuntt",
        "visiblename": "Cuntie Pookie",
        #"dob": "20040401",
        "signupdate": "20220710",
        "email": "cunt@gmail.com",
        "password_hash": "fake_password_hash",
        "profiles": [new_profile.model_dump()]
    }

    new_user = User(**default_user)
    return new_user.dict()