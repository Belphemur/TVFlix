import unittest
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPUnauthorized, HTTPInternalServerError

from ..resources.commentresource import CommentsResource, SingleCommentsResource

from datetime import date

# default view test
class TestMySeasonResource(unittest.TestCase):    
    def tearDown(self):
        testing.tearDown()
        
    #GET:   
    def test_passing_GetCommentResource(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments'
        request.matchdict = {'label': 'game-of-thrones'}
        info = CommentsResource.get(CommentsResource(request))
        
        self.assertEqual(info['size'], 2)
        links = info['_links']
        self.assertEqual(links['self'], {'href': '/tvflix/shows/game-of-thrones/comments'})
        
    def test_failure_GetCommentResourceInvalidLabel(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments'
        request.matchdict = {'label': 'no-show'}
        comment  = CommentsResource(request)
        self.assertRaises(HTTPNotFound, comment.get)
        
    def test_failure_GetCommentResourceNoComments(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments'
        request.matchdict = {'label': 'simpsons'}
        comment  = CommentsResource(request)
        self.assertRaises(HTTPNotFound, comment.get)
        
    #POST
    def test_passing_PostCommentResource(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments'
        request.matchdict = {'label': 'simpsons'}
        request.headers = {'apikey': 'asd'}
        request.json_body = {'comment': "my comment"}
        info = CommentsResource.post(CommentsResource(request))
        
        self.assertEqual(info['username'], 'test user 2')
        self.assertEqual(info['comment'], 'my comment')
        
    def test_failure_PostCommentResourceNoSuchShow(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments'
        request.matchdict = {'label': 'no-show'}
        request.headers = {'apikey': 'asd'}
        request.json_body = {'comment': "my comment"}
        comment  = CommentsResource(request)
        
        self.assertRaises(HTTPNotFound, comment.post)
        
    def test_failure_PostCommentResourceNoApikey(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments'
        request.matchdict = {'label': 'simpsons'}
        request.headers = {'something': 'asd'}
        request.json_body = {'comment': "my comment"}
        comment  = CommentsResource(request)
        
        self.assertRaises(HTTPUnauthorized, comment.post)
        
    def test_failure_PostCommentResourceNoHeader(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments'
        request.matchdict = {'label': 'simpsons'}
        request.json_body = {'comment': "my comment"}
        comment  = CommentsResource(request)
        
        self.assertRaises(HTTPUnauthorized, comment.post)
        
    def test_failure_PostCommentResourceNoJsonBody(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments'
        request.matchdict = {'label': 'simpsons'}
        request.headers = {'apikey': 'asd'}
        comment  = CommentsResource(request)
        
        self.assertRaises(HTTPBadRequest, comment.post)
        
    def test_failure_PostCommentResourceNoCommentInJsonBody(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments'
        request.matchdict = {'label': 'simpsons'}
        request.headers = {'apikey': 'asd'}
        request.json_body = {'somethingelse': "my comment"}
        comment  = CommentsResource(request)
        
        self.assertRaises(HTTPBadRequest, comment.post)
        
    def test_failure_PostCommentResourceSecondComment(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments'
        request.matchdict = {'label': 'game-of-thrones'}
        request.headers = {'apikey': 'asd'}
        request.json_body = {'comment': "my comment"}
        comment  = CommentsResource(request)
        
        self.assertRaises(HTTPInternalServerError, comment.post)
        
    #PUT
    def test_passing_PutSingleCommentResource(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments/{username}'
        #username like this can't exists in reality
        request.matchdict = {'label': 'game-of-thrones', 'username': 'test user 1'}
        request.headers = {'apikey': 'asdasd'}
        request.json_body = {'comment': "my comment"}
        info = SingleCommentsResource.put(SingleCommentsResource(request))
        
        self.assertEqual(info['username'], 'test user 1')
        self.assertEqual(info['comment'], 'my comment') 
        #checks if updated time has been set today, seconds we can't guess 
        self.assertTrue(str(date.today()) in info['updated'])

    def test_failure_PutSingleCommentResourceNoSuchShow(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments/{username}'
        #username like this can't exists in reality
        request.matchdict = {'label': 'no-show', 'username': 'test user 1'}
        request.headers = {'apikey': 'asdasd'}
        request.json_body = {'comment': "my comment"}
        
        info  = SingleCommentsResource(request)
        
        self.assertRaises(HTTPNotFound, info.put)
        
    def test_failure_PutSingleCommentResourceNoUser(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments/{username}'
        #username like this can't exists in reality
        request.matchdict = {'label': 'game-of-thrones', 'username': 'Nope'}
        request.headers = {'apikey': 'asdasd'}
        request.json_body = {'comment': "my comment"}
        
        info  = SingleCommentsResource(request)
        
        self.assertRaises(HTTPUnauthorized, info.put)
        
    def test_failure_PutSingleCommentResourceWrongApikey(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments/{username}'
        #username like this can't exists in reality
        request.matchdict = {'label': 'game-of-thrones', 'username': 'test user 1'}
        request.headers = {'apikey': 'nope'}
        request.json_body = {'comment': "my comment"}
        
        info  = SingleCommentsResource(request)
        
        self.assertRaises(HTTPUnauthorized, info.put)
        
    def test_failure_PutSingleCommentResourceNoHeader(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments/{username}'
        #username like this can't exists in reality
        request.matchdict = {'label': 'game-of-thrones', 'username': 'test user 1'}
        request.json_body = {'comment': "my comment"}
        
        info  = SingleCommentsResource(request)
        
        self.assertRaises(HTTPUnauthorized, info.put)
        
    def test_failure_PutSingleCommentResourceNoJson(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments/{username}'
        #username like this can't exists in reality
        request.matchdict = {'label': 'game-of-thrones', 'username': 'test user 1'}
        request.headers = {'apikey': 'asdasd'}
        
        info  = SingleCommentsResource(request)
        
        self.assertRaises(HTTPBadRequest, info.put)
        
    def test_failure_PutSingleCommentResourceWrongVariableInJson(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments/{username}'
        #username like this can't exists in reality
        request.matchdict = {'label': 'game-of-thrones', 'username': 'test user 1'}
        request.headers = {'apikey': 'asdasd'}
        request.json_body = {'asd': "my comment"}
        
        info  = SingleCommentsResource(request)
        
        self.assertRaises(HTTPBadRequest, info.put)
        
    def test_failure_PutSingleCommentResourceEmptyComment(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/comments/{username}'
        #username like this can't exists in reality
        request.matchdict = {'label': 'game-of-thrones', 'username': 'test user 1'}
        request.headers = {'apikey': 'asdasd'}
        request.json_body = {'comment': ""}
        
        info  = SingleCommentsResource(request)
        
        self.assertRaises(HTTPBadRequest, info.put)
        