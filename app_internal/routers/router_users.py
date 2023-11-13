
from fastapi import APIRouter, Depends, Request, status, Response
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.exceptions import HTTPException
from datetime import timedelta
from ..modules import mod_users as MainModule
from pydantic import BaseModel
import datetime

async def get_token_header(req: Request):
    print("GET TOKEN HEADER ----------------------------------------")
    token = req.headers.get("X-Access-Token")
    print(token)
    if token == None:
        print("TOKEN NONE")
        return False
    try:
        user = MainModule.get_user_from_token(token)
        print(user)
        req.state.current_user = user
        return user
    except:
        print("GET TOKEN HEADER ERROR ###")

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/list", response_class=JSONResponse)
async def get_list():
    userlist = MainModule.list_users()
    return {"response": "success", "userlist": userlist}

@router.post("/get_query", response_class=JSONResponse)
async def post_get_query(req: dict):
    print("AAAAAAAAAAAAAAAAAH")
    print(req)
    if not req.get('query'):
        return {"response": "failure"}
    resultList = [] # bdata.select_query('Users', req['query'])
    print(resultList)
    return resultList

@router.post("/getByID", response_class=JSONResponse)
async def getByID(req: dict):
    targetUser = MainModule.select_users(MainModule.User.id == req["id"])
    print(targetUser)
    if targetUser != None:
        return targetUser[0]
    else:
        return {"response": "failure"}

@router.get("/me")
async def get_current_user(req: Request):
    print(req.state)
    return req.state.current_user
    dt = datetime.datetime.now()
    return dt.strftime("%Y%m%d")

"""
failException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)
    

@router.post("/edit", response_class=JSONResponse)
async def post_edit(req: dict):
    # dbc = getDBConnection()
    # cur = dbc.cursor()
    # cur.execute("UPDATE Users SET ? WHERE id = ?")
    print(req)
    for key,value in req.items():
        print(f" --- {key}: {value}")
    
"""

@router.get("/test")
async def test():
    dt = datetime.datetime.now()
    return dt.strftime("%Y%m%d")
# ----------------------------------------------------------------------------
