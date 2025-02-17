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


