import settings
import requests


class SlackConnection:
    
    def __init__(self):
        self.baseurl = "https://slack.com/api/"
        self.slack_settings = settings.AppSettings()

    
    def check_connection(self):
        url = self.baseurl + "auth.test"
        data = {'token' : self.slack_settings.slack_api_key}
        r = requests.post(url, data=data)
        
    def post(self, message):
        url = self.baseurl + "chat.postMessage"
        data = { 'token' : self.slack_settings.slack_api_key, 'text' : message, 'channel' : self.slack_settings.slack_notification_channel, 'username' : "Pipeline Bot"}
        r = requests.post(url, data=data)

