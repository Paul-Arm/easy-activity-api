from typing import Optional
from pydantic import BaseModel
import datetime


class UserCreate(BaseModel):
    anmeldename: str
    passwort: str
    name: str
    vorname: str
    email: str


class Nutzer(BaseModel):
    Nutzername: str
    Passwort: str
    Email: str
    Nachname: str
    Vorname: str
    IstEventveranstalter: bool


class Gruppe(BaseModel):
    GruppeID: int
    Gruppenname: str
class NeueGruppe(BaseModel):
    Gruppenname: str

class GruppeSchema(BaseModel):
    Gruppenname: str

    class Config:
        orm_mode = True

class Adresse(BaseModel):
    Straße: str
    Hausnummer: str
    Postleitzahl: str
    Ort: str
    Staat: str




class neueAktivität(BaseModel):
    Abstimmungsende: Optional[str] = None
    Adresse: Adresse
    Beschreibung: Optional[str] = None
    Endzeitpunkt: Optional[str] = None
    Ortsabstimmung: int
    Zeitabstimmung: int
    Startzeitpunkt: str
    Titel: str
    Zusagenende: Optional[str] = None
    ZeitAlsSchnittmenge: Optional[bool] = None
    OffenesEnde: bool

class TeilnahmeModel(BaseModel):
    NutzerID: int
    AktivitätID: int
    StimmtZu: bool


class NeueNachricht(BaseModel):
    Inhalt: str
    GruppenID: int

class NachrichtenSchema(BaseModel):
    NachrichtenID: int
    Inhalt: str
    GruppenID: int
    NutzerID: int
    Zeitstempel: datetime.datetime

