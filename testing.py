from fastapi import APIRouter, Depends, HTTPException
from dbModels import database, Nutzer, Gruppe, Aktivität, Adresse


testing_router = APIRouter()

@testing_router.get("/test")
async def test():
    res = Gruppe.get()

    return {"message": res}