import pytest
import requests

class TestStoriesResource:

    def test_no_stories(self):
        j = requests.get('http://api:8000/stories').json()
        assert j == {'stories': []}

    def test_create_story(self):

        j = requests.post('http://api:8000/stories', json={'title': 'Hey there'}).json()
        assert j['story']['title'] == 'Hey there'

        j = requests.get('http://api:8000/stories').json()
        assert j['stories'][0]['title'] == 'Hey there'
