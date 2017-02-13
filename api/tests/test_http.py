import pytest
import requests

class TestStoriesResource:

    def test_create_story(self):
        j = requests.post('http://api:8000/stories', json={'title': 'Hey there'}).json()
        assert j['story']['title'] == 'Hey there'
        story_id = j['story']['id']

        j = requests.get(f'http://api:8000/stories/{story_id}').json()
        assert j['story']['title'] == 'Hey there'

        assert j['story'] in requests.get(f'http://api:8000/stories').json()['stories']

    def test_modify_story(self):
        j = requests.post('http://api:8000/stories', json={'title': 'Hey there'}).json()
        assert j['story']['title'] == 'Hey there'
        story_id = j['story']['id']

        j = requests.put(f'http://api:8000/stories/{story_id}', json={'section': 'News'}).json()

        j = requests.get(f'http://api:8000/stories/{story_id}').json()
        assert j['story']['section'] == 'News'

    def test_story_event_time(self):
        # Create story without event time
        j = requests.post('http://api:8000/stories', json={'title': 'Hey this has an event time'}).json()
        story_id = j['story']['id']
        assert j['story']['event_time'] == None

        # Ensure it has no event time
        j = requests.get(f'http://api:8000/stories/{story_id}').json()
        assert j['story']['event_time'] == None

        # Add event time
        requests.put(f'http://api:8000/stories/{story_id}', json={'event_time': '2017-02-07T15:27:28+00:00'})

        # Ensure it has event time
        j = requests.get(f'http://api:8000/stories/{story_id}').json()
        assert j['story']['event_time'] == '2017-02-07T15:27:28+00:00'

        # Remove event time
        requests.put(f'http://api:8000/stories/{story_id}', json={'event_time': None})

        # Ensure it has no event time
        j = requests.get(f'http://api:8000/stories/{story_id}').json()
        assert j['story']['event_time'] == None


class TestSettingsResource:

    def test_get_settings(self):
        j = requests.get('http://api:8000/settings').json()
        assert isinstance(j['settings'], dict)
