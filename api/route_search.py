import json

import falcon

import models
import schemas
import api_util

stories_schema = schemas.StorySchema(many=True)

## change url to search results based on the author, article name (story)
class SearchResource:

    def on_get(self, req, resp):
        ## print(req.params)
        if ("title" in req.params):
            stories = models.Story.select().where(models.Story.title == req.params["title"])

        if ("created" in req.params):
            stories = models.Story.select().where(models.Story.created == req.params["created"]) 

        if ("event_time") in req.params):
			stories = models.Story.select().where(models.Story.event_time == req.params["event_time"])

		if ("location" in req.params):
			stories = models.Story.select().where(models.Story.location == req.params["location"])

		if ("section" in req.params): 
			stories = models.Story.select().where(models.Story.section == req.params["section"])

        search_results = stories_schema.dump(stories)
        
        resp.body = api_util.json_dump({'search_results': search_results})
