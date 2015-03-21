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
                    embedComment = {"username": com.user.username,
                                    "comment": com.comment,
                                    "posted": str(com.posted),
                                    "updated": str(com.updated)
                                    }
                                    
                    embedComment['_links'] = _links
                    comment.append(embedComment)
                    
                size = len(comments)
                content = {'_links': _links, 'size': size, '_embedded': comment}
                
                return content                   
        
        raise HTTPNotFound
        
    def post(self):
        label = self.request.matchdict['label']
        
        show = Show.GetShowByLabel(label)
        
        if show:
            if not 'apikey' in self.request.headers.keys():
                raise HTTPUnauthorized
                
            apikey = self.request.headers['apikey']   
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
                
            #checks if user has already commented the show
            comments = show.GetComments()
            
            if comments:
                for com in comments:
                    if com.user.user_id == user.user_id:
                        raise HTTPInternalServerError
                
            with transaction.manager:
                com = Comment(user_id=user.user_id, show_id=show.show_id, comment=comment,
                              posted=datetime.now(), updated=None)
                Session.add(com)
                
            #refresh user object    
            user = Session.query(User).filter(User.user_id == user.user_id).first()  
            #get new comment from user
            newComment = user.GetCommentForShow(show)
            
            #not designed /comment/{username} !!
            _links = {"self": {"href": "/tvflix/shows/"+ label +"/comments/" +user.username},
                    "show": {"href": "/tvflix/shows/"+ label}
                    }
                    
            content = {"username": newComment.user.username,
                      "comment": newComment.comment,
                      "posted": str(newComment.posted),
                      "updated": str(newComment.updated)
                      }
                     
            content['_links']  = _links
            
            return content
               
        raise HTTPNotFound
        
@resource(path='/tvflix/shows/{label}/comments/{username}')
class SingleCommentsResource(object):
    def __init__(self, request):
        self.request = request
        #set content type to hal+json
        request.response.content_type = 'application/hal+json'

    @view(renderer='json')
    def put(self):
        label = self.request.matchdict['label']  
        username = self.request.matchdict['username'] 
        
        show = Show.GetShowByLabel(label)
        
        if show:
            if not 'apikey' in self.request.headers.keys():
                raise HTTPUnauthorized
                
            apikey = self.request.headers['apikey']   
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
                #update comment
                with transaction.manager:
                    time = datetime.now()
                    Session.query(Comment).filter(Comment.comment_id == com.comment_id)\
                        .update({'comment': comment, 'updated': time})
                    
                newCom = Comment.GetUserCommentForShow(user, show)
                
                _links = {"self": {"href": "/tvflix/shows/"+ label +"/comments/" +user.username},
                        "show": {"href": "/tvflix/shows/"+ label}
                        }
                        
                content = {"username": user.username,
                          "comment": newCom.comment,
                          "posted": str(newCom.posted),
                          "updated": str(newCom.updated)
                          }
                          
                content['_links'] = _links
                
                return content
                
        raise HTTPNotFound
                

    @view(renderer='json')
    def delete(self):
        label = self.request.matchdict['label']  
        username = self.request.matchdict['username'] 
        
        show = Show.GetShowByLabel(label)
        
        if show:
            if not 'apikey' in self.request.headers.keys():
                raise HTTPUnauthorized
                
            apikey = self.request.headers['apikey']   
            user = User.GetUserByApiKey(apikey)
               
            if not user or not str(username) == str(user.username):
                raise HTTPUnauthorized
                
            com = Comment.GetUserCommentForShow(user, show)
            if com:
                with transaction.manager:
                    Session.delete(com)
                    
                raise HTTPNoContent
                    
        raise HTTPNotFound

        
        
        
        
        
        
        
        
        
        
        