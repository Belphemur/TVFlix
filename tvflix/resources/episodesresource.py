from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPInternalServerError, HTTPUnauthorized
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import Session
from ..models.show import Show
from ..models.user import User
from ..models.episode import Episode
import transaction

from cornice import Service
from cornice.resource import resource, view
from webob import Response, exc
import json

from datetime import datetime, date, time

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
        
        if not str(number).isdigit():
            raise HTTPNotFound
        
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
        
        
    @view(renderer='json')    
    def post(self):       
        label = self.request.matchdict['label']
        number = self.request.matchdict['number']
        
        if not str(number).isdigit():
            raise HTTPNotFound
            
        show = Show.GetShowByLabel(label)

        if show:
            try:
                apikey = self.request.headers['apikey']
            except:
                raise HTTPUnauthorized
                
            user = User.GetUserByApiKey(apikey)
               
            if not user or user.admin == False:
                raise HTTPUnauthorized
            
            try:
                epinumber = self.request.json_body['number']
                season = self.request.json_body['season']
                bcast_date = self.request.json_body['bcast_date']
            except:
                raise HTTPBadRequest
            
            try:
                title = self.request.json_body['title'] #can be empty
            except:
                title = None
                
            try:
                summary = self.request.json_body['summary'] #can be empty
            except:
                summary = None
            
            if not str(epinumber).isdigit():
                raise HTTPBadRequest 
            
            #url episode number and given episode number must match
            if not str(season) == str(number):
                raise HTTPBadRequest
                
            #trying to transfer the date to parsable format 
            try:
                bcast_date = bcast_date.replace("-","")
                bcast_date = datetime.strptime(bcast_date, "%Y%m%d").date() #make it a date object
            except:
                raise HTTPBadRequest
                
            #add more text later    
            if show.GetEpisodeBySeasonByNumber(int(season), int(epinumber)):
                raise HTTPInternalServerError 
            
            #adding episode to db
            with transaction.manager:
                epi = Episode.AddEpisode(show=show, title=title, season=int(season),
                                     number=int(epinumber), bcast_date=bcast_date, summary=summary)
                
            if epi:
                _links = {"self": { "href": "/tvflix/shows/"+ label +"/seasons/"+ str(season) +"/episodes/" +str(epinumber) },
                        "season": { "href": "/tvflix/shows/"+ label +"/seasons/"+ str(season)}
                          }
                          
                content = {"number": int(epinumber),
                          "title": title,
                          "bcast_date": str(bcast_date),
                          "summary": summary,
                          "season": int(season)
                          }
                          
                content['_links'] = _links
                
                return content
                    
        raise HTTPNotFound
        