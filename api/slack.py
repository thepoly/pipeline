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
    
    
    def slack_connect(url, data):
        pass
        
    def post(self, title, time, channel):
        url = self.baseurl + "chat.postMessage"
        data = { 'token' : self.slack_settings.slack_api_key, 'text' : "{} taking place at {} tomorrow".format(title, time), 'channel' : channel, 'username' : "Pipeline Bot"}
        r = requests.post(url, data=data)
        print(r.content)



    def get_slackID(self, person_id, handle):
        
        if models.Person.get(id = person_id).slack_id != None:
            return models.Person.get(id = person_id).slack_id

        else:
            url = self.baseurl + "/users.list"
            data = {'token' : self.slack_settings.slack_api_key}
            r = requests.post(url, data=data)
            rjson = r.json()
            for i in rjson['members']:
                if i['name'] == handle:
                    person = models.Person.get(id = person_id)
                    person.slack_id = i['id']
                    person.save()
                    return models.Person.get(id = person_id).slack_id
            

    def message(self, title, time, id, handle):
        url = self.baseurl + "im.open"
        slack_id = self.get_slackID(id, handle)
        data = { 'token' : self.slack_settings.slack_api_key, 'user' : slack_id}
        
        r = requests.post(url, data=data)
        rjson = r.json()
        print(rjson)
        
        self.post(title,time, rjson['channel']['id'])
        
        url = self.baseurl + "im.close"
        data = { 'token' : self.slack_settings.slack_api_key, 'user' : handle}
        r = requests.post(url, data=data)




def get_stories():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    events_tomorrow = models.Story.select().where(models.Story.event_time.day == tomorrow.day)
    return events_tomorrow


if __name__ == "__main__":
    events = get_stories()
    slack = SlackConnection()
    for i in events:
        for j in i.story_people:
            handle = j.person.slack_handle
            slack.message(i.title, i.event_time, j.person.id, handle)
