from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import Session
from ..models.show import Show

from cornice import Service
from cornice.resource import resource, view
from webob import Response, exc
import json

@resource(path='/tvflix/shows/{label}/seasons/{number}/episodes')
class EpisodesResource(object):
    def __init__(self, request):
        self.request = request
        #set content type to hal+json
        request.response.content_type = 'application/hal+json'

    @view(renderer='json')
    def get(self):
        label = self.request.matchdict['label']
        number = self.request.matchdict['number']
        
        if not isinstance(number, int):
            raise HTTPBadRequest
        
        show = Show.GetShowByLabel(label)
        
        if show:
            episodes = show.GetEpisodeBySeason(int(number))
            
            if episodes:
                links = {"season": { "href": "/tvflix/shows/"+ label +"/seasons/" +str(number) },
                        "self": { "href": "/tvflix/shows/"+ label +"/seasons/"+ str(number) +"/episodes" }
                        }
                
                episode = []
                for epi in episodes:
                    _links = {"season": { "href": "/tvflix/shows/"+ label +"/seasons/" +str(number) },
                            "self": { "href": "/tvflix/shows/"+ label +"/seasons/"+ str(number) +"/episodes/" +str(epi.number) }
                            }
                            
                    epiContent = {"number": int(epi.number),
                                "title": epi.title,
                                "bcast_date": str(epi.bcast_date),
                                "summary": epi.summary,
                                "season": int(epi.season)
                                }
                                
                    embedContent = {'_links': _links}
                    episode.append(embedContent)
                    episode.append(epiContent)
                    
                _embedded = {'episode': episode}
                content = {}    
                content['_links'] = links
                content['size'] = len(episodes)
                content['_embedded'] = _embedded
                
                return content
                
        raise HTTPNotFound