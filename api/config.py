import models


class AppConfig:

    default_settings = {
        'slack_api_key': None,
        'slack_notification_channel': None
    }

    def __init__(self):
        # ensure our tables have been created and a DB connection established
        models.connect()

        # create default config
        self.create_settings()

    def create_settings(self):
        for s_key, s_val in self.default_settings.items():
            models.Setting.create_or_get(key=s_key, value=s_val)

    def __getattr__(self, item):
        try:
            setting = models.Setting.get(models.Setting.key == item)
        except models.Setting.NotFoundError:
            raise
        return setting.value

    def __setattr__(self, item, value):
        setting = models.Setting.get(models.Setting.key == item)
        setting.value = value
        setting.save()
