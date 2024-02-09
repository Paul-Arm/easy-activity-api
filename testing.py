from fastapi import APIRouter, Depends, HTTPException
from dbModels import database, Nutzer, Gruppe, Aktivität, Adresse, NutzerGruppe


testing_router = APIRouter()

@testing_router.get("/test")
async def test():
    res = NutzerGruppe.create_table()

    return {"message": res}