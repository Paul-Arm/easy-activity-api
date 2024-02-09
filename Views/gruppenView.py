from fastapi import APIRouter, Depends, HTTPException, status
from peewee import DoesNotExist
from playhouse.shortcuts import model_to_dict
from pydantic import BaseModel

from dbModels import Nutzer, Gruppe, NutzerGruppe, database
from pydanticModels import Gruppe as GruppeSchema
from pydanticModels import NeueGruppe
from login import get_current_user

gruppe_router = APIRouter(
    prefix="/Gruppen",
    tags=["Gruppen"],
    dependencies=[Depends(get_current_user)],
    responses={
        404: {"description": "Not found"},
        403: {"description": "Forbidden"},
        400: {"description": "Bad Request"},
        500: {"description": "Internal Server Error"}
    }
)

class UserInviteRequest(BaseModel):
    user_id: int


@gruppe_router.post("", status_code=status.HTTP_201_CREATED)
async def create_group(
    group_data: NeueGruppe, 
    current_user: Nutzer = Depends(get_current_user)
):
    try:
        with database.atomic():
            new_group = Gruppe.create(
                Gruppenname=group_data.Gruppenname,
                ErstellerID=current_user.NutzerID
            )
            NutzerGruppe.create(
                NutzerID=current_user.NutzerID,
                GruppeID=new_group.GruppeID,
                Status=True
            )
            return model_to_dict(new_group, recurse=False)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating group: {str(e)}"
        )
@gruppe_router.get("", response_model=list[GruppeSchema])
async def get_my_groups(current_user: Nutzer = Depends(get_current_user)):
    """
    Zeigt alle Gruppen in denen der Nutzer aktives Mitglied ist
    """
    try:
        query = (Gruppe.select()
                 .join(NutzerGruppe)
                 .where(
                     (NutzerGruppe.NutzerID == current_user.NutzerID) &
                     (NutzerGruppe.Status == True)
                 ))
        return [model_to_dict(group, recurse=False) for group in query]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler beim Abrufen der Gruppen: {str(e)}"
        )

@gruppe_router.get("/Einladungen", response_model=list[GruppeSchema])
async def get_pending_invitations(current_user: Nutzer = Depends(get_current_user)):
    """
    Zeigt alle ausstehenden Gruppeneinladungen des Nutzers
    """
    try:
        pending_invites = (NutzerGruppe.select(Gruppe)
                           .join(Gruppe)
                           .where(
                               (NutzerGruppe.NutzerID == current_user.NutzerID) &
                               (NutzerGruppe.Status == False)
                           ))
        
        return [model_to_dict(invite.gruppe_id, recurse=False) for invite in pending_invites]
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fehler beim Abrufen der Einladungen: {str(e)}"
        )

@gruppe_router.get("/{group_id}", response_model=GruppeSchema)
async def get_group_details(
    group_id: int, 
    current_user: Nutzer = Depends(get_current_user)
):
    try:
        NutzerGruppe.get(
            (NutzerGruppe.NutzerID == current_user.NutzerID) &
            (NutzerGruppe.GruppeID == group_id) &
            (NutzerGruppe.Status == True)
        )
        group = Gruppe.get(Gruppe.GruppeID == group_id)
        return model_to_dict(group, recurse=False)
    except NutzerGruppe.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this group"
        )
    except Gruppe.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@gruppe_router.post("/{group_id}/invite")
async def invite_user(
    group_id: int,
    invite_data: UserInviteRequest,
    current_user: Nutzer = Depends(get_current_user)
):
    try:
        group = Gruppe.get(Gruppe.GruppeID == group_id)
        
        #TODO: richtig ?
        # if group.ErstellerID_id != current_user.NutzerID:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Only group creator can invite users"
        #     )
        
        user_to_invite = Nutzer.get(Nutzer.NutzerID == invite_data.user_id)
        
        if NutzerGruppe.get_or_none(
            (NutzerGruppe.NutzerID == invite_data.user_id) &
            (NutzerGruppe.GruppeID == group_id)
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already has pending invitation or is member"
            )
        
        NutzerGruppe.create(
            NutzerID=invite_data.user_id,
            GruppeID=group_id,
            Status=False
        )
        return {"message": "Invitation sent successfully"}
    
    except Nutzer.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except Gruppe.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to process request: {str(e)}"
        )


@gruppe_router.post("/{group_id}/join")
async def join_group(
    group_id: int,
    current_user: Nutzer = Depends(get_current_user)
):
    try:
        invitation = NutzerGruppe.get(
            (NutzerGruppe.NutzerID == current_user.NutzerID) &
            (NutzerGruppe.GruppeID == group_id) &
            (NutzerGruppe.Status == False)
        )
        invitation.Status = True
        invitation.save()
        return {"message": "Successfully joined group"}
    except NutzerGruppe.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No pending invitation found"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@gruppe_router.post("/{group_id}/leave")
async def leave_group(
    group_id: int,
    current_user: Nutzer = Depends(get_current_user)
):
    try:
        membership = NutzerGruppe.get(
            (NutzerGruppe.NutzerID == current_user.NutzerID) &
            (NutzerGruppe.GruppeID == group_id) &
            (NutzerGruppe.Status == True)
        )
        membership.delete_instance()
        
        group = Gruppe.get(Gruppe.GruppeID == group_id)
        if group.ErstellerID_id == current_user.NutzerID:
            group.ErstellerID = None
            group.save()
        
        return {"message": "Successfully left group"}
    
    except NutzerGruppe.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this group"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )