import datetime
import json

import falcon

from pipeline.api import models, schemas

def json_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError('{} is not JSON serializable'.format(type(obj)))

def json_dump(data):
    return json.dumps(data, default=json_serializer)

def json_load(data):
    try:
        return json.loads(data)
    except json.decoder.JSONDecodeError:
        raise falcon.HTTPBadRequest(None, 'invalid JSON')

stories_schema = schemas.StorySchema(many=True)
story_schema = schemas.StorySchema()
people_schema = schemas.PersonSchema(many=True)
person_schema = schemas.PersonSchema()

class StoriesResource:

    def on_get(self, req, resp):
        stories = models.Story.select()
        result = stories_schema.dump(stories)

        resp.body = json_dump(result.data)

    def on_post(self, req, resp):
        data = json_load(req.stream.read().decode('utf-8'))
        data, errors = story_schema.load(data)
        if errors:
            raise falcon.HTTPBadRequest(None, errors)

        story = models.Story.create(**data)
        result = story_schema.dump(story)

        resp.body = json_dump(result.data)


class StoryResource:

    def on_get(self, req, resp, story_id):
        try:
            story = models.Story.get(id=story_id)
        except models.Story.DoesNotExist:
            resp.body = json.dumps({'message': 'Story does not exist'})
            raise falcon.HTTPNotFound()

        result = story_schema.dump(story)
        resp.body = json_dump(result.data)

    def on_post(self, req, resp, story_id):
        try:
            story = models.Story.get(id=story_id)
        except models.Story.DoesNotExist:
            resp.body = json.dumps({'message': 'Story does not exist'})
            raise falcon.HTTPNotFound()

        data = json_load(req.stream.read().decode('utf-8'))
        data, errors = story_schema.load(data, partial=True)
        if errors:
            raise falcon.HTTPBadRequest(None, errors)

        for field, value in data.items():
            setattr(story, field, value)

        data, errors = story_schema.dump(story)
        if errors:
            raise falcon.HTTPBadRequest(None, errors)
        story.save()

        resp.body = json_dump(data)


class PeopleResource:

    def on_get(self, req, resp):
        people = models.Person.select()
        result = people_schema.dump(people)

        resp.body = json_dump(result.data)

    def on_post(self, req, resp):
        data = json_load(req.stream.read().decode('utf-8'))
        data, errors = person_schema.load(data)
        if errors:
            raise falcon.HTTPBadRequest(None, errors)

        person = models.Person.create(**data)
        result = person_schema.dump(person)

        resp.body = json_dump(result.data)


class PersonResource:

    def on_get(self, req, resp, person_id):
        try:
            person = models.Person.get(id=person_id)
        except models.Person.DoesNotExist:
            resp.body = json.dumps({'message': 'Person does not exist'})
            raise falcon.HTTPNotFound()

        result = person_schema.dump(person)
        resp.body = json_dump(result.data)

    def on_post(self, req, resp, person_id):
        try:
            person = models.Person.get(id=person_id)
        except models.Person.DoesNotExist:
            resp.body = json.dumps({'message': 'Person does not exist'})
            raise falcon.HTTPNotFound()

        data = json_load(req.stream.read().decode('utf-8'))
        data, errors = person_schema.load(data, partial=True)
        if errors:
            raise falcon.HTTPBadRequest(None, errors)

        for field, value in data.items():
            setattr(person, field, value)

        data, errors = person_schema.dump(person)
        if errors:
            raise falcon.HTTPBadRequest(None, errors)
        person.save()

        resp.body = json_dump(data)


models.connect()

api = falcon.API()
api.add_route('/stories', StoriesResource())
api.add_route('/stories/{story_id}', StoryResource())
api.add_route('/people', PeopleResource())
api.add_route('/people/{person_id}', PersonResource())
