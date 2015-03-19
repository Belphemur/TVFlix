import unittest
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest

from ..resources.seasonresource import SeasonResource, SingleSeasonResource

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
        
    def test_passNormalSingleSeasonResource(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}'
        request.matchdict = {'label': 'game-of-thrones', 'number': 1}
        info = SingleSeasonResource.get(SingleSeasonResource(request))
        
        self.assertEqual(info['episodes'], 2)
        self.assertEqual(info['last_bcast_episode'], 2)
        
    def test_passNormalSingleSeasonResourceWithStringNumber(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}'
        request.matchdict = {'label': 'game-of-thrones', 'number': '1'}
        info = SingleSeasonResource.get(SingleSeasonResource(request))
        
        self.assertEqual(info['episodes'], 2)
        self.assertEqual(info['last_bcast_episode'], 2)
        
    def test_noFoundSingleSeasonResourceNoEpisodes(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}'
        request.matchdict = {'label': 'simpsons', 'number': 1}
        season = SingleSeasonResource(request)
        
        self.assertRaises(HTTPNotFound, season.get)
        
    def test_NotFound_SingleSeasonResource(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}'  
        request.matchdict = {'label': 'dont-exists', 'number': 1}
        season  = SingleSeasonResource(request)
        
        self.assertRaises(HTTPNotFound, season.get)
        
    def test_badRequest_SingleSeasonResource(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}'  
        request.matchdict = {'label': 'game-of-thrones', 'number': 'bad'}
        season  = SingleSeasonResource(request)
        
        self.assertRaises(HTTPBadRequest, season.get)
        