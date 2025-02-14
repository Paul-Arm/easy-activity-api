from peewee import *

database = MySQLDatabase('EasyActivaty', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': '77.90.57.155', 'port': 6123, 'user': 'root', 'password': 'oNdTxtvWfsflpvmMcJ5ibmkD7O1abNTli5iwTUXojeV05XjOuqxrO2oxxFU42E9r'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Adresse(BaseModel):
    adresse_id = BigAutoField(column_name='AdresseID')
    breitengrad = CharField(column_name='Breitengrad')
    hausnummer = CharField(column_name='Hausnummer')
    längengrad = CharField(column_name='L├ñngengrad')
    ort = CharField(column_name='Ort')
    postleitzahl = CharField(column_name='Postleitzahl')
    staat = CharField(column_name='Staat')
    straße = CharField(column_name='Stra├ƒe')

    class Meta:
        table_name = 'Adresse'

class Gruppe(BaseModel):
    gruppe_id = BigAutoField(column_name='GruppeID')
    gruppenname = CharField(column_name='Gruppenname')

    class Meta:
        table_name = 'Gruppe'

class Nutzer(BaseModel):
    e__mail = CharField(column_name='E-Mail')
    ist_eventveranstalter = IntegerField(column_name='IstEventveranstalter')
    nachname = CharField(column_name='Nachname')
    nutzer_id = BigAutoField(column_name='NutzerID')
    nutzername = CharField(column_name='Nutzername')
    passwort = CharField(column_name='Passwort')
    vorname = CharField(column_name='Vorname')

    class Meta:
        table_name = 'Nutzer'

class Aktivität(BaseModel):
    abstimmungsende = DateTimeField(column_name='Abstimmungsende', null=True)
    adresse = ForeignKeyField(column_name='AdresseID', field='adresse_id', model=Adresse, null=True, unique=True)
    aktivität_id = BigAutoField(column_name='Aktivit├ñtID')
    beschreibung = CharField(column_name='Beschreibung', null=True)
    endzeitpunkt = DateTimeField(column_name='Endzeitpunkt', null=True)
    ergebnis = TextField(column_name='Ergebnis', null=True)
    ersteller = ForeignKeyField(column_name='ErstellerID', field='nutzer_id', model=Nutzer, unique=True)
    gruppe = ForeignKeyField(column_name='GruppeID', field='gruppe_id', model=Gruppe, unique=True)
    ortsabstimmung = IntegerField(column_name='Ortsabstimmung', null=True)
    startzeitpunkt = DateTimeField(column_name='Startzeitpunkt', null=True)
    status = IntegerField(column_name='Status', null=True)
    titel = CharField(column_name='Titel')
    zeitabstimmung = IntegerField(column_name='Zeitabstimmung', null=True)
    zusagenende = DateTimeField(column_name='Zusagenende', null=True)

    class Meta:
        table_name = 'Aktivität'

