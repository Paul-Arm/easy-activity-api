from pydanticModels import neueAktivität
from dbModels import  Aktivität, Adresse
import logging


from fastapi import APIRouter, Depends, HTTPException

from login import get_current_user

aktivität_router = APIRouter(prefix="/Aktivitaet", tags=["Aktivität"], dependencies=[Depends(get_current_user)])


@aktivität_router.get("", response_model=dict)
async def read_all():
    activities = [ a for a in Aktivität.select().dicts()]
    return {"content": activities}

@aktivität_router.post("")
async def create_one(aktivität: neueAktivität, current_user: dict = Depends(get_current_user)):

    # Adresse erstellen falls nicht vorhanden

    adresse , a = Adresse.create(
        Straße=aktivität.Adresse.Straße,
        Hausnummer=aktivität.Adresse.Hausnummer,
        Postleitzahl=aktivität.Adresse.Postleitzahl,
        Ort=aktivität.Adresse.Ort,
        Staat=aktivität.Adresse.Staat
    ).get_or_create()


    # # Aktivität erstellen
    # user_id = current_user.NutzerID
    # aktivität = Aktivität.create(
    #     Titel=aktivität.Titel,
    #     Beschreibung=aktivität.Beschreibung,
    #     Adresse=adresse.AdresseID,
    #     Startzeitpunkt=aktivität.Startzeitpunkt,
    #     Endzeitpunkt=aktivität.Endzeitpunkt,
    #     ErstellerID=user_id,
    #     GruppeID="2",

    # )


    return {"message": "ok"}

