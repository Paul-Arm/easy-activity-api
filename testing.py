from fastapi import APIRouter, Depends, HTTPException
from dbModels import db, Nutzer


testing_router = APIRouter()

@testing_router.get("/test")
async def test():
    #res = Nutzer.create(Nutzername="test", Passwort="test", Email="test", Nachname="test", Vorname="test")
    res = Nutzer.get()
    return {"message": res}