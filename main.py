from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from login import authenticate_user, get_current_user, create_access_token
from login import Token, ACCESS_TOKEN_EXPIRE_MINUTES, authError
#from data import router_data
from testing import testing_router
from dbModels import Nutzer
from passlib.context import CryptContext
import logging

from peewee import IntegrityError


#views
from Views.gruppenView import gruppe_router
from Views.aktivitätView import aktivität_router
from Views.teilnahmeView import teilnahme_router
from Views.nachrichtenView import nachrichten_router


# suppress passlib logging
# module 'bcrypt' has no attribute '__about__'
# https://github.com/pyca/bcrypt/issues/684
import logging
logging.getLogger('passlib').setLevel(logging.ERROR)
app = FastAPI(
    title="EasyActivity API",
    description="",
)

#app.include_router(router_data)
app.include_router(testing_router)
app.include_router(gruppe_router)
app.include_router(aktivität_router)
app.include_router(teilnahme_router)
app.include_router(nachrichten_router)

# CORS setup
origins = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",

    "https://easy-activity.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token", responses={401: {"model": authError}, 200: {"model": Token}})
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):  
    try:
        user = authenticate_user(form_data.username, form_data.password)
    except Exception as e:  
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.Nutzername}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "IstEventveranstalter": user.IstEventveranstalter}

class UserCreate(BaseModel):
    anmeldename: str
    passwort: str
    name: str
    vorname: str
    email: str


@app.post("/create-user")
async def create_user(user: UserCreate):
    # if not current_user.adminRolle == 1:
    #     raise HTTPException(status_code=401, detail="Unauthorized")
    
    existing_user = Nutzer.get_or_none(Nutzer.Nutzername == user.anmeldename)
    if existing_user:
        return {"message": "User already exists"}
    if len(user.passwort) < 8:
        return Response(
            status_code=400, content="Password must be at least 8 characters long"
        )
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(user.passwort)
    try:
        Nutzer.create(
            Nutzername=user.anmeldename,
            Passwort=hashed_password,
            Nachname=user.name,
            Vorname=user.vorname,
            Email=user.email,
            IstEventveranstalter=False

        )
        return {"message": "Nutzer erfolgreich erstellt"}
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Die Email ist bereits registriert")

@app.patch("/patch-user")
async def patch_user(username: str, status: str, current_user: dict = Depends(get_current_user)):
    if not current_user.adminRolle == 1:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    user = Nutzer.get_or_none(Nutzer.Nutzername == username)
    if not user:
        return {"message": "User does not exist"}
    if status not in ["active", "locked"]:
        return {"message": "Invalid status"}
    
    user.gesperrt = status == "locked"
    user.save()
    return {"message": "User status updated successfully"}