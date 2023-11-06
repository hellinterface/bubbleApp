
from fastapi import APIRouter, Depends, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from pydantic import BaseModel, Field
import sqlite3
import os
import secrets
import json
from ..bdata import BData

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

def user_factory(cursor, row):
    # print(u"current directory: %s" % os.getcwd())
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    print(d)
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
print(DB_USERS_PATH)
bdata = BData(DB_USERS_PATH, user_factory)

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
    id: str = Field(allow_mutation=False, bdata_unique=True)
    handle: str = Field(bdata_unique=True)
    visible_name: str = Field()
    email: str = Field(bdata_unique=True)
    password_hash: str = Field()
    join_date: int = Field()
    profiles: list[UserProfile] = Field(bdata_type=str)
    folder_id: str = Field(bdata_unique=True)

class User_inDB(BaseModel):
    id: str = Field(allow_mutation=False, bdata_unique=True)
    handle: str = Field(bdata_unique=True)
    visible_name: str = Field()
    email: str = Field(bdata_unique=True)
    password_hash: str = Field()
    join_date: int = Field()
    profiles: str = Field(bdata_type=str)
    folder_id: str = Field(bdata_unique=True)


def convertToUserList(strlist: list[str]):
    for i in strlist:
        User()

def addUserToDB(user: SignUpUserInfo):
    #profilesString = json.dumps(user.profiles).replace('\"', '\\"')
    bdata.insert("Users", user)

@router.get("/list", response_class=JSONResponse)
async def read_items():
    userlist = bdata.select('Users', '*')
    print("Userlist: " + str(len(userlist)))
    for i in userlist:
        print(i)
    return {"response": "success", "userlist": userlist}

@router.post("/get_query", response_class=JSONResponse)
async def post_get_query(req: dict):
    print("AAAAAAAAAAAAAAAAAH")
    print(req)
    if not req.get('query'):
        return {"response": "failure"}
    resultList = bdata.select_query('Users', req['query'])
    print(resultList)
    return resultList

@router.post("/getByID", response_class=JSONResponse)
async def getByID(req: dict):
    targetUser = bdata.select('Users', {"id": req["id"]})
    print(targetUser)
    if targetUser != None:
        return {"response": "success", "data": targetUser[0].model_dump()} 
    else:
        return {"response": "failure"}

@router.post("/login", response_class=JSONResponse)
async def try_login(req: dict):
    print(req)
    targetUserList = bdata.select("Users", {"email": req["email"], "password_hash": req["password_hash"]})
    print(targetUserList)
    if (len(targetUserList) == 0):
        print("FAUL")
        return {"response": "failure"}
    else:
        print("YEAH")
        return {"response": "success", "user_id": targetUserList[0].id} 

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
    user_info.folder_id = secrets.token_urlsafe(8)

    dictionary = user_info.model_dump()

    profiles_str = json.dumps(json.dumps(user_info.profiles))
    profiles_str = profiles_str[:-1]
    profiles_str = profiles_str[1:]
    profiles_str = profiles_str.replace('"', '""')
    dictionary['profiles'] = profiles_str

    user_indb = User_inDB(**dictionary)

    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(profiles_str)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    bdata.insert("Users", user_indb)

    return {"response": "success", "user_id": user_info.id} 

@router.post("/edit", response_class=JSONResponse)
async def post_edit(req: dict):
    # dbc = getDBConnection()
    # cur = dbc.cursor()
    # cur.execute("UPDATE Users SET ? WHERE id = ?")
    print(req)
    for key,value in req.items():
        print(f" --- {key}: {value}")
    

# ----------------------------------------------------------------------------

tables = bdata.get_tables()
print("Tables:")
print(tables)
if ("Users" not in tables):
    bdata.create("Users", User_inDB)