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
    PLZ: str
    Ort: str

class Aktivität(BaseModel):
    GruppeID: int
    Titel: str
    Beschreibung: str
    Adresse: int