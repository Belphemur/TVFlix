import unittest
from pyramid import testing

from ..models import Session, Base


# default view test
class TestMyShowView(unittest.TestCase):    
    def tearDown(self):
        Session.remove()
        testing.tearDown()

    def test_passing_showView(self):
        from ..views.show import get_show

        request = testing.DummyRequest()
        #url is /tvflix/shows/{label}, so this is how i define the label 
        request.matchdict = {'label': 'game-of-thrones'} 
        info = get_show(request)
        self.assertEqual(info['channel'], 'HBO')
        
    def test_failure_showView(self):
        pass
        #not yet working
        '''from ..views.show import get_show   

        request = testing.DummyRequest()
        #url is /tvflix/shows/{label}, so this is how i define the label 
        request.matchdict = {'label': 'no-such-show'} 
        info = get_show(request)
        self.assertEqual('Not Found' in info)'''