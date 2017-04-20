import io
import json

import falcon
import magic

import models
import schemas
import api_util


photos_schema = schemas.PhotoSchema(many=True)
photo_schema = schemas.PhotoSchema()


class PhotosResource:

    def on_get(self, req, resp):
        photos = models.Photo.select()
        result = photos_schema.dump(photos)

        resp.body = api_util.json_dump(result.data)

    def on_post(self, req, resp):
        data = req.stream.read()
        mime_type = magic.from_buffer(data[:1024], mime=True)

        photo = models.Photo.create(photo=data, mime_type=mime_type)
        result = photo_schema.dump(photo)

        resp.body = api_util.json_dump(result.data)


class PhotoResource:

    def on_get(self, req, resp, photo_id):
        try:
            photo = models.Photo.get(id=photo_id)
        except models.Photo.DoesNotExist:
            resp.body = json.dumps({'message': 'Photo does not exist'})
            raise falcon.HTTPNotFound()

        resp.content_type = photo.mime_type
        resp.stream = io.BytesIO(photo.photo)
