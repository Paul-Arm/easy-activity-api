from pydanticModels import neueAktivität
from dbModels import  Aktivität, Adresse
import logging

from peewee import JOIN

from fastapi import APIRouter, Depends, HTTPException

from login import get_current_user

aktivität_router = APIRouter(prefix="/Aktivitaet", tags=["Aktivität"], dependencies=[Depends(get_current_user)])


@aktivität_router.get("", response_model=dict)
async def read_all():
    activities = [ a for a in Aktivität.select().dicts()]
    return {"content": activities}

@aktivität_router.get("/MeineAktivitaeten", response_model=list)
async def read_my(current_user: dict = Depends(get_current_user)):
    user_id = current_user.NutzerID
    
    AdresseAlias = Adresse.alias("adr")  # Alias für die Adresse-Tabelle

    activities = (
        Aktivität
        .select(Aktivität, AdresseAlias)  
        .join(AdresseAlias, JOIN.LEFT_OUTER, on=(Aktivität.Adresse == AdresseAlias.AdresseID))  # Correct JOIN syntax
        .where(Aktivität.Ersteller == user_id)
        .dicts()
    )

    return list(activities)  # Explizit in eine Liste umwandeln



@aktivität_router.post("")
async def create_one(aktivität: neueAktivität, current_user: dict = Depends(get_current_user)):

    # Adresse erstellen falls nicht vorhanden

    adresse, created = Adresse.get_or_create(
        Straße=aktivität.Adresse.Straße,
        Hausnummer=aktivität.Adresse.Hausnummer,
        Postleitzahl=aktivität.Adresse.Postleitzahl,
        Ort=aktivität.Adresse.Ort,
        Staat=aktivität.Adresse.Staat
    )



    # Aktivität erstellen
    user_id = current_user.NutzerID
    # if current_user.IstEventveranstalter:
    #     groupe_id = None
    # else:
    #     groupe_id = "1" #TODO: Gruppe des Nutzers holen
    groupe_id = "1"
    aktivität = Aktivität.create(
        Titel=aktivität.Titel,
        Beschreibung=aktivität.Beschreibung,
        Adresse=adresse.AdresseID,
        Startzeitpunkt=aktivität.Startzeitpunkt,
        Endzeitpunkt=aktivität.Endzeitpunkt,
        ErstellerID=user_id,
        GruppeID=groupe_id,

    )


    return {"message": "ok"}
