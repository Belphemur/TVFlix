from pyramid.httpexceptions import (
    HTTPNotFound, 
    HTTPBadRequest, 
    HTTPInternalServerError, 
    HTTPUnauthorized, 
    HTTPNoContent
    )
    
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from ..models import Session
from ..models.show import Show
from ..models.user import User
from ..models.episode import Episode
import transaction

from cornice import Service
from cornice.resource import resource, view
from webob import Response
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
                                "bcast_date": epi.bcast_date.isoformat(),
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
            if not 'apikey' in self.request.headers.keys():
                raise HTTPUnauthorized
                
            apikey = self.request.headers['apikey']   
            user = User.GetUserByApiKey(apikey)
               
            if not user or user.admin == False:
                raise HTTPUnauthorized
                
            try: #checks if json_body in request
                self.request.json_body
            except:
                raise HTTPBadRequest
            
            if not 'bcast_date' in self.request.json_body.keys():
                raise HTTPBadRequest
            if not 'number' in self.request.json_body.keys():
                raise HTTPBadRequest
            if not 'season' in self.request.json_body.keys():
                raise HTTPBadRequest

            epinumber = self.request.json_body['number']
            season = self.request.json_body['season']
            bcast_date = self.request.json_body['bcast_date']
   
            if 'title' in self.request.json_body.keys():
                title = self.request.json_body['title'] #can be empty
            else:
                title = None
                
            if 'summary' in self.request.json_body.keys():
                summary = self.request.json_body['summary'] #can be empty
            else:
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
        
      
#single episode resource
@resource(path='/tvflix/shows/{label}/seasons/{number}/episodes/{ep}')
class SingleEpisodesResource(object):
    def __init__(self, request):
        self.request = request
        #set content type to hal+json
        request.response.content_type = 'application/hal+json'
    
    @view(renderer='json')
    def get(self):
        label = self.request.matchdict['label']
        number = self.request.matchdict['number']
        ep = self.request.matchdict['ep']
        
        if not str(number).isdigit():
            raise HTTPNotFound
            
        if not str(ep).isdigit():
            raise HTTPNotFound
            
        show = Show.GetShowByLabel(label)

        if show:    
            episode = show.GetEpisodeBySeasonByNumber(int(number), int(ep))
            
            if episode:
                _links = {"self": {"href": "/tvflix/shows/"+ label +"/seasons/"+ str(number) +"/episodes/" +str(ep)},
                        "season": {"href": "/tvflix/shows/"+ label +"/seasons/"+ str(number)}
                        }
                        
                content = {"number": episode.number,
                          "title": episode.title,
                          "bcast_date": str(episode.bcast_date),
                          "summary": episode.summary,
                          "season": episode.season
                          }
                          
                content['_links'] = _links
                
                return content
         
        raise HTTPNotFound
    
    @view(renderer='json')
    def put(self):
        label = self.request.matchdict['label']
        number = self.request.matchdict['number']
        ep = self.request.matchdict['ep']
        
        if not str(number).isdigit():
            raise HTTPNotFound
            
        if not str(ep).isdigit():
            raise HTTPNotFound
            
        show = Show.GetShowByLabel(label)

        if show:  
            #check if user exists and it has admin rights
            if not 'apikey' in self.request.headers.keys():
                raise HTTPUnauthorized
                    
            apikey = self.request.headers['apikey']   
            user = User.GetUserByApiKey(apikey)
               
            if not user or user.admin == False:
                raise HTTPUnauthorized
                
            #check json_body and content 
            try:
                self.request.json_body
            except:
                raise HTTPBadRequest
            
            if not 'bcast_date' in self.request.json_body.keys():
                raise HTTPBadRequest
            if not 'number' in self.request.json_body.keys():
                raise HTTPBadRequest
            if not 'season' in self.request.json_body.keys():
                raise HTTPBadRequest
            if not 'title' in self.request.json_body.keys():
                raise HTTPBadRequest
            if not  'summary' in self.request.json_body.keys():
                raise HTTPBadRequest
            
            try:
                bcast_date = self.request.json_body['bcast_date']  
                bcast_date = bcast_date.replace("-","")
                bcast_date = datetime.strptime(bcast_date, "%Y%m%d").date() #make it a date object
            except:
                raise HTTPBadRequest
                    
            epinumber = self.request.json_body['number']
            season = self.request.json_body['season']
            title = self.request.json_body['title']
            summary = self.request.json_body['summary']
            
            if not str(epinumber) == str(ep):
                raise HTTPBadRequest
                
            if not str(number) == str(season):
                raise HTTPBadRequest
                
            episode = show.GetEpisodeBySeasonByNumber(int(number), int(ep))
            
            if episode:
                with transaction.manager:
                    Session.query(Episode).filter(Episode.ep_id == episode.ep_id).update({"title": title, "season": season, "number": epinumber, "bcast_date": bcast_date, "summary":summary})
                    
                #get newly modified show
                newShow = Show.GetShowByLabel(label)
                episode = newShow.GetEpisodeBySeasonByNumber(int(number), int(ep))
                
                _links = {"self": {
                          "href": "/tvflix/shows/"+ label +"/seasons/"+ str(number) +"/episodes/" + str(ep)},
                        "season": {"href": "/tvflix/shows/"+ label +"/seasons/"+ str(number) }
                        }
                        
                content = {"number": episode.number,
                          "title": episode.title,
                          "bcast_date": str(episode.bcast_date),
                          "summary": episode.summary,
                          "season": episode.season
                          }
                          
                content['_links'] = _links
                
                return content
                    
        raise HTTPNotFound
    
    @view(renderer='json')
    def delete(self):
        label = self.request.matchdict['label']
        number = self.request.matchdict['number']
        ep = self.request.matchdict['ep']
        
        if not str(number).isdigit():
            raise HTTPNotFound
            
        if not str(ep).isdigit():
            raise HTTPNotFound
            
        show = Show.GetShowByLabel(label)

        if show:  
            #check if user exists and it has admin rights
            if not 'apikey' in self.request.headers.keys():
                raise HTTPUnauthorized
                    
            apikey = self.request.headers['apikey']   
            user = User.GetUserByApiKey(apikey)
               
            if not user or user.admin == False:
                raise HTTPUnauthorized
                
            episode = show.GetEpisodeBySeasonByNumber(int(number), int(ep))           
            if episode:
                #delete and commit changes using transaction
                with transaction.manager:
                    episode.DeleteEpisode()

                raise HTTPNoContent
                        
        raise HTTPNotFound
                    