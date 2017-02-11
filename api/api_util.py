import datetime
import json

import falcon


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

