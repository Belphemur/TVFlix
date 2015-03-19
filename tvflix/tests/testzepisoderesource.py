import unittest
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPUnauthorized, HTTPInternalServerError

from ..resources.episodesresource import EpisodesResource

# default view test
class TestMySeasonResource(unittest.TestCase):    
    def tearDown(self):
        testing.tearDown()
        
    #GET:   
    def test_passing_episodesResource(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes'
        request.matchdict = {'label': 'game-of-thrones', 'number': 1}
        info = EpisodesResource.get(EpisodesResource(request))
        
        self.assertEqual(info['size'], 2)
        links = info['_links']
        self.assertEqual(links['self'], {'href': '/tvflix/shows/game-of-thrones/seasons/1/episodes'})
        
    def test_passing_episodesResourceWithNumberAsString(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes'
        request.matchdict = {'label': 'game-of-thrones', 'number': '1'}
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
        self.assertRaises(HTTPNotFound, episodes.get)
        
    #POST:
    def test_passing_PostEpisodesResource(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/'
        request.matchdict = {'label': 'test', 'number': 1}
        request.headers = {'apikey': 'asd'}
        request.json_body = {"title": "Dragons",
                            "season": 1,
                            "bcast_date": "2015-03-10",
                            "number": 5,
                            "summary": "great episode"
                            }
                            
        info = EpisodesResource.post(EpisodesResource(request))
        
        self.assertEqual(info['title'], "Dragons")
        self.assertEqual(info['season'], 1)
        self.assertEqual(info['number'], 5)
        
    def test_passing_PostEpisodesResourceIntAreStrings(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/'
        request.matchdict = {'label': 'test', 'number': 1}
        request.headers = {'apikey': 'asd'}
        request.json_body = {"title": "Dragons",
                            "season": '1',
                            "bcast_date": "2015-03-10",
                            "number": '6',
                            "summary": "great episode"
                            }
                            
        info = EpisodesResource.post(EpisodesResource(request))
        
        self.assertEqual(info['title'], "Dragons")
        self.assertEqual(info['season'], 1)
        self.assertEqual(info['number'], 6)
        
    def test_failure_PostEpisodesResourceWrongApikey(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/'
        request.matchdict = {'label': 'test', 'number': 1}
        request.headers = {'apikey': 'wrong-api-key'}
        request.json_body = {"title": "Dragons",
                            "season": 1,
                            "bcast_date": "2015-03-10",
                            "number": 5,
                            "summary": "great episode"
                            }
                            
        episode  = EpisodesResource(request)

        self.assertRaises(HTTPUnauthorized, episode.post)
        
    def test_failure_PostEpisodesResourceNoApikey(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/'
        request.matchdict = {'label': 'test', 'number': 1}
        request.headers = {'asd': 'asd'}
        request.json_body = {"title": "Dragons",
                            "season": 1,
                            "bcast_date": "2015-03-10",
                            "number": 5,
                            "summary": "great episode"
                            }
                            
        episode  = EpisodesResource(request)

        self.assertRaises(HTTPUnauthorized, episode.post)
        
    def test_failure_PostEpisodesResourceNotAdmin(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/'
        request.matchdict = {'label': 'test', 'number': 1}
        request.headers = {'apikey': 'asdasd'} #shouldn't be an admin's apikey
        request.json_body = {"title": "Dragons",
                            "season": 1,
                            "bcast_date": "2015-03-10",
                            "number": 5,
                            "summary": "great episode"
                            }
                            
        episode  = EpisodesResource(request)

        self.assertRaises(HTTPUnauthorized, episode.post)
        
    def test_failure_PostEpisodesResourceInvalidLabel(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes'
        request.matchdict = {'label': 'no-show', 'number': 1}
        episodes  = EpisodesResource(request)
        self.assertRaises(HTTPNotFound, episodes.post)
        
    def test_failure_PostEpisodesResourceInvalidNumber(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes'
        request.matchdict = {'label': 'test', 'number': 'asd'}
        episodes  = EpisodesResource(request)
        self.assertRaises(HTTPNotFound, episodes.post)
    
    def test_failure_PostEpisodesResourceNoJson(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes'
        request.matchdict = {'label': 'test', 'number': 1}
        request.headers = {'apikey': 'asd'} #correct admins key
        episodes  = EpisodesResource(request)
        self.assertRaises(HTTPBadRequest, episodes.post)
        
    def test_failure_PostEpisodesResourceEpiNumberIsString(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes'
        request.matchdict = {'label': 'test', 'number': 1}
        request.headers = {'apikey': 'asd'} #correct admins key
        request.json_body = {"title": "Dragons",
                            "season": 1,
                            "bcast_date": "2015-03-10",
                            "number": 'asd',
                            "summary": "great episode"
                            }
        episodes  = EpisodesResource(request)
        self.assertRaises(HTTPBadRequest, episodes.post)
        
    def test_failure_PostEpisodesResourceSeasonNumberIsString(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes'
        request.matchdict = {'label': 'test', 'number': 1}
        request.headers = {'apikey': 'asd'} #correct admins key
        request.json_body = {"title": "Dragons",
                            "season": 'asdasd',
                            "bcast_date": "2015-03-10",
                            "number": '12',
                            "summary": "great episode"
                            }
        episodes  = EpisodesResource(request)
        self.assertRaises(HTTPBadRequest, episodes.post)
        
    def test_failure_PostEpisodesResourceSeasonNumberAndURLNumberWontMatch(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes'
        request.matchdict = {'label': 'test', 'number': 1}
        request.headers = {'apikey': 'asd'} #correct admins key
        request.json_body = {"title": "Dragons",
                            "season": 2,
                            "bcast_date": "2015-03-10",
                            "number": '143',
                            "summary": "great episode"
                            }
        episodes  = EpisodesResource(request)
        self.assertRaises(HTTPBadRequest, episodes.post)
        
    def test_failure_PostEpisodesResourceEpisodeExists(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes'
        request.matchdict = {'label': 'game-of-thrones', 'number': 1}
        request.headers = {'apikey': 'asd'} #correct admins key
        request.json_body = {"title": "Dragons",
                            "season": 1,
                            "bcast_date": "2015-03-10",
                            "number": 1,
                            "summary": "great episode"
                            }
        episodes  = EpisodesResource(request)
        self.assertRaises(HTTPInternalServerError, episodes.post)
        
    def test_failure_PostEpisodesResourceDateIsInWrongFormat(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes'
        request.matchdict = {'label': 'test', 'number': 1}
        request.headers = {'apikey': 'asd'} #correct admins key
        request.json_body = {"title": "Dragons",
                            "season": 1,
                            "bcast_date": "2015/03/10",
                            "number": 123,
                            "summary": "great episode"
                            }
        episodes  = EpisodesResource(request)
        self.assertRaises(HTTPBadRequest, episodes.post)
