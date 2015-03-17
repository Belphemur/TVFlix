import unittest
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound

from ..models import Session, Base


# default view test
class TestMyShowView(unittest.TestCase):    
    def tearDown(self):
        Session.remove()
        testing.tearDown()

    def test_passing_showView(self):
        from ..resources.showresource import ShowResource

        request = testing.DummyRequest()
        #url is /tvflix/shows/{label}, so this is how i define the label 
        request.matchdict = {'label': 'game-of-thrones'}
        show  = ShowResource(request)
        info = show.get()
        self.assertEqual(info['channel'], 'HBO')
        
    def test_failure_showView(self):
        pass
        #not yet working
        from ..resources.showresource import ShowResource

        request = testing.DummyRequest()
        #url is /tvflix/shows/{label}, so this is how i define the label
        request.matchdict = {'label': 'dont-exists'}
        show  = ShowResource(request)
        self.assertRaises(HTTPNotFound, show.get)