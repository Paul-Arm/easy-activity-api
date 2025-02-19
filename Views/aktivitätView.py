from pydanticModels import neueAktivität
from pydanticModels import Adresse as AdresseSchema
from pydantic import BaseModel
from dbModels import  Aktivität, Adresse, EventOrtVorschlag, EventZeitVorschlag , Nutzer, database, Gruppe
import logging

from peewee import JOIN
from typing import List, Optional
from datetime import datetime
from fastapi import status


from fastapi import APIRouter, Depends, HTTPException
from peewee import fn

# IntegrityError
from peewee import IntegrityError

from login import get_current_user

aktivität_router = APIRouter(prefix="/Aktivitaet", tags=["Aktivität"], dependencies=[Depends(get_current_user)])


# Pydantic Modelle
class AdresseSchema(BaseModel):
    Straße: str
    Hausnummer: str
    Postleitzahl: str
    Ort: str
    Staat: str

class AktivitätCreate(BaseModel):
    Titel: str
    Beschreibung: Optional[str] = None
    Adresse: Optional[AdresseSchema] = None
    Startzeitpunkt: Optional[datetime] = None
    Endzeitpunkt: Optional[datetime] = None
    Ortsabstimmung: bool = False
    Zeitabstimmung: bool = False
    GruppeID: Optional[int] = None
    Abstimmungsende: Optional[datetime] = None
    ZeitAlsSchnittmenge: Optional[bool] = None
    OffenesEnde: bool

class ZeitVorschlagCreate(BaseModel):
    Startzeit: datetime
    Endzeit: datetime


@aktivität_router.get("", response_model=list)
async def get_Public_Activities():
    """Gibt alle öffentlichen Aktivitäten zurück"""
    activities = (
        Aktivität
        .select(Aktivität, Adresse)
        .join(Adresse, JOIN.LEFT_OUTER, on=(Aktivität.Adresse == Adresse.AdresseID))
        .where(Aktivität.Gruppe == None) #TODO: ?
        .dicts()
    )

    return list(activities)

@aktivität_router.get("/MeineAktivitaeten", response_model=list)
async def read_my(current_user: dict = Depends(get_current_user)):
    """Gibt alle Aktivitäten des aktuellen Nutzers zurück"""
    user_id = current_user.NutzerID
    
    AdresseAlias = Adresse.alias("adr")  # Alias für die Adresse-Tabelle

    activities = (
        Aktivität
        .select(Aktivität, AdresseAlias)  
        .join(AdresseAlias, JOIN.LEFT_OUTER, on=(Aktivität.Adresse == AdresseAlias.AdresseID))  # Correct JOIN syntax
        .where(Aktivität.ErstellerID == user_id)
        .dicts()
    )

    return list(activities)  # Explizit in eine Liste umwandeln







# Endpunkte
@aktivität_router.post("", status_code=status.HTTP_201_CREATED)
async def create_activity(
    activity: AktivitätCreate,
    current_user: Nutzer = Depends(get_current_user)):
    """Erstellt eine neue Aktivität"""

    with database.atomic():
        adresse_id = None
        if activity.Adresse and not activity.Ortsabstimmung:
            adresse, _ = Adresse.get_or_create(**activity.Adresse.dict())
            adresse_id = adresse.AdresseID


        if (activity.GruppeID ):
            gr = Gruppe.get_or_none(Gruppe.GruppeID == activity.GruppeID)
            if not gr:
                raise HTTPException(status_code=404, detail="Gruppe {} nicht gefunden".format(activity.GruppeID))

            neue_aktivitaet = Aktivität.create(
                Titel=activity.Titel,
                Beschreibung=activity.Beschreibung,
                Adresse=adresse_id,
                Startzeitpunkt=activity.Startzeitpunkt,
                Endzeitpunkt=activity.Endzeitpunkt,
                Ortsabstimmung=activity.Ortsabstimmung,
                Zeitabstimmung=activity.Zeitabstimmung,
                Ersteller=current_user.NutzerID,
                Gruppe=activity.GruppeID,
                Abstimmungsende=activity.Abstimmungsende,
                ZeitAlsSchnittmenge=activity.ZeitAlsSchnittmenge,
                OffenesEnde=activity.OffenesEnde,
                Status=0,
                
            )
        else:
            if not current_user.IstEventveranstalter:
                raise HTTPException(status_code=400, detail="Nur Eventveranstalter können öffentliche Aktivitätenerstellen")
            
            neue_aktivitaet = Aktivität.create(
            Titel=activity.Titel,
            Beschreibung=activity.Beschreibung,
            Adresse=adresse_id,
            Startzeitpunkt=activity.Startzeitpunkt,
            Endzeitpunkt=activity.Endzeitpunkt,
            Ortsabstimmung=activity.Ortsabstimmung,
            Zeitabstimmung=activity.Zeitabstimmung,
            Ersteller=current_user.NutzerID,
            Abstimmungsende=activity.Abstimmungsende,
            ZeitAlsSchnittmenge=activity.ZeitAlsSchnittmenge,
            OffenesEnde=activity.OffenesEnde
        )            
        
        return {"id": neue_aktivitaet.AktivitätID}


