from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import Session
from ..models.user import User
from ..models.show import Show

from cornice import Service
from cornice.resource import resource, view
from webob import Response, exc
import json


@resource(path='/tvflix/shows/{label}/seasons')
class SeasonResource(object):
    def __init__(self, request):
        self.request = request
        #set content type to hal+json
        request.response.content_type = 'application/hal+json'
        
    @view(renderer='json')
    def get(self):
        label = self.request.matchdict['label']
        show = Show.GetShowByLabel(label)
        
        if show:
            seasons = show.GetAllSeasonNumbers()
            
            links = {"self": { "href": "/tvflix/shows/"+ label +"/seasons"}
                     }
            
            season = []
            for num in seasons:
                episodes = show.GetEpisodeBySeason(num)
                
                _links = {"self": {"href": "/tvflix/shows/"+ label +"/seasons/" +str(num)},
                          "show": {"href": "/tvflix/shows/" +label},
                          "episode": {"href": "/tvflix/shows/"+ label +"/seasons/"+ str(num) +"/episodes"}
                        }
                        
                seasonContent = {"number": str(num),
                                "episodes": len(episodes),
                                "last_bcast_episode": episodes[-1].number, #TODO better
                                "start_date": str(episodes[0].bcast_date) #episodes are ordered by a date
                                }
                                
                embedContent = {'_links': _links}
                season.append(embedContent)
                season.append(seasonContent)
                
            _embedded = {'season': season}
            content = {}    
            content['_links'] = links
            content['size'] = len(seasons)
            content['_embedded'] = _embedded
            
            return content
                   
        raise HTTPNotFound
        

@resource(path='/tvflix/shows/{label}/seasons/{number}')
class SingleSeasonResource(object):
    def __init__(self, request):
        self.request = request
        #set content type to hal+json
        request.response.content_type = 'application/hal+json'
       
    @view(renderer='json')
    def get(self):
        label = self.request.matchdict['label']
        number = self.request.matchdict['number']
        
        if not str(number).isdigit():
            raise HTTPBadRequest
        
        show = Show.GetShowByLabel(label)
        
        if show:
            episodes = show.GetEpisodeBySeason(int(number))
                   
            _links = { "self": { "href": "/tvflix/shows/"+ label +"/seasons/" +str(number) },
                    "show": { "href": "/tvflix/shows/" +label },
                    "episode": {"href": "/tvflix/shows/"+ label +"/seasons/"+ str(number) +"/episodes" }
                    }
            if episodes:                
                content = {"number": number,
                          "episodes": len(episodes),
                          "last_bcast_episode": int(episodes[-1].number),
                          "start_date": str(episodes[0].bcast_date)
                          }
                        
                content['_links'] = _links
                
                return content
            
        raise HTTPNotFound
    
        
        