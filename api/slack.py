import requests
import time
import datetime

import models
import settings


class SlackConnection:
    
    def __init__(self):
        self.baseurl = "https://slack.com/api/"
        self.slack_settings = settings.AppSettings()

    
    def check_connection(self):
        url = self.baseurl + "auth.test"
        data = {'token' : self.slack_settings.slack_api_key}
        r = requests.post(url, data=data)
        
    def post(self, title, time):
        url = self.baseurl + "chat.postMessage"
        data = { 'token' : self.slack_settings.slack_api_key, 'text' : "{} taking place at {} tomorrow".format(title, time), 'channel' : self.slack_settings.slack_notification_channel, 'username' : "Pipeline Bot"}
        r = requests.post(url, data=data)


def get_stories():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    events_tomorrow = models.Story.select().where(models.Story.event_time.day == tomorrow.day)
    return events_tomorrow


if __name__ == "__main__":
    events = get_stories()
    slack = SlackConnection()
    for i in events:
        slack.post(i.title, i.event_time)
