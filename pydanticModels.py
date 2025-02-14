from typing import Optional
from pydantic import BaseModel

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

class Adresse(BaseModel):
    Straße: str
    Hausnummer: str
    Postleitzahl: str
    Ort: str
    Staat: str





class neueAktivität(BaseModel):
    Abstimmungsende: Optional[str] = None
    Adresse: Adresse
    Beschreibung: str
    Endzeitpunkt: Optional[str] = None
    Ortsabstimmung: int
    Zeitabstimmung: int
    Startzeitpunkt: str
    Titel: str
    Zusagenende: str
