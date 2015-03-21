from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

from ..models.show import Show
from ..models.episode import Episode

from cornice import Service
from cornice.resource import resource, view
from webob import Response
import json

def showParser(shows, show):
    if shows:
        for i in shows:
            if i.showlabel == show.showlabel:
                return False
            
    return True
    
def episodeParser(episodes, ep):
    if episodes:
        for i in episodes:
            if i.ep_id == ep.ep_id:
                return False
            
    return True

#?query=key&query=key searching works
@resource(path='/tvflix/search/shows')
class SearchShowResource(object):
    def __init__(self, request):
        self.request = request
        #set content type to hal+json
        request.response.content_type = 'application/hal+json'

    @view(renderer='json')
    def get(self):
        #get query string, it's a tuple
        req = self.request.GET.items()

        keywords = []
        for i in req:
            if i[0] == u'query' and not i[1] == '':
                keywords.append(i[1])
        
        shows = []
        for i in keywords:
            #search shows
            show = Show.SearchShowsByKeywords(i)
            
            #check if show exist in a shows list
            if show:
                for j in show:
                    if showParser(shows, j):
                        #if all good, add show to shows list
                        shows.append(j)
   
        if shows:
            query = ''
            for i in keywords:
                query = query + 'query=' +i +'&'
                
            links = {"self": { "href": "/tvflix/search/shows?" +query }}
            
            listOfShows = []
            for show in shows:
                _links = {"self": {"href": "/tvflix/shows/" +show.showlabel},
                          "comments": {"href": "/tvflix/shows/"+ show.showlabel +"/comments"},
                          "seasons": {"href": "/tvflix/shows/"+ show.showlabel +"/seasons"}
                          }
                          
                tags = []          
                if show.tags:
                    for i in show.tags:
                        tags.append(i.name)
                          
                embedContent = {"label": show.showlabel,
                                "title": show.title,
                                "start_year": show.start_year,
                                "end_year": show.end_year,
                                "summary": show.summary,
                                "channel": show.channel,
                                "tags": str(tags)}
                        
                embedContent['_links'] = _links        
                listOfShows.append(embedContent)
                
            content = {'_links': links, 'size': len(shows), '_embedded': listOfShows}
            
            return content    
         
        raise HTTPNotFound
        
        
@resource(path='/tvflix/search/episodes')
class SearchEpisodeResource(object):
    def __init__(self, request):
        self.request = request
        #set content type to hal+json
        request.response.content_type = 'application/hal+json'

    @view(renderer='json')
    def get(self):
        #get query string, it's a tuple
        req = self.request.GET.items()

        keywords = []
        for i in req:
            if i[0] == u'query' and not i[1] == '':
                keywords.append(i[1])
                
        episodes = []        
        if keywords:
            for i in keywords:
                epi = Episode.SearchEpisodeByKeywords(i)
                
                if epi:
                    for j in epi:
                        if episodeParser(episodes, j):
                            episodes.append(j)
                            
        if episodes:
            query = ''
            for i in keywords:
                query = query + 'query=' +i +'&'
                
            links = {"self": {"href": "/tvflix/search/episodes?" +query}}
            
            episode = []
            for ep in episodes:
                _links = {"self": {"href": "/tvflix/shows/"+ ep.show.showlabel +"/seasons/"+ str(ep.season) +"/episodes/" + str(ep.number) },
                          "season": {"href": "/tvflix/shows/"+ ep.show.showlabel +"/seasons/"+ str(ep.season)}
                          }
                          
                embedContent = {"number": ep.number,
                                "title": ep.title,
                                "bcast_date": str(ep.bcast_date),
                                "summary": ep.summary,
                                "season": ep.season
                                }
                                
                embedContent['_links'] = _links
                episode.append(embedContent)
                
            content = {'_links': links, 'size': len(episodes), '_embedded': episode}
            
            return content
                                           
        raise HTTPNotFound