@aktivität_router.patch("/{id}")
async def update_activity(
    id: int,
    activity: AktivitätCreate,
    current_user: Nutzer = Depends(get_current_user)
):
    with database.atomic():
        aktivität = Aktivität.get_or_none(Aktivität.AktivitätID == id)
        if not aktivität:
            raise HTTPException(status_code=404, detail="Aktivität {} nicht gefunden".format(id))

        adresse_id = None
        # Adresse erstellen falls geändert und fals Ortsabstimmung nicht aktiv
        if activity.Adresse and not activity.Ortsabstimmung:
            adresse, _ = Adresse.get_or_create(**activity.Adresse.dict())
            adresse_id = adresse.AdresseID

        aktivität.Titel = activity.Titel
        aktivität.Beschreibung = activity.Beschreibung
        aktivität.Adresse = adresse_id
        aktivität.Startzeitpunkt = activity.Startzeitpunkt
        aktivität.Endzeitpunkt = activity.Endzeitpunkt
        aktivität.Ortsabstimmung = activity.Ortsabstimmung
        aktivität.Zeitabstimmung = activity.Zeitabstimmung
        aktivität.Abstimmungsende = activity.Abstimmungsende
        aktivität.OffenesEnde = activity.OffenesEnde
        aktivität.ZeitAlsSchnittmenge = activity.ZeitAlsSchnittmenge
        aktivität.save()

        return aktivität

@aktivität_router.post("/{id}/Ortvorschlag")
async def create_ortvorschlag(
    activity_id: int,
    adresse: AdresseSchema,
    current_user: Nutzer = Depends(get_current_user)
):
    aktivität = Aktivität.get_or_none(Aktivität.AktivitätID == activity_id)
    if not aktivität or not aktivität.Ortsabstimmung:
        raise HTTPException(status_code=400, detail="Ortsabstimmung nicht aktiv")

    with database.atomic():
        db_adresse = Adresse.create(**adresse.dict())
        vorschlag = EventOrtVorschlag.create(
            AktivitätID=activity_id,
            AdresseID=db_adresse.AdresseID,
            ErstellerID=current_user.NutzerID
        )
        return {"vorschlag_id": vorschlag.VorschlagID}

@aktivität_router.get("/{id}/Ortvorschlaege")
async def get_ortvorschlaege(activity_id: int):
    res = (EventOrtVorschlag.filter(AktivitätID=activity_id)
           .join(Adresse, on=(EventOrtVorschlag.AdresseID == Adresse.AdresseID), attr='AdresseID')
           .join(Nutzer, on=(EventOrtVorschlag.ErstellerID == Nutzer.NutzerID))
           .group_by(EventOrtVorschlag.AdresseID)
           .select(EventOrtVorschlag, Adresse, Nutzer.Nutzername, fn.COUNT(EventOrtVorschlag.AdresseID).alias('votes'))
           .order_by('votes')
           .dicts()
           )
           
    return [v for v in res]

@aktivität_router.post("/{id}/Zeitvorschlag")
async def create_zeitvorschlag(
    activity_id: int,
    zeit: ZeitVorschlagCreate,
    current_user: Nutzer = Depends(get_current_user)
):
    aktivität = Aktivität.get_or_none(Aktivität.AktivitätID == activity_id)
    if not aktivität or not aktivität.Zeitabstimmung:
        raise HTTPException(status_code=400, detail="Zeitabstimmung nicht aktiv")

    with database.atomic():
        vorschlag = EventZeitVorschlag.create(
            AktivitätID=activity_id,
            Startzeit=zeit.Startzeit,
            Endzeit=zeit.Endzeit,
            ErstellerID=current_user.NutzerID
        )
        return {"vorschlag_id": vorschlag.VorschlagID}

@aktivität_router.get("/{id}/Zeitvorschlaege", response_model=List[dict])
async def get_zeitvorschlaege(activity_id: int):
    # query = (EventZeitVorschlag
    #     .select(
    #         EventZeitVorschlag,
    #         Nutzer.Nutzername,
    #         fn.COUNT(EventZeitVorschlag.Nutzer).alias('votes')
    #     .join(Nutzer)
    #     .left_join(EventZeitVorschlag)
    #     .where(EventZeitVorschlag.Aktivität == activity_id)
    #     .group_by(EventZeitVorschlag.VorschlagID)
    #     .order_by(fn.COUNT(EventZeitVorschlag.ErstellerID).desc())))
    
    res = (EventZeitVorschlag.filter(AktivitätID=activity_id)
           .join(Nutzer, on=(EventZeitVorschlag.ErstellerID == Nutzer.NutzerID))
           .select(EventZeitVorschlag, Nutzer.Nutzername, fn.COUNT(fn.CONCAT(EventZeitVorschlag.Startzeit, EventZeitVorschlag.Endzeit)).alias('votes'))
           .group_by(EventZeitVorschlag.Startzeit, EventZeitVorschlag.Endzeit)

           .dicts()
           )
           
    return [v for v in res]