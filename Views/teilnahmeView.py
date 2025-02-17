from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status
from login import get_current_user

from dbModels import Nutzer, Teilnehmer, database, Aktivität
from pydanticModels import TeilnahmeModel








teilnahme_router = APIRouter(prefix="/Teilnahme", tags=["Teilnahme"], dependencies=[Depends(get_current_user)])

@teilnahme_router.get("/{aktivitaet_id}/")
async def get_teilnahmen(aktivitaet_id: int, current_user: Nutzer = Depends(get_current_user)):
    """
    Zeigt alle Teilnahmen an einer Aktivität
    """
    try:
        res = (Teilnehmer.select()
                 .where(Teilnehmer.AktivitätID == aktivitaet_id)
                 .dicts()
                 )
        return res
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error getting Teilnahmen: {str(e)}"
        )


