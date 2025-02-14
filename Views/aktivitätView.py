from pydanticModels import neueAktivität
from dbModels import  Aktivität
import logging


from fastapi import APIRouter, Depends, HTTPException

from login import get_current_user

aktivität_router = APIRouter(prefix="/Aktivitaet", tags=["Aktivität"], dependencies=[Depends(get_current_user)])


@aktivität_router.get("")
async def read_all():
    return {"message": "This is a test"}

@aktivität_router.post("")
async def create_one(aktivität: neueAktivität):
    logging.info(aktivität)
    return {"message": "ok", "data": aktivität.model_dump()}

