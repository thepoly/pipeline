import falcon

import models
import middleware

import route_stories
import route_people

models.connect()

api = falcon.API(middleware=middleware.components)
api.add_route('/stories', route_stories.StoriesResource())
api.add_route('/stories/{story_id}', route_stories.StoryResource())
api.add_route('/stories/{story_id}/people', route_stories.StoryPeopleResource())
api.add_route('/people', route_people.PeopleResource())
api.add_route('/people/{person_id}', route_people.PersonResource())
