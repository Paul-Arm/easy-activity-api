

from peewee import *
from peewee import SQL, PrimaryKeyField, Model, AutoField, CharField, DateTimeField, TextField, IntegerField, BooleanField, ForeignKeyField, CompositeKey, MySQLDatabase
import os

pw = os.environ.get("DB_PASSWORD")
if pw is None:
    raise Exception("DB_PASSWORD not set")


database = MySQLDatabase('EasyActivaty', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': '77.90.57.155', 'port': 6123, 'user': 'root', 'password': pw})
database.connect()


class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database



class Nutzer(BaseModel):

    class Meta:
        table_name = "Nutzer"
    
    NutzerID = AutoField()
    Nutzername  = CharField()
    Passwort = CharField()
    Email = CharField(column_name="E-mail")
    Nachname = CharField(null=True)
    Vorname  = CharField()
    IstEventveranstalter = BooleanField(null=False)

class Gruppe(BaseModel):
    
    class Meta:
        table_name = "Gruppe"
    
    GruppeID = AutoField()
    Gruppenname = CharField()
    ErstellerID = ForeignKeyField(Nutzer, column_name='ErstellerID', field='NutzerID', null=True)

class NutzerGruppe(BaseModel):
    NutzerID = ForeignKeyField(Nutzer, column_name='NutzerID')
    GruppeID = ForeignKeyField(Gruppe, column_name='GruppeID')
    Status = BooleanField(null=False)
    class Meta:
        table_name = 'NutzerGruppe'
        primary_key = CompositeKey('NutzerID', 'GruppeID')

class Adresse(BaseModel):
    
    class Meta:
        table_name = "Adresse"
    
    AdresseID = AutoField()
    Straße = CharField()
    Hausnummer = CharField()
    Postleitzahl = CharField()
    Ort = CharField()
    Staat = CharField()

class Aktivität(BaseModel):
    AktivitätID = AutoField( column_name='AktivitaetID')
    Abstimmungsende = DateTimeField(column_name='Abstimmungsende', null=True)
    Adresse = ForeignKeyField(column_name='AdresseID', field='AdresseID', model=Adresse, null=True)
    Beschreibung = CharField(column_name='Beschreibung', null=True)
    Endzeitpunkt = DateTimeField(column_name='Endzeitpunkt', null=True)
    Ergebnis = TextField(column_name='Ergebnis', null=True)
    Ersteller = ForeignKeyField(column_name='ErstellerID', field='NutzerID', model=Nutzer, null=True )
    Gruppe = ForeignKeyField(column_name='GruppeID', field='GruppeID', model=Gruppe, null=True)
    Ortsabstimmung = IntegerField(column_name='Ortsabstimmung', null=True)
    Startzeitpunkt = DateTimeField(column_name='Startzeitpunkt', null=True)
    Status = IntegerField(column_name='Status', null=True)
    Titel = CharField(column_name='Titel')
    Zeitabstimmung = IntegerField(column_name='Zeitabstimmung', null=True)
    Zusagenende = DateTimeField(column_name='Zusagenende', null=True)
    OffenesEnde = BooleanField(column_name='OffenesEnde', null=True)
    ZeitAlsSchnittmenge = BooleanField(column_name='ZeitAlsSchnittmenge', null=True)

    class Meta:
        table_name = 'Aktivitaet'
        
class EventOrtVorschlag(BaseModel):
    VorschlagID = AutoField()
    AktivitätID = ForeignKeyField(Aktivität, column_name='AktivitätID', field="AktivitätID", backref='ortvorschlaege')
    AdresseID = ForeignKeyField(Adresse,column_name='AdresseID'  , field="AdresseID", backref='ortvorschlaege')
    ErstellerID = ForeignKeyField(Nutzer,column_name='ErstellerID', field='NutzerID')
    ErstelltAm = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        table_name = 'EventOrtVorschlag'

class EventZeitVorschlag(BaseModel):
    VorschlagID = AutoField()
    AktivitätID = ForeignKeyField(Aktivität,column_name='AktivitätID', field="AktivitätID", backref='zeitvorschlaege')
    Startzeit = DateTimeField()
    Endzeit = DateTimeField()
    ErstellerID = ForeignKeyField(Nutzer,column_name='ErstellerID', field='NutzerID', backref='zeitvorschlaege')
    ErstelltAm = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        table_name = 'EventZeitVorschlag'


class Teilnehmer(BaseModel):
    NutzerID = ForeignKeyField(Nutzer, column_name='NutzerID', field='NutzerID')
    AktivitätID = ForeignKeyField(Aktivität, column_name='AktivitätID', field='AktivitätID')
    StimmtZu = BooleanField(null=True)
    class Meta:
        table_name = 'Teilnehmer'
        primary_key = CompositeKey('NutzerID', 'AktivitätID')


class Nachrichten(BaseModel):
    NachrichtenID = AutoField()
    GruppenID = ForeignKeyField(Gruppe, column_name='GruppenID', field='GruppeID')
    NutzerID = ForeignKeyField(Nutzer, column_name='NutzerID', field='NutzerID')
    Zeitstempel = DateTimeField()
    Inhalt = TextField()

    class Meta:
        table_name = 'Nachrichten'