import unittest
from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest, HTTPUnauthorized, HTTPInternalServerError, HTTPNoContent

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
        request.matchdict = {'label': 'game-of-thrones', 'number': 3, 'ep': 1}
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPNotFound, episodes.get)
        
    def test_failure_SingleEpisodesResourceNoSuchEpisode(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'game-of-thrones', 'number': 1, 'ep': 11}
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPNotFound, episodes.get)
        
    def test_failure_SingleEpisodesResourceRandonStringAsSeason(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'game-of-thrones', 'number': 'asd', 'ep': 1}
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPNotFound, episodes.get)
        
    def test_failure_SingleEpisodesResourceRandonStringAsEpisode(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'game-of-thrones', 'number': 1, 'ep': 'asdads'}
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPNotFound, episodes.get)
        
    #PUT
    def test_passing_PostSingleEpisodesResource(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'game-of-thrones', 'number': 1, 'ep': 2}
        request.headers = {'apikey': 'asd'} #correct admin key
        request.json_body = {"title": "New title",
                            "season": 1,
                            "bcast_date": "2012-03-10",
                            "number": 2,
                            "summary": "new summary"
                            }
                            
        info = SingleEpisodesResource.put(SingleEpisodesResource(request))
        
        #self.assertEqual(info['title'], "New title")
        self.assertEqual(info['season'], 1)
        self.assertEqual(info['number'], 2)
        self.assertEqual(info['bcast_date'], "2012-03-10")
        self.assertEqual(info['summary'], "new summary")
        
    def test_passing_PostSingleEpisodesResourceValuesAreStrings(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'game-of-thrones', 'number': '1', 'ep': '2'}
        request.headers = {'apikey': 'asd'} #correct admin key
        request.json_body = {"title": "New title",
                            "season": '1',
                            "bcast_date": "2012-03-11",
                            "number": '2',
                            "summary": "new summaryyy"
                            }
                            
        info = SingleEpisodesResource.put(SingleEpisodesResource(request))
        
        #self.assertEqual(info['title'], "New title")
        self.assertEqual(info['season'], 1)
        self.assertEqual(info['number'], 2)
        self.assertEqual(info['bcast_date'], "2012-03-11")
        self.assertEqual(info['summary'], "new summaryyy")
        
    def test_failure_PostSingleEpisodesResourceNoRealApiKey(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'game-of-thrones', 'number': 1, 'ep': 2}
        request.headers = {'apikey': 'asdaaaaaa'} #correct admin key
        request.json_body = {"title": "New title",
                            "season": 1,
                            "bcast_date": "2012-03-10",
                            "number": 2,
                            "summary": "new summary"
                            }
                            
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPUnauthorized, episodes.put)
        
    def test_failure_PostSingleEpisodesResourceNotAnAdmin(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'game-of-thrones', 'number': 1, 'ep': 2}
        request.headers = {'apikey': 'asdasd'}
        request.json_body = {"title": "New title",
                            "season": 1,
                            "bcast_date": "2012-03-10",
                            "number": 2,
                            "summary": "new summary"
                            }
                            
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPUnauthorized, episodes.put)    
        
    def test_failure_PostSingleEpisodesResourceNoHeader(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'game-of-thrones', 'number': 1, 'ep': 2}
        request.json_body = {"title": "New title",
                            "season": 1,
                            "bcast_date": "2012-03-10",
                            "number": 2,
                            "summary": "new summary"
                            }
                            
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPUnauthorized, episodes.put)
        
    def test_failure_PostSingleEpisodesResourceEpisodeNumberMissMatch(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'game-of-thrones', 'number': 1, 'ep': 3}
        request.headers = {'apikey': 'asd'} #correct admin key
        request.json_body = {"title": "New title",
                            "season": 1,
                            "bcast_date": "2012-03-10",
                            "number": 2,
                            "summary": "new summary"
                            }
                            
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPBadRequest, episodes.put)
        
    def test_failure_PostSingleEpisodesResourceSeasonNumberMissMatch(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'game-of-thrones', 'number': 12, 'ep': 2}
        request.headers = {'apikey': 'asd'} #correct admin key
        request.json_body = {"title": "New title",
                            "season": 1,
                            "bcast_date": "2012-03-10",
                            "number": 2,
                            "summary": "new summary"
                            }
                            
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPBadRequest, episodes.put) 
        
    def test_failure_PostSingleEpisodesResourceValuesAreIncorrectlyNamed(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'game-of-thrones', 'number': 12, 'ep': 2}
        request.headers = {'apikey': 'asd'} #correct admin key
        request.json_body = {"title": "New title",
                            "asd": 1,
                            "bcast_date": "2012-03-10",
                            "number": 2,
                            "summary": "new summary"
                            }
                            
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPBadRequest, episodes.put)
        
    def test_failure_PostSingleEpisodesResourceNoJsonBody(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'game-of-thrones', 'number': 12, 'ep': 2}
        request.headers = {'apikey': 'asd'} #correct admin key
                            
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPBadRequest, episodes.put)
        
    def test_failure_PostSingleEpisodesResourceBadDateFormat(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'game-of-thrones', 'number': 1, 'ep': 2}
        request.headers = {'apikey': 'asd'} #correct admin key
        request.json_body = {"title": "New title",
                            "number": 1,
                            "bcast_date": "2012703/10",
                            "number": 2,
                            "summary": "new summary"
                            }
                            
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPBadRequest, episodes.put)
        
    def test_failure_PostSingleEpisodesResourceNoShow(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'no-show', 'number': 1, 'ep': 2}
        request.headers = {'apikey': 'asd'} #correct admin key
        request.json_body = {"title": "New title",
                            "asd": 1,
                            "bcast_date": "2012-03-10",
                            "number": 2,
                            "summary": "new summary"
                            }
                            
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPNotFound, episodes.put)
        
    def test_failure_PostSingleEpisodesResourceNumberInURLIsString(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'no-show', 'number': 'asda', 'ep': 2}
        request.headers = {'apikey': 'asd'} #correct admin key
        request.json_body = {"title": "New title",
                            "asd": 1,
                            "bcast_date": "2012-03-10",
                            "number": 2,
                            "summary": "new summary"
                            }
                            
        episodes  = SingleEpisodesResource(request)
        self.assertRaises(HTTPNotFound, episodes.put)
       
    #DELETE
    def test_passing_DeleteSingleEpisodesResource(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'family-guy', 'number': 0, 'ep': 1}
        request.headers = {'apikey': 'asd'} #correct admin key
                            
        info  = SingleEpisodesResource(request)
        self.assertRaises(HTTPNoContent, info.delete)
        
    def test_failure_DeleteSingleEpisodesResourceIncorrectApikey(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'family-guy', 'number': '0', 'ep': '1'}
        request.headers = {'apikey': 'asdasd'} #incorrect admin key
                            
        info  = SingleEpisodesResource(request)
        self.assertRaises(HTTPUnauthorized, info.delete)
        
    def test_failure_DeleteSingleEpisodesResourceNoHeader(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'family-guy', 'number': 0, 'ep': 1}
                            
        info  = SingleEpisodesResource(request)
        self.assertRaises(HTTPUnauthorized, info.delete)
        
    def test_passing_DeleteSingleEpisodesResourceNoEpisode(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'family-guy', 'number': 1, 'ep': 1}
        request.headers = {'apikey': 'asd'} #correct admin key
                            
        info  = SingleEpisodesResource(request)
        self.assertRaises(HTTPNotFound, info.delete)
        
    def test_passing_DeleteSingleEpisodesResourceRandomStringsAsNumber(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'family-guy', 'number': 'asdasd', 'ep': 1}
        request.headers = {'apikey': 'asd'} #correct admin key
                            
        info  = SingleEpisodesResource(request)
        self.assertRaises(HTTPNotFound, info.delete)
        
    def test_passing_DeleteSingleEpisodesResourceRandomStringsAsEp(self):
        request = testing.DummyRequest()
        #url '/tvflix/shows/{label}/seasons/{number}/episodes/{ep}'
        request.matchdict = {'label': 'family-guy', 'number': 0, 'ep': 'asdasd'}
        request.headers = {'apikey': 'asd'} #correct admin key
                            
        info  = SingleEpisodesResource(request)
        self.assertRaises(HTTPNotFound, info.delete)
        
    
        
        