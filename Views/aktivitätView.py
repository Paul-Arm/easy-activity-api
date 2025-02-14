from pydanticModels import neueAktivität
from dbModels import  Aktivität



from fastapi import APIRouter, Depends, HTTPException

from login import get_current_user

aktivität_router = APIRouter(prefix="/Aktivitaet", tags=["Aktivität"], dependencies=[Depends(get_current_user)])


@aktivität_router.get("")
async def read_all():
    return {"message": "This is a test"}

@aktivität_router.post("")
async def create_one(aktivität: neueAktivität):
    return {"message": "This is a test"}

