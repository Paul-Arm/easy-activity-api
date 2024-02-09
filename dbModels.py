

from peewee import *
from peewee import Model, AutoField, CharField, DateTimeField, TextField, IntegerField, BooleanField, ForeignKeyField, CompositeKey, MySQLDatabase

database = MySQLDatabase('EasyActivaty', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': '77.90.57.155', 'port': 6123, 'user': 'root', 'password': 'oNdTxtvWfsflpvmMcJ5ibmkD7O1abNTli5iwTUXojeV05XjOuqxrO2oxxFU42E9r'})
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
    AktivitätID = AutoField(column_name='AktivitätID', primary_key=True)
    Abstimmungsende = DateTimeField(column_name='Abstimmungsende', null=True)
    Adresse = ForeignKeyField(column_name='AdresseID', field='AdresseID', model=Adresse, null=True, unique=True)
    Beschreibung = CharField(column_name='Beschreibung', null=True)
    Endzeitpunkt = DateTimeField(column_name='Endzeitpunkt', null=True)
    Ergebnis = TextField(column_name='Ergebnis', null=True)
    Ersteller = ForeignKeyField(column_name='ErstellerID', field='NutzerID', model=Nutzer, unique=True)
    Gruppe = ForeignKeyField(column_name='GruppeID', field='GruppeID', model=Gruppe, unique=True)
    Ortsabstimmung = IntegerField(column_name='Ortsabstimmung', null=True)
    Startzeitpunkt = DateTimeField(column_name='Startzeitpunkt', null=True)
    Status = IntegerField(column_name='Status', null=True)
    Titel = CharField(column_name='Titel')
    Zeitabstimmung = IntegerField(column_name='Zeitabstimmung', null=True)
    Zusagenende = DateTimeField(column_name='Zusagenende', null=True)

    class Meta:
        table_name = 'Aktivität'