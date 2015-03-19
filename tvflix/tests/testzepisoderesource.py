import unittest
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest

from ..resources.episodesresource import EpisodesResource

# default view test
class TestMySeasonResource(unittest.TestCase):    
    def tearDown(self):
        testing.tearDown()
        
    def test_passing_episodesResource(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes'
        request.matchdict = {'label': 'game-of-thrones', 'number': 1}
        info = EpisodesResource.get(EpisodesResource(request))
        
        self.assertEqual(info['size'], 2)
        links = info['_links']
        self.assertEqual(links['self'], {'href': '/tvflix/shows/game-of-thrones/seasons/1/episodes'})
        
    def test_failure_episodesResourceInvalidLabel(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes'
        request.matchdict = {'label': 'no-show', 'number': 1}
        episodes  = EpisodesResource(request)
        self.assertRaises(HTTPNotFound, episodes.get)
        
    def test_failure_episodesResourceNoSuchSeasonNumber(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes'
        #no such season
        request.matchdict = {'label': 'game-of-thrones', 'number': 3}
        episodes  = EpisodesResource(request)
        self.assertRaises(HTTPNotFound, episodes.get)
        
    def test_failure_episodesResourceInvalidSeasonNumber(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes'
        #no such season
        request.matchdict = {'label': 'game-of-thrones', 'number': 'asd'}
        episodes  = EpisodesResource(request)
        self.assertRaises(HTTPBadRequest, episodes.get)