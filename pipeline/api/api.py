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


models.connect()

api = falcon.API()
api.add_route('/stories', StoriesResource())
