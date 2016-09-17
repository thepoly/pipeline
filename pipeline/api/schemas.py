import marshmallow


class StorySchema(marshmallow.Schema):
    id = marshmallow.fields.Int(dump_only=True)
    title = marshmallow.fields.Str(required=True)
    created = marshmallow.fields.DateTime(dump_only=True)

    @marshmallow.post_dump(pass_many=True)
    def wrap(self, data, many):
        key = 'stories' if many else 'story'
        return {key: data}


class PersonSchema(marshmallow.Schema):
    id = marshmallow.fields.Int(dump_only=True)
    name = marshmallow.fields.Str(required=True)

    @marshmallow.post_dump(pass_many=True)
    def wrap(self, data, many):
        key = 'people' if many else 'person'
        return {key: data}
