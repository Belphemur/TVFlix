import unittest
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound

from ..resources.searchresource import SearchShowResource, SearchEpisodeResource, showParser, episodeParser

from datetime import date

from ..models.show import Show

# default view test
class TestMySeasonResource(unittest.TestCase):    
    def tearDown(self):
        testing.tearDown()
        
    #GET show:   
    def test_passing_GetShowSearchResource(self):
        request = testing.DummyRequest(params={'query': 'game'})
        info = SearchShowResource.get(SearchShowResource(request))
        
        self.assertEqual(info['size'], 1)
        links = info['_links']
        self.assertEqual(links['self'], {'href': '/tvflix/search/shows?query=game&'})
        
    def test_failure_GetShowSearchResourceNoResults(self):
        request = testing.DummyRequest(params={'query': 'nothing to get here'})
        
        info  = SearchShowResource(request)
        self.assertRaises(HTTPNotFound, info.get)
        
    def test_failure_GetShowSearchResourceMissingQuery(self):
        request = testing.DummyRequest()
        
        info  = SearchShowResource(request)
        self.assertRaises(HTTPNotFound, info.get)
     
    #GET episode
    def test_passing_GetEpisodeSearchResource(self):
        request = testing.DummyRequest(params={'query': 'tits'})
        info = SearchEpisodeResource.get(SearchEpisodeResource(request))
        
        self.assertEqual(info['size'], 1)
        links = info['_links']
        self.assertEqual(links['self'], {'href': '/tvflix/search/episodes?query=tits&'})
        
    def test_failure_GetEpisodeSearchResourceNoResults(self):
        request = testing.DummyRequest(params={'query': 'nothing to get here'})
        
        info  = SearchEpisodeResource(request)
        self.assertRaises(HTTPNotFound, info.get)
        
    def test_failure_GetEpisodeSearchResourceNoQuery(self):
        request = testing.DummyRequest()
        
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
        
        
        
        
        