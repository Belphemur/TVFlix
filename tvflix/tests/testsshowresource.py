import unittest
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound, HTTPNotImplemented

from ..models import Session, Base

from ..resources.showresource import ShowResource

# default view test
class TestMyShowView(unittest.TestCase):    
    def tearDown(self):
        Session.remove()
        testing.tearDown()

    def test_passing_showResource(self):
        request = testing.DummyRequest()
        #url is /tvflix/shows/{label}, so this is how i define the label 
        request.matchdict = {'label': 'game-of-thrones'}
        show  = ShowResource(request)
        info = show.get()
        self.assertEqual(info['channel'], 'HBO')
        self.assertEqual(info['title'], 'Game of Thrones')
        
    def test_passing_showWithEmptyVariables(self):
        request = testing.DummyRequest()
        #url is /tvflix/shows/{label}
        request.matchdict = {'label': 'simpsons'}
        info = ShowResource.get(ShowResource(request))
        self.assertEqual(info['channel'], 'MTV')
        self.assertEqual(info['title'], 'The simpsons')
        self.assertEqual(info['end_year'], None)
        self.assertEqual(info['tags'], None)
        
    def test_failure_showResource(self):
        request = testing.DummyRequest()
        #url is /tvflix/shows/{label}
        request.matchdict = {'label': 'dont-exists'}
        show  = ShowResource(request)
        self.assertRaises(HTTPNotFound, show.get)
        
    def test_failure_showResourcePutNotImplemented(self):
        request = testing.DummyRequest()
        #url is /tvflix/shows/{label}
        request.matchdict = {'label': 'game-of-thrones'}
        show  = ShowResource(request)
        self.assertRaises(HTTPNotImplemented, show.put)