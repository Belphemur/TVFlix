import unittest
import transaction
from datetime import date, datetime

from pyramid import testing

from .models import Session

from .models.user import User
from .models.show import Show
from .models.episode import Episode
from .models.user import User
from .models.comment import Comment
from .models.tag import Tag
from .models.show_tag import Shows_Tag


# default view test
class TestMyViewSuccessCondition(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine

        engine = create_engine('sqlite://')
        from .models import Base

        Session.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = User(username='test user44', password='password', api_key="test", admin=False)
            Session.add(model)

    def tearDown(self):
        Session.remove()
        testing.tearDown()

    def test_passing_view(self):
        from .views import my_view

        request = testing.DummyRequest()
        info = my_view(request)
        #self.assertEqual(info['one'].name, 'one')
        self.assertEqual(info['project'], 'tvflix')


#testing database
class TestMyDatabaseMethodsAndStuff(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine

        engine = create_engine('sqlite://')
        from .models import Base

        Session.configure(bind=engine)
        Base.metadata.create_all(engine)

        #lets add users
        with transaction.manager:
            user1 = User(username='test user 1', password='password', api_key='asdasd', admin=False)
            user2 = User(username='test user 2', password='password', api_key='asd', admin=True)
            Session.add(user1)
            Session.add(user2)

        #Shows
        with transaction.manager:
            show1 = Show(showlabel='game-of-thrones', title=u'Game of Thrones',
                         start_year=2009, end_year=2016, bcast_day=6, summary="Everybody dies", channel="HBO")

            show2 = Show(showlabel='test', title=u'test',
                         start_year=2011, end_year=2016, bcast_day=6, summary="Everybody disses", channel="test")

            Session.add(show1)
            Session.add(show2)

        #Episodes
        with transaction.manager:
            session = Session()
            epi1 = Episode(show_id=1, title="everybody dies 1", season=1, number=1,
                           bcast_date=date.today(), summary='Series starts, everybody are still alive')

            epi2 = Episode(show_id=1, title="tits", season=1, number=2,
                           bcast_date=date.today(), summary='Just boobs')

            epi3 = Episode(show_id=1, title="Dragons", season=2, number=1,
                           bcast_date=date.today(), summary='Boobs and dragons')

            Session.add(epi1)
            Session.add(epi2)
            Session.add(epi3)

        #Comments
        with transaction.manager:
            com1 = Comment(user_id=2, show_id=1, comment="OH god no, why everyone keeps dying!??!! Bad show",
                           posted=datetime.now(), updated=None)

            com2 = Comment(user_id=1, show_id=1, comment="buhahaaa",
                           posted=datetime.now(), updated=None)

            Session.add(com1)
            Session.add(com2)

        with transaction.manager:
            tag1 = Tag(name='Drama')
            tag2 = Tag(name='Nudity')

            Session.add(tag1)
            Session.add(tag2)

        #linking the tags and shows
        with transaction.manager:
            conn = engine.connect()
            conn.execute(Shows_Tag.insert(), [
                {'show_id': 1, 'tag_id': 1},
                {'show_id': 1, 'tag_id': 2}])

            conn.close()

    def tearDown(self):
        Session.remove()
        testing.tearDown()


    #actual tests
    #testing methods for show
    def testingGetShowByLabel(self):
        show = Show.GetShowByLabel('game-of-thrones')
        self.assertEqual(str(show.title), u'Game of Thrones')

    def testingGetShowByLabelFailureCondition(self):
        show = Show.GetShowByLabel('no-show')
        self.assertIsNone(show)

    def testShows_SearchShowsByKeywords(self):
        #should get the same show each time
        show1 = Show.SearchShowsByKeywords('2009')
        show2 = Show.SearchShowsByKeywords('dies')
        show3 = Show.SearchShowsByKeywords('game')

        #show's are lists     
        self.assertEqual(show1[0], show2[0])
        self.assertEqual(show1[0], show3[0])

    def testShows_SearchShowsByKeywordsFailureCondition(self):
        show = Show.SearchShowsByKeywords('fail')

        self.assertIsNone(show)

    def testGetEpisodesForShow(self):
        #get show
        show = Show.GetShowByLabel('game-of-thrones')

        for epi in show.GetEpisodes():
            self.assertEqual(epi.show_id, 1)

    def testGetEpisodesForShowFailCondition(self):
        #get show
        show = Show.GetShowByLabel('test')

        self.assertIsNone(show.GetEpisodes())

    def testGetEpisodesForSeason(self):
        show = Show.GetShowByLabel('game-of-thrones')
        season = 1
        epi = show.GetEpisodeForSeason(season)

        for ep in epi:
            self.assertEqual(ep.season, season)

    def testGetEpisodesForSeasonFailCondition(self):
        show = Show.GetShowByLabel('game-of-thrones')
        season = 3
        epi = show.GetEpisodeForSeason(season)

        self.assertIsNone(epi)

    def testGetComments(self):
        show = Show.GetShowByLabel('game-of-thrones')
        for com in show.GetComments():
            self.assertEqual(com.show_id, 1)

    def testGetCommentsFailCondition(self):
        show = Show.GetShowByLabel('test')
        self.assertIsNone(show.GetComments())

    def testGetTags(self):
        show = Show.GetShowByLabel('game-of-thrones')
        tag = show.GetTags()
        self.assertEqual(tag[0].name, "Drama")
        self.assertEqual(tag[1].name, "Nudity")

    def testGetTagsFailcondition(self):
        show = Show.GetShowByLabel('test')
        self.assertIsNone(show.GetTags())

    #tests for user
    def testGetUserByApiKey(self):
        user = User.GetUserByApiKey('asdasd')
        self.assertEqual(user.user_id, 1)

    def testGetUserByApiKeyFailcondition(self):
        user = User.GetUserByApiKey('nokey')
        self.assertIsNone(user)

    def testGetUserComment(self):
        user = User.GetUserByApiKey('asdasd')
        show = Show.GetShowByLabel('game-of-thrones')
        comment = user.GetCommentForShow(show)
        self.assertEqual(comment.comment_id, 2)

    def testGetUserCommentFailureCondition(self):
        user = User.GetUserByApiKey('asdasd')
        show = Show.GetShowByLabel('noshow')
        comment = user.GetCommentForShow(show)
        self.assertIsNone(comment)

    #test comments
    def testAddComment(self):
        user = User.GetUserByApiKey('asd')
        show = Show.GetShowByLabel('test')
        self.assertTrue(Comment.AddComment('test comment!! wuhuu', show, user))
        comment = user.GetCommentForShow(show)
        self.assertEqual(comment.comment, 'test comment!! wuhuu')

    def testAddCommentUserFailure(self):
        user = User.GetUserByApiKey('asd11')
        show = Show.GetShowByLabel('test')
        self.assertFalse(Comment.AddComment('test comment!! wuhuu', show, user))

    def testAddCommentShowFailure(self):
        user = User.GetUserByApiKey('asd')
        show = Show.GetShowByLabel('noshow')
        self.assertFalse(Comment.AddComment('test comment!! wuhuu', show, user))

    def testAddCommentSecondCommentFailure(self):
        user = User.GetUserByApiKey('asd')
        show = Show.GetShowByLabel('game-of-thrones')
        self.assertFalse(Comment.AddComment('test comment!! wuhuu', show, user))

    #can't really fail
    def testModifyComment(self):
        user = User.GetUserByApiKey('asdasd')
        show = Show.GetShowByLabel('game-of-thrones')
        comment = user.GetCommentForShow(show)
        self.assertTrue(comment.ModifyComment('New msg'))
        comment = user.GetCommentForShow(show)
        self.assertEqual(comment.comment, 'New msg')

    #doesn't have failing condition. either comment is or isn't
    def testDeleteComment(self):
        user = User.GetUserByApiKey('asdasd')
        show = Show.GetShowByLabel('game-of-thrones')
        comment = user.GetCommentForShow(show)
        self.assertTrue(comment.DeleteComment())
        self.assertIsNone(user.GetCommentForShow(show))

    #tests for episodes
    def testSearchEpisodeByKeywords(self):
        epi1 = Episode.SearchEpisodeByKeywords('boobs')
        epi2 = Episode.SearchEpisodeByKeywords('tits')

        for i in epi1:
            self.assertEqual(i.show_id, 1)

        for i in epi2:
            self.assertEqual(i.number, 2)

    def testSearchEpisodeByKeywordsFailCondition(self):
        self.assertIsNone(Episode.SearchEpisodeByKeywords('failure'))

    def testAddNewEpisode(self):
        show = Show.GetShowByLabel('game-of-thrones')
        self.assertTrue(Episode.AddEpisode(show, 'test2', 2, 3, date.today(), 'blaalaaa'))
        self.assertTrue(show.GetEpisodeForSeason(2))

    def testAddNewEpisodeFailconditionOneMissing(self):
        self.assertFalse(Episode.AddEpisode('test2', 3, date.today(), 'blaalaaa'))

    def testUpdatingEpisode(self):
        epi = Episode.SearchEpisodeByKeywords('tits')
        self.assertTrue(epi[0].ModifyEpisode(title='modifiedTitle', summary='asdasdas'))
        self.assertIsNotNone(Episode.SearchEpisodeByKeywords('modifiedTitle'))

    #if episode then it works    
    def testDeleteEpisode(self):
        show = Show.GetShowByLabel('game-of-thrones')
        for epi in show.GetEpisodeForSeason(1):
            epi.DeleteEpisode()

        self.assertIsNone(show.GetEpisodeForSeason(1))
        
        

    
