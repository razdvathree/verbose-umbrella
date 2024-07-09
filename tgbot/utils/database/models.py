from peewee import SqliteDatabase, Model, TextField, IntegerField

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db


class Notes(BaseModel):
    id = IntegerField(primary_key=True)
    note_content = TextField()

    class Meta:
        db_table = "notes"

