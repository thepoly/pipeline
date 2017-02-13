import json

import falcon

import models
import schemas
import api_util


class SettingsResource:

    def on_get(self, req, resp):
        settings = models.Setting.select()

        settings_dict = {}
        for setting in settings:
            settings_dict[setting.key] = setting.value

        resp.body = api_util.json_dump({'settings': settings_dict})

    def on_put(self, req, resp):
        data = api_util.json_load(req.stream.read().decode('utf-8'))

        # ensure that this is a dict
        if not isinstance(data, dict):
            raise falcon.HTTPBadRequest(None, 'Provide a dictionary')

        # modify each listed setting
        for setting_key, setting_value in data.items():
            try:
                setting = models.Setting.get(key=setting_key)
            except models.Setting.DoesNotExist:
                resp.body = json.dumps({'message': f'Setting {setting_key} does not exist'})
                raise falcon.HTTPNotFound()

            setting.value = setting_value
            setting.save()

        resp.body = api_util.json_dump(data)
