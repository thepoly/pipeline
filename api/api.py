import falcon

import settings
import models
import middleware

import route_stories
import route_people
import route_photos
import route_settings




models.connect()

#Initialize settings
settings.AppSettings()

api = falcon.API(middleware=middleware.components)
api.add_route('/stories', route_stories.StoriesResource())
api.add_route('/stories/{story_id}', route_stories.StoryResource())
api.add_route('/stories/{story_id}/people', route_stories.StoryPeopleResource())
api.add_route('/people', route_people.PeopleResource())
api.add_route('/people/{person_id}', route_people.PersonResource())
api.add_route('/photos', route_photos.PhotosResource())
api.add_route('/photos/{photo_id}', route_photos.PhotoResource())
api.add_route('/settings', route_settings.SettingsResource())
