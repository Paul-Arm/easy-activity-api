from fastapi import APIRouter, Depends, HTTPException
from dbModels import EventOrtVorschlag, EventZeitVorschlag


testing_router = APIRouter()

@testing_router.get("/test")
async def test():
    res = EventZeitVorschlag.create_table()
    res2 = EventOrtVorschlag.create_table()

    return {"message": res,"msg2": res2}