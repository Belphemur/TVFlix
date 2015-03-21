from pyramid.httpexceptions import HTTPNotFound, HTTPNotImplemented
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from ..models.show import Show

from cornice import Service
from cornice.resource import resource, view
from webob import Response
import json


@resource(path='/tvflix/shows/{label}')
class ShowResource(object):
    def __init__(self, request):
        self.request = request
        #set content type to hal+json
        request.response.content_type = 'application/hal+json'

    @view(renderer='json')
    def get(self):
        label = self.request.matchdict['label']
        show = Show.GetShowByLabel(label)

        if show:
            showTags = show.GetTags()
            tags = None
            
            if showTags:
                tags = []
                for tag in showTags:
                    tags.append(tag.name)

            _links = {"self": {"href": "/tvflix/shows/" + str(label)},
                      "comments": {"href": "/tvflix/shows/"+ str(label) +"/comments"},
                      "seasons": {"href": "/tvflix/shows/"+ str(label) +"/seasons"}
                      }

            content = {"label": show.showlabel,
                      "title": show.title,
                      "start_year": show.start_year,
                      "end_year": show.end_year,
                      "summary": show.summary,
                      "channel": show.channel,
                      "tags": tags
                        }

            content["_links"] = _links

            return content
        raise HTTPNotFound
        
    def put(self):
        raise HTTPNotImplemented

