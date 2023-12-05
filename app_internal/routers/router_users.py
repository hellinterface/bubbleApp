
from fastapi import APIRouter, Depends, Request, status, Response, Body
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.exceptions import HTTPException
from datetime import timedelta
from ..modules import mod_users as MainModule
from pydantic import BaseModel
from typing import Annotated
import datetime

class Message(BaseModel):
    message: str

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
    dependencies=[Depends(MainModule.get_token_header)],
    responses={404: {"description": "Not found"}},
)

@router.get("/list", response_class=JSONResponse,
    response_model=list[MainModule.User],
    responses={
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": [{"id": 128, "handle": "somehandle", "other": "stuff..."}, "..."]
                }
            },
        },
    }
)
async def get_list():
    """Получение списка всех пользователей."""
    userlist = MainModule.list_users()
    return userlist

@router.post("/get_query", response_class=JSONResponse)
async def post_get_query(req: Annotated[dict, Body(examples=[{"query": "is_admin=1 OR handle='somehandle'"}])]):
    """Возвращает всех пользователей, которые удовлетворяют SQL-запросу в поле query."""
    print("AAAAAAAAAAAAAAAAAH")
    print(req)
    if not req.get('query'):
        return {"response": "failure"}
    resultList = [] # bdata.select_query('Users', req['query'])
    print(resultList)
    return resultList

@router.post("/getByID", response_class=JSONResponse,
    responses={
        404: {"model": Message, "description": "The item was not found"},
        200: {
            "description": "Item requested by ID",
            "content": {
                "application/json": {
                    "example": {"id": 128, "handle": "somehandle", "other": "stuff..."}
                }
            },
        },
    })
async def get_by_id(req: Annotated[dict, Body(examples=[{"id": 128}])]):
    """Получение пользователя, которому соответствует ID, указанный в поле id."""
    targetUser = MainModule.select_users(MainModule.User.id == req["id"])
    print(targetUser)
    if targetUser != None:
        return targetUser[0]
    else:
        return {"response": "failure"}

@router.get("/me")
async def get_current_user(req: Request):
    """Получение объекта текущего пользователя (на основе токена из cookie)."""
    print(req.state)
    try:
        return req.state.current_user
    except:
        return JSONResponse(status_code=401, content={"message":"Unauthorized"})
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
