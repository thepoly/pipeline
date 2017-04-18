import marshmallow


class StorySchema(marshmallow.Schema):
    id = marshmallow.fields.Int(dump_only=True)
    title = marshmallow.fields.Str(required=True)
    created = marshmallow.fields.DateTime(dump_only=True)
    event_time = marshmallow.fields.DateTime(allow_none=True)
    location = marshmallow.fields.Str(allow_none=True)
    section = marshmallow.fields.Str(allow_none=True)

    @marshmallow.post_dump(pass_many=True)
    def wrap(self, data, many):
        key = 'stories' if many else 'story'
        return {key: data}


class PersonSchema(marshmallow.Schema):
    id = marshmallow.fields.Int(dump_only=True)
    name = marshmallow.fields.Str(required=True)
    slack_handle = marshmallow.fields.Str(allow_none=True)
    slack_id = marshmallow.fields.Str(allow_none=True)

    @marshmallow.post_dump(pass_many=True)
    def wrap(self, data, many):
        key = 'people' if many else 'person'
        return {key: data}


class PhotoSchema(marshmallow.Schema):
    id = marshmallow.fields.Int(dump_only=True)
    created = marshmallow.fields.DateTime(dump_only=True)
    mime_type = marshmallow.fields.Str(dump_only=True)

    @marshmallow.post_dump(pass_many=True)
    def wrap(self, data, many):
        key = 'photos' if many else 'photo'
        return {key: data}


class AddStoryPersonSchema(marshmallow.Schema):
    id = marshmallow.fields.Int()

    @marshmallow.post_dump(pass_many=True)
    def wrap(self, data, many):
        key = 'story_people' if many else 'story_person'
        return {key: data}


class AddStoryPhotoSchema(marshmallow.Schema):
    id = marshmallow.fields.Int()

    @marshmallow.post_dump(pass_many=True)
    def wrap(self, data, many):
        key = 'story_photo' if many else 'story_photo'
        return {key: data}
