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
    event_time = peewee.DateTimeField(null=True)
    location = peewee.TextField(null=True)
    section = peewee.TextField(null=True)


class Person(BaseModel):
    created = peewee.DateTimeField(default=datetime.datetime.now)
    name = peewee.TextField()


class StoryPerson(BaseModel):
    created = peewee.DateTimeField(default=datetime.datetime.now)
    story = peewee.ForeignKeyField(Story, related_name='story_people')
    person = peewee.ForeignKeyField(Person, related_name='story_people')

    class Meta:
        primary_key = peewee.CompositeKey('story', 'person')


def connect():
    db.connect()
    db.create_tables([Story, Person, StoryPerson], safe=True)
