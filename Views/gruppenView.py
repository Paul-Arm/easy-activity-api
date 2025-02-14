from pydantic import BaseModel
from fastapi import APIRouter

from pydanticModels import Gruppe as GruppeSchema
from fastapi import Depends
from login import get_current_user





gruppe_router = APIRouter(
    prefix="/Gruppe",
    tags=["Gruppe"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"},
               401: {"description": "Unauthorized"},
               200: {"description": "Success"},
               201: {"description": "Created"},
               403: {"description": "Forbidden"},
               500: {"description": "Internal Server Error"}},
)


@gruppe_router.get("")
async def read_all():
    return {"message": "This is a test"}

@gruppe_router.post("")
async def create_one(gruppe: GruppeSchema):
    return {"message": "This is a test"}


@gruppe_router.get("/{id}")
async def read_one(id: int):
    return {"message": "This is a test {}".format(id)}


@gruppe_router.post("/{id}/addUser")
async def add_user_to_group(id: int, user_id: int):
    return {"message": "add user {} to group {}".format(user_id, id)}


@gruppe_router.post("/{id}/removeSelf")
async def remove_self_from_group(id: int, current_user: dict = Depends(get_current_user)):
    user_id = current_user.NutzerID
    return {"message": "remove user {} from group {}".format(user_id, id)}