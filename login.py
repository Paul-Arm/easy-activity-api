from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status

import os
from dbModels import Nutzer

# Secret key for JWT encoding/decoding
SECRET_KEY = "secret_key" #TODO: os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str
    IstEventVeranstalter: bool

class TokenData(BaseModel):
    username: str | None = None
    roll: str | None = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    try:
        user = Nutzer.get(Nutzer.Nutzername == username)
        return user
    except Nutzer.DoesNotExist:
        return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nutzer nicht gefunden",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # if user.gesperrt:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Account ist gesperrt, bitte kontaktieren Sie den Administrator",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # if user.anmeldeversuche >= 3:
    #     # Lock the user
    #     user.gesperrt = True
    #     user.save()
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Account wurde durch zu viele fasche versuche gesperrt, bitte kontaktieren Sie den Administrator",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
        
    if not verify_password(password, user.Passwort):
        # Increase login attempts
        user.anmeldeversuche += 1
        user.save()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falsches Passwort, noch " + str(3 - user.anmeldeversuche) + " Versuche",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        # Reset login attempts
        user.anmeldeversuche = 0
        user.save()
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    to_encode.update({"roll": "user"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    # gets the user and verifies the token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, roll=payload.get("roll"))
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user