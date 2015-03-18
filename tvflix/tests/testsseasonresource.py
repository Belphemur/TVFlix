import unittest
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound

from ..resources.seasonresource import SeasonResource

# default view test
class TestMySeasonResource(unittest.TestCase):    
    def tearDown(self):
        testing.tearDown()

    def test_passing_seasonResource(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons'
        request.matchdict = {'label': 'game-of-thrones'}
        info = SeasonResource.get(SeasonResource(request))
        
        self.assertEqual(info['size'], 2)
        links = info['_links']
        self.assertEqual(links['self'], {'href': '/tvflix/shows/game-of-thrones/seasons'})
        
    def test_noEpisodesInSeason(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons'
        request.matchdict = {'label': 'simpsons'}
        info = SeasonResource.get(SeasonResource(request))
        
        self.assertEqual(info['size'], 0)
        self.assertEqual(info['_embedded'], {'season': []})
        
    def test_NotFound_seasonResource(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons'  
        request.matchdict = {'label': 'dont-exists'}
        season  = SeasonResource(request)
        self.assertRaises(HTTPNotFound, season.get)