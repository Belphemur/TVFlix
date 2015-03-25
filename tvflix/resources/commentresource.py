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
from ..models.comment import Comment
import transaction

from cornice import Service
from cornice.resource import resource, view
from webob import Response
import json

from datetime import datetime, date, time

def generateCommentEnvelop(label, newComment, user):
    # not designed /comment/{username} !!
    _links = {"self": {"href": "/tvflix/shows/" + label + "/comments/" + user.username},
              "show": {"href": "/tvflix/shows/" + label}
              }
    content = {"username": newComment.user.username,
               "comment": newComment.comment,
               "posted": str(newComment.posted),
               "updated": str(newComment.updated)
               }
    content['_links'] = _links
    return content

@resource(path='/tvflix/shows/{label}/comments')
class CommentsResource(object):
    def __init__(self, request):
        self.request = request
        #set content type to hal+json
        request.response.content_type = 'application/hal+json'

    @view(renderer='json')
    def get(self):
        label = self.request.matchdict['label']
        
        show = Show.GetShowByLabel(label)
        
        if show:
            comments = show.GetComments()
            
            if comments:
                _links = {"self":{  "href":"/tvflix/shows/"+ label +"/comments"},
                          "show":{  "href":"/tvflix/shows/"+ label}
                          }
                
                comment = []
                for com in comments:
                    updated = 'None' if com.updated is None else com.updated.isoformat()
                    embedComment = {"username": com.user.username,
                                    "comment": com.comment,
                                    "posted": com.posted.isoformat(),
                                    "updated": updated
                                    }
                                    
                    embedComment['_links'] = _links
                    comment.append(embedComment)
                    
                size = len(comments)
                content = {'_links': _links, 'size': size, '_embedded': comment}
                
                return content                   
        
        raise HTTPNotFound

    def post(self):
        with transaction.manager:
            label = self.request.matchdict['label']

            show = Show.GetShowByLabel(label)

            if show:
                apikey = self.request.headers.get("apikey")
                if not apikey:
                    raise HTTPUnauthorized

                user = User.GetUserByApiKey(apikey)

                if not user:
                    raise HTTPUnauthorized

                try: #checks if json_body in request
                    self.request.json_body
                except:
                    raise HTTPBadRequest

                if not 'comment' in self.request.json_body.keys():
                    raise HTTPBadRequest
                else:
                    comment = self.request.json_body['comment']

                if not Comment.AddComment(message=comment,User=user,Show=show):
                     raise HTTPInternalServerError

                #refresh user object
                #get new comment from user
                newComment = user.GetCommentForShow(show)

                return generateCommentEnvelop(label, newComment, user)

            raise HTTPNotFound
        
@resource(path='/tvflix/shows/{label}/comments/{username}')
class SingleCommentsResource(object):
    def __init__(self, request):
        self.request = request
        #set content type to hal+json
        request.response.content_type = 'application/hal+json'

    @view(renderer='json')
    def put(self):
        with transaction.manager:
            label = self.request.matchdict['label']
            username = self.request.matchdict['username']

            show = Show.GetShowByLabel(label)

            if show:
                apikey = self.request.headers.get("apikey")
                if not apikey:
                    raise HTTPUnauthorized

                user = User.GetUserByApiKey(apikey)

                if not user or not str(username) == str(user.username):
                    raise HTTPUnauthorized

                try: #checks if json_body in request
                    self.request.json_body
                except:
                    raise HTTPBadRequest

                if not 'comment' in self.request.json_body.keys():
                    raise HTTPBadRequest
                else:
                    comment = self.request.json_body['comment']
                    if comment == '' or comment is None:
                        raise HTTPBadRequest

                com = Comment.GetUserCommentForShow(user, show)
                if com:
                    if com.ModifyComment(comment):
                        return generateCommentEnvelop(label, com, user)
                    else:
                        raise HTTPInternalServerError

            raise HTTPNotFound
                

    @view(renderer='json')
    def delete(self):
        with transaction.manager:
            label = self.request.matchdict['label']
            username = self.request.matchdict['username']

            show = Show.GetShowByLabel(label)

            if show:
                apikey = self.request.headers.get("apikey")
                if not apikey:
                    raise HTTPUnauthorized

                user = User.GetUserByApiKey(apikey)

                if not user or not str(username) == str(user.username):
                    raise HTTPUnauthorized

                com = Comment.GetUserCommentForShow(user, show)
                if com:
                    if com.DeleteComment():
                        raise HTTPNoContent
                    else:
                        raise HTTPInternalServerError

            raise HTTPNotFound

        
        
        
        
        
        
        
        
        
        
        