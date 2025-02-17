from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from login import get_current_user

from dbModels import Nutzer, Teilnehmer, database, Aktivität
from pydanticModels import TeilnahmeModel








teilnahme_router = APIRouter(prefix="/Teilnahme", tags=["Teilnahme"], dependencies=[Depends(get_current_user)])

@teilnahme_router.get("/{aktivitaet_id}/", response_model=list[TeilnahmeModel])
async def get_teilnahmen(aktivitaet_id: int, current_user: Nutzer = Depends(get_current_user)):
    """
    Zeigt alle Teilnahmen an einer Aktivität
    """
    try:
        res = (Teilnehmer.select()
                 .where(Teilnehmer.AktivitätID == aktivitaet_id)
                 .dicts()
                 )
        return [r for r in res]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error getting Teilnahmen: {str(e)}"
        )


@teilnahme_router.get("/meine", response_model=list[TeilnahmeModel])
async def get_meine_teilnahmen(current_user: Nutzer = Depends(get_current_user)):
    """
    Zeigt alle Teilnahmen des Nutzers
    """
    try:
        res = (Teilnehmer.select()
                 .where(Teilnehmer.NutzerID == current_user.NutzerID)
                 .dicts()
                 )
        return [r for r in res]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error getting Teilnahmen: {str(e)}"
        )
    
@teilnahme_router.post("/{aktivitaet_id}/abstimmen", status_code=status.HTTP_201_CREATED)
async def teilnahme_abstimmen(aktivitaet_id: int, teilnahme: bool, current_user: Nutzer = Depends(get_current_user)):
    """
    sage einer Aktivität (des users) zu oder ab
    """
    try:
        a = Aktivität.get_or_none(Aktivität.AktivitätID == aktivitaet_id)
        if a is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aktivität nicht gefunden"
            )
        
        with database.atomic():
            new_teilnahme = Teilnehmer.update(
                NutzerID=current_user.NutzerID,
                AktivitätID=aktivitaet_id,
                StimmtZu=teilnahme
            )
            return {"message": "Teilnahme erfolgreich auf " + str(teilnahme) + " gesetzt"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating Teilnahme: {str(e)}"
        )

        