from peewee import *

db = MySQLDatabase( host="77.90.57.155", port=6123, user="root", password="oNdTxtvWfsflpvmMcJ5ibmkD7O1abNTli5iwTUXojeV05XjOuqxrO2oxxFU42E9r", database="EasyActivaty")
#"mysql://mariadb:65XzK62h2wNZgBN9Ca95S1ylSFM9oAUQ0mKkeboe0sQKQpn5J4LCkZrzd0mLq349@77.90.57.155:6123/default"
db.connect()

class Nutzer(Model):

    class Meta:
        database = db
        table_name = "Nutzer"
    
    NutzerID = AutoField()
    Nutzername  = CharField()
    Passwort = CharField()
    Email = CharField(column_name="E-mail")
    Nachname = CharField(null=True)
    Vorname  = CharField()

