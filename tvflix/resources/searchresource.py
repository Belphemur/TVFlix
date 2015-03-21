from pyramid.httpexceptions import HTTPNotFound
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import Session
from ..models.show import Show
from ..models.user import User
from ..models.comment import Comment
import transaction

from cornice import Service
from cornice.resource import resource, view
from webob import Response, exc
import json

def showParser(shows, show):
    if shows:
        for i in shows:
            if i.showlabel == show.showlabel:
                return False
            
    return True
    

@resource(path='/tvflix/search/shows')
class searchShowResource(object):
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
            if i[0] == u'query':
                keywords.append(i[1])
        print keywords
        
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