import datetime

import peewee

db = peewee.SqliteDatabase('pipeline.db')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Story(BaseModel):
    # TODO: id = peewee.UUIDField or something...
    created = peewee.DateTimeField(default=datetime.datetime.now)
    title = peewee.TextField()

def connect():
    db.connect()
    db.create_tables([Story], safe=True)
