import json

import falcon
import peewee

import models
import schemas
import api_util


people_schema = schemas.PersonSchema(many=True)
person_schema = schemas.PersonSchema()
stories_schema = schemas.StorySchema(many=True)
story_schema = schemas.StorySchema()
add_story_person_schema = schemas.AddStoryPersonSchema()


class StoriesResource:

    def on_get(self, req, resp):
        stories = models.Story.select()

        result = stories_schema.dump(stories)

        resp.body = api_util.json_dump(result.data)

    def on_post(self, req, resp):
        data = api_util.json_load(req.stream.read().decode('utf-8'))
        data, errors = story_schema.load(data)
        if errors:
            raise falcon.HTTPBadRequest(None, errors)

        story = models.Story.create(**data)
        result = story_schema.dump(story)

        resp.body = api_util.json_dump(result.data)


class StoryResource:

    def on_get(self, req, resp, story_id):
        try:
            story = models.Story.get(id=story_id)
        except models.Story.DoesNotExist:
            resp.body = json.dumps({'message': 'Story does not exist'})
            raise falcon.HTTPNotFound()

        result = story_schema.dump(story)
        resp.body = api_util.json_dump(result.data)

    def on_put(self, req, resp, story_id):
        try:
            story = models.Story.get(id=story_id)
        except models.Story.DoesNotExist:
            resp.body = json.dumps({'message': 'Story does not exist'})
            raise falcon.HTTPNotFound()

        data = api_util.json_load(req.stream.read().decode('utf-8'))
        data, errors = story_schema.load(data, partial=True)
        if errors:
            raise falcon.HTTPBadRequest(None, errors)

        for field, value in data.items():
            setattr(story, field, value)

        data, errors = story_schema.dump(story)
        if errors:
            raise falcon.HTTPBadRequest(None, errors)
        story.save()

        resp.body = api_util.json_dump(data)


class StoryPeopleResource:

    def on_get(self, req, resp, story_id):
        try:
            story = models.Story.get(id=story_id)
        except models.Story.DoesNotExist:
            resp.body = json.dumps({'message': 'Story does not exist'})
            raise falcon.HTTPNotFound()

        people = (models.Person.select()
                  .join(models.StoryPerson)
                  .where(models.StoryPerson.story == story))

        result = people_schema.dump(people)
        resp.body = api_util.json_dump(result.data)

    def on_post(self, req, resp, story_id):
        data = api_util.json_load(req.stream.read().decode('utf-8'))
        data, errors = add_story_person_schema.load(data)
        if errors:
            raise falcon.HTTPBadRequest(None, errors)
        person_id = data['id']

        try:
            models.Story.get(id=story_id)
        except models.Story.DoesNotExist:
            resp.body = json.dumps({'message': 'Story does not exist'})
            raise falcon.HTTPNotFound()

        try:
            person = models.Person.get(id=person_id)
        except models.Person.DoesNotExist:
            resp.body = json.dumps({'message': 'Person does not exist'})
            raise falcon.HTTPNotFound()

        try:
            models.StoryPerson.create(story_id=story_id, person_id=person.id)
        except peewee.IntegrityError:
            # person has already been added to this story_id
            raise falcon.HTTPConflict(None, 'Person has already been added to this story')

        self.on_get(req, resp, story_id)
