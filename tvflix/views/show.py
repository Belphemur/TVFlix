from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import Session
from ..models.user import User
from ..models.show import Show

from cornice import Service
from webob import Response, exc
import json

    
class _404(exc.HTTPError):
    def __init__(self, msg='Not Found'):
        body = {'status': 404, 'message': msg}
        Response.__init__(self, json.dumps(body))
        self.status = 404
        self.content_type = 'application/json'  
    
    
#route for show views  
show = Service(name='shows', path='/tvflix/shows/{label}')

#view class for shows GET
@show.get()
def get_show(request):
    label = request.matchdict['label']
    show = Show.GetShowByLabel(label)
    
    if show:
        showTags = show.GetTags()
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
    raise _404

