
from fastapi import APIRouter, Depends, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from ..dependencies import get_token_header
from pydantic import BaseModel, Field
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


def dict_factory(cursor, row):
    print(u"current directory: %s" % os.getcwd())
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print(d)
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    d["profiles"] = json.loads(d["profiles"].replace('\\"', '\"'))
    #print(d["profiles"])
    profileList = list()
    for i in d["profiles"]:
        profileList.append(UserProfile(**i))
    d["profiles"] = profileList 
    #print(d["profiles"])
    userObject = User(**d)
    return userObject

DB_USERS_PATH = os.path.dirname(__file__) + '\\users_db.db'

def createUsersTable(dbc):
    dbc.execute('''CREATE TABLE "Users" (
	"id"	TEXT NOT NULL UNIQUE,
	"handle"	TEXT NOT NULL UNIQUE,
	"visible_name"	TEXT NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	"password_hash"	TEXT NOT NULL,
	"join_date"	INTEGER NOT NULL,
	"folder_id"	TEXT NOT NULL UNIQUE,
	"profiles"	TEXT NOT NULL,
	PRIMARY KEY("id")
);''')

# проверка файла базы данных на валидность
def checkDB(filepath):
    conn = sqlite3.connect(filepath)
    conn.row_factory = sqlite3.Row
    tables = conn.execute("SELECT * FROM sqlite_master WHERE type='table'").fetchall()
    if len(tables) == 0:
        return False
    else:
        return True

# подключение к базе данных
def getDBConnection():
    conn = sqlite3.connect(DB_USERS_PATH)
    conn.row_factory = dict_factory
    if not checkDB(DB_USERS_PATH):
        createUsersTable(conn)
        print("******* database created. *******")
    return conn

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

class SignUpUserInfo(BaseModel):
    id: str | None = None
    handle: str
    visible_name: str
    email: str
    password_hash: str
    join_date: int
    profiles: list[dict] | None = None
    folder_id: str | None = None

class User(BaseModel):
    id: str = Field(allow_mutation=False)
    handle: str
    visible_name: str
    email: str
    password_hash: str
    join_date: int
    profiles: list[UserProfile]
    folder_id: str

def convertToUserList(strlist: list[str]):
    for i in strlist:
        User()

def replaceNoneWithEmptyString(x):
    if x == None:
        return ""
    else:
        return x

def db_insert(dbc, table_name, dictionary: BaseModel):
    # cur = dbc.cursor()
    dictionary = dictionary.model_dump()
    values = list(map(replaceNoneWithEmptyString, dictionary.values()))
    for i in values:
        if i == None:
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaa")
            i = ""
    values = list(map(str, values))
    query = f'''INSERT INTO {table_name} ({','.join(dictionary.keys())}) VALUES ("{'","'.join(values)}")'''
    print(query)
        

def addUserToDB(user: SignUpUserInfo):
    dbc = getDBConnection()
    cur = dbc.cursor()
    profilesString = json.dumps(user.profiles).replace('\"', '\\"')
    #string = f'INSERT INTO Users (id, handle, visiblename, email, password_hash, dob, signupdate, profiles) VALUES ("{user.id}", "{user.visiblename}", "{user.email}", "{user.password_hash}", 19700101, {user.signupdate}, "{profilesString}")'
    #print(string)
    #return string
    cur.execute("INSERT INTO Users (id, handle, visible_name, email, password_hash, join_date, folder_id, profiles) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (user.id, user.handle, user.visible_name, user.email, user.password_hash, user.join_date, user.folder_id, profilesString))
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
    return {"response": "success"}

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

@router.post("/signup", response_class=JSONResponse)
async def get_create(user_info: SignUpUserInfo): #new_user: User
    # print(req)
    default_profile = {
        "position": 0,
        "title": "Default",
        "visible_name": user_info.visible_name,
        "bio": "",
        "contacts": list(),
        "groups": list(),
        "notifications": list(),
        "events": list()
    }
    new_profile = UserProfile(**default_profile)

    user_info.id = secrets.token_urlsafe(6)
    user_info.profiles = list()
    user_info.profiles.append(new_profile.model_dump())

    db_insert(None, "Users", user_info)

    # addUserToDB(user_info)

    return {"response": "success", "user_id": user_info.id} 

@router.post("/edit", response_class=JSONResponse)
async def post_edit(req: dict):
    # dbc = getDBConnection()
    # cur = dbc.cursor()
    # cur.execute("UPDATE Users SET ? WHERE id = ?")
    print(req)
    for key,value in req.items():
        print(f" --- {key}: {value}")