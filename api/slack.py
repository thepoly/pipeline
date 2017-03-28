import requests
import time
import datetime

import models
import settings



class SlackConnection:
    
    def __init__(self):
        self.baseurl = "https://slack.com/api/"
        self.slack_settings = settings.AppSettings()
    
    #Handles all connections to slack
    def slack_connect(self, url_extension, data):
        url = self.baseurl + url_extension
        try:
            response = requests.post(url, data=data)
        except requests.exceptions.ConnectionError:
            print("Unable to connect to slack API")

        responsejson = response.json()
        
        if responsejson['ok'] == "false":
            print("Error with slack API:\n", responsejson["error"])
        
        else:
            return responsejson


    #Get the slack ID from the user's handle
    def get_slackID(self, person_id, handle):
        
        if models.Person.get(id = person_id).slack_id != None:
            return models.Person.get(id = person_id).slack_id

        else:
            url = "users.list"
            data = {'token' : self.slack_settings.slack_api_key}
            response = self.slack_connect(url, data)
            
            #Due to limitations of the API, all users must be returned, then the correct one searched for
            for i in rjson['members']:
                if i['name'] == handle:
                    person = models.Person.get(id = person_id)
                    person.slack_id = i['id']
                    person.save()
                    return models.Person.get(id = person_id).slack_id
            

    def message(self, title, time, location, id, handle):
        url = "im.open"
        slack_id = self.get_slackID(id, handle)
        data = { 'token' : self.slack_settings.slack_api_key, 'user' : slack_id}
        response = self.slack_connect(url, data)
        
        if location == None:
            location = "a yet to be determined location!"
        
        url = "chat.postMessage"
        data = { 'token' : self.slack_settings.slack_api_key, 'text' : "{} taking place at {} tomorrow at {}".format(title, time, location), 'channel' : response['channel']['id'], 'username' : "Pipeline Bot"}
        
        self.slack_connect(url, data)
        
        url = "im.close"
        data = { 'token' : self.slack_settings.slack_api_key, 'user' : handle}

        self.slack_connect(url, data)



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
            slack.message(i.title, i.event_time, i.location, j.person.id, handle)
