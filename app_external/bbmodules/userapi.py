
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Annotated
from pydantic import BaseModel
import secrets
import httpx
from .. import exceptions


# LOGIN LOGIC

SECRET_KEY = "aa171942c2c26d0f39775b861f187a81f43865c0bf917ff58c1acca419d95b5f"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 3

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str | None = None
    
class User(BaseModel):
    username: str
    email: str | None = None
    visiblename: str | None = None

class UserInDB(User):
    password_hash: str

class LogInRequest(BaseModel):
    email: str
    password_hash: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(user_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            objectToSend = {"id": user_id }
            r = await client.post('http://127.0.0.1:8080/api/users/getByID', json=objectToSend)
            backendOutput = r.json()
        except:
            print("SQAKND")
            raise exceptions.httpxException
        if (backendOutput["response"] == "success"):
            return backendOutput["data"]
        else:   
            print("FCUK")
            raise exceptions.notFoundException

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    print("WOOOOOOOOOOOOOOOOOOOOO")
    if (token == None):
        print("NO TOKEN")
        raise credentials_exception
    try:
        print("JWT")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        print("USER ID: " + user_id)
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    try:
        user = await get_user(user_id=token_data.user_id)
    except exceptions.notFoundException:
        raise exceptions.notFoundException
    except exceptions.httpxException:
        raise exceptions.httpxException
        
    if user is None:
        raise credentials_exception
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticate_user(email: str, passwordHash: str):
    async with httpx.AsyncClient() as client:
        try:
            objectToSend = {"email": email, "password_hash": passwordHash}
            r = await client.post('http://127.0.0.1:8080/api/users/login', json=objectToSend)
            backendOutput = r.json()
            print(backendOutput)
            if (backendOutput["response"] == "success"):
                return backendOutput["user_id"]
            else:   
                raise Exception
        except:
            raise Exception