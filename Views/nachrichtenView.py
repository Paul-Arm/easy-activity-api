from fastapi import APIRouter, Depends, HTTPException, status
from login import get_current_user
import datetime
from dbModels import Nutzer, Nachrichten, NutzerGruppe

from pydanticModels import NeueNachricht, NachrichtenSchema





nachrichten_router = APIRouter(prefix="/Nachrichten", tags=["Nachrichten"], dependencies=[Depends(get_current_user)])

@nachrichten_router.get("", response_model=list[NachrichtenSchema])
async def get_meine_nachrichten(GruppenID: int , current_user: Nutzer = Depends(get_current_user)):
    """
    Zeigt alle in einer gruppe
    """
    try:
        if GruppenID:

            nutzer_gruppe = NutzerGruppe.get_or_none(NutzerGruppe.NutzerID == current_user.NutzerID, NutzerGruppe.GruppeID == GruppenID)
            if not nutzer_gruppe:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Du bist entweder kein Teilnehmer dieser Gruppe oder diese Gruppe existiert nicht"
                )
            res = (Nachrichten.select()
                 .where(Nachrichten.GruppenID == GruppenID)
                 .dicts()
                 )
        else:
            
            return {"message": "GruppenID fehlt"}
        return [r for r in res]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error getting Nachrichten: {str(e)}"
        )


@nachrichten_router.post("", status_code=status.HTTP_201_CREATED, response_model=dict)
async def send_message(message: NeueNachricht, current_user: Nutzer = Depends(get_current_user)):
    """
    sende eine Nachricht
    """
    try:
        nutzer_gruppe = NutzerGruppe.get_or_none(NutzerGruppe.NutzerID == current_user.NutzerID, NutzerGruppe.GruppeID == message.GruppenID)
        if not nutzer_gruppe:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Du bist entweder nicht in der Gruppe oder diese Gruppe existiert nicht"
            )
        new_message = Nachrichten.create(
            Inhalt=message.Inhalt,
            NutzerID=current_user.NutzerID,
            GruppenID=message.GruppenID,
            Zeitstempel=datetime.datetime.now()
        )
        return {"message": "Nachricht gesendet"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error sending Nachricht: {str(e)}"
        )

