import unittest
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPUnauthorized, HTTPInternalServerError

from ..resources.episodesresource import SingleEpisodesResource

# default view test
class TestMySeasonResource(unittest.TestCase):    
    def tearDown(self):
        testing.tearDown()
        
    #GET:   
    def test_passing_SingleEpisodesResource(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'game-of-thrones', 'number': 1, 'ep': 1}
        info = SingleEpisodesResource.get(SingleEpisodesResource(request))
        
        self.assertEqual(info['season'], 1)
        self.assertEqual(info['number'], 1) #episode number
        self.assertEqual(info['title'], 'everybody dies 1') #episodes title
        links = info['_links']
        self.assertEqual(links['self'], {'href': '/tvflix/shows/game-of-thrones/seasons/1/episodes/1'})
        
    def test_passing_SingleEpisodesResourceWithStrings(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'game-of-thrones', 'number': '1', 'ep': '1'}
        info = SingleEpisodesResource.get(SingleEpisodesResource(request))
        
        self.assertEqual(info['season'], 1)
        self.assertEqual(info['number'], 1) #episode number
        self.assertEqual(info['title'], 'everybody dies 1') #episodes title
        links = info['_links']
        self.assertEqual(links['self'], {'href': '/tvflix/shows/game-of-thrones/seasons/1/episodes/1'})
        
    def test_failure_SingleEpisodesResourceInvalidLabel(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'no-show', 'number': 1, 'ep': '2'}
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPNotFound, episodes.get)
        
    def test_failure_SingleEpisodesResourceNoSuchSeason(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'no-show', 'number': 3, 'ep': 1}
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPNotFound, episodes.get)
        
    def test_failure_SingleEpisodesResourceNoSuchEpisode(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'no-show', 'number': 1, 'ep': 11}
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPNotFound, episodes.get)
        
    def test_failure_SingleEpisodesResourceRandonStringAsSeason(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'no-show', 'number': 'asd', 'ep': 1}
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPNotFound, episodes.get)
        
    def test_failure_SingleEpisodesResourceRandonStringAsEpisode(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'no-show', 'number': 1, 'ep': 'asdads'}
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPNotFound, episodes.get)