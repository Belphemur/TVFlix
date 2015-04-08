import unittest
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound
from webob.multidict import MultiDict

from ..resources.searchresource import SearchShowResource, SearchEpisodeResource, showParser, episodeParser

from datetime import date

from ..models.show import Show

# default view test
class TestMySeasonResource(unittest.TestCase):    
    def tearDown(self):
        testing.tearDown()
        
    #GET show:   
    def test_passing_GetShowSearchResource(self):
        #request = testing.DummyRequest(params={'query': 'game'})
        request = testing.DummyRequest()
        request.GET = MultiDict([('query', 'game')])
        info = SearchShowResource.get(SearchShowResource(request))
        
        self.assertEqual(info['size'], 1)
        links = info['_links']
        self.assertEqual(links['self'], {'href': '/tvflix/search/shows?query=game'})
        
    def test_passing_GetShowSearchResourceMultipleQueries(self):
        request = testing.DummyRequest()
        request.GET = MultiDict([('query', 'game'), ('query', 'simpsons'), ('query', 'baz')])  
        info = SearchShowResource.get(SearchShowResource(request))
        
        self.assertEqual(info['size'], 2)
        links = info['_links']
        self.assertEqual(links['self'], {'href': '/tvflix/search/shows?query=game&query=simpsons&query=baz'})
        
    def test_failure_GetShowSearchResourceNoResults(self):
        #request = testing.DummyRequest(params={'query': 'nothing to get here'})
        request = testing.DummyRequest()
        request.GET = MultiDict([('query', 'nothing here')])
        
        info  = SearchShowResource(request)
        self.assertRaises(HTTPNotFound, info.get)
        
    def test_failure_GetShowSearchResourceMissingQuery(self):
        request = testing.DummyRequest()
        request.GET = MultiDict([])
        
        info  = SearchShowResource(request)
        self.assertRaises(HTTPNotFound, info.get)
     
    #GET episode
    def test_passing_GetEpisodeSearchResource(self):
        request = testing.DummyRequest()
        request.GET = MultiDict([('query', 'tits')])
        info = SearchEpisodeResource.get(SearchEpisodeResource(request))
        
        self.assertEqual(info['size'], 1)
        links = info['_links']
        self.assertEqual(links['self'], {'href': '/tvflix/search/episodes?query=tits'})
        
    def test_passing_GetEpisodeSearchResourceMultipleQueries(self):
        request = testing.DummyRequest()
        request.GET = MultiDict([('query', 'tits'), ('query', 'dragons'), ('query', 'baz')])
        info = SearchEpisodeResource.get(SearchEpisodeResource(request))
        
        self.assertEqual(info['size'], 2)
        links = info['_links']
        self.assertEqual(links['self'], {'href': '/tvflix/search/episodes?query=tits&query=dragons&query=baz'})
        
    def test_failure_GetEpisodeSearchResourceNoResults(self):
        request = testing.DummyRequest()
        request.GET = MultiDict([('query', 'nothing to get here')])
        
        info  = SearchEpisodeResource(request)
        self.assertRaises(HTTPNotFound, info.get)
        
    def test_failure_GetEpisodeSearchResourceNoQuery(self):
        request = testing.DummyRequest()
        request.GET = MultiDict([])
        
        info  = SearchEpisodeResource(request)
        self.assertRaises(HTTPNotFound, info.get)
        
    #other methods
    def test_TrueShowParser(self):
        show = Show.GetShowByLabel('test')
        
        self.assertTrue(showParser([], show))
        
    def test_FalseShowParser(self):
        show = Show.GetShowByLabel('test')
        
        self.assertFalse(showParser([show], show))
        
    def test_true_episodeParser(self):
        #should only be 1 episode
        show = Show.GetShowByLabel('family-guy')
        epi = show.episodes
        
        self.assertTrue(episodeParser([], epi))
        
    def test_false_episodeParser(self):
        #should only be 1 episode
        show = Show.GetShowByLabel('family-guy')
        epi = show.episodes #list
        
        self.assertFalse(episodeParser([epi[0]], epi[0]))
        
        
        
        
        