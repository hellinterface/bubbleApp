from fastapi import APIRouter

router = APIRouter()

@router.get("/front/rtc")
async def get_rtc():
    f = open("../index.html", "r")
    return f.read()

@router.get("/api/frontend/hello")
async def get_hello():
    return {"answer": "Heya!"}