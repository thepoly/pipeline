import json

import falcon

import models
import schemas
import api_util


people_schema = schemas.PersonSchema(many=True)
person_schema = schemas.PersonSchema()


class PeopleResource:

    def on_get(self, req, resp):
        people = models.Person.select()
        result = people_schema.dump(people)

        resp.body = api_util.json_dump(result.data)

    def on_post(self, req, resp):
        data = api_util.json_load(req.stream.read().decode('utf-8'))
        data, errors = person_schema.load(data)
        if errors:
            raise falcon.HTTPBadRequest(None, errors)

        person = models.Person.create(**data)
        result = person_schema.dump(person)

        resp.body = api_util.json_dump(result.data)


class PersonResource:

    def on_get(self, req, resp, person_id):
        try:
            person = models.Person.get(id=person_id)
        except models.Person.DoesNotExist:
            resp.body = json.dumps({'message': 'Person does not exist'})
            raise falcon.HTTPNotFound()

        result = person_schema.dump(person)
        resp.body = api_util.json_dump(result.data)

    def on_put(self, req, resp, person_id):
        try:
            person = models.Person.get(id=person_id)
        except models.Person.DoesNotExist:
            resp.body = json.dumps({'message': 'Person does not exist'})
            raise falcon.HTTPNotFound()

        data = api_util.json_load(req.stream.read().decode('utf-8'))
        data, errors = person_schema.load(data, partial=True)
        if errors:
            raise falcon.HTTPBadRequest(None, errors)

        for field, value in data.items():
            setattr(person, field, value)

        data, errors = person_schema.dump(person)
        if errors:
            raise falcon.HTTPBadRequest(None, errors)
        person.save()

        resp.body = api_util.json_dump(data)
