from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    ForeignKey,
    Text,
    Date,
    or_
)

from sqlalchemy.orm import relationship

from ..models import Base, Session


class Episode(Base):
    __tablename__ = 'Episodes'
    ep_id = Column(Integer, primary_key=True)
    show_id = Column(Integer, ForeignKey('Shows.show_id'), nullable=False)
    title = Column(Unicode(50))
    season = Column(Integer, nullable=False)
    number = Column(Integer, nullable=False)
    bcast_date = Column(Date, nullable=False)
    summary = Column(Text)
    
    show = relationship("Show", backref='Episode', foreign_keys=[show_id])

    @classmethod
    def SearchEpisodeByKeywords(cls, keywords):
        """
        Search Episode by using the keywords given
        :param keywords: string
        :return: Array of Episodes or None if no episodes found
        """
        episode = Session.query(Episode).filter(or_(
                                    Episode.title.like ('%'+ keywords +'%'),
                                    Episode.summary.like ('%'+ keywords +'%')
                                    )).all()
                                    
        if episode:
            return episode
        return None
    
    @classmethod
    def AddEpisode(cls, show = None, title=None, season=None, number=None, bcast_date=None, summary=None):
        """
        Add the wanted Episode to the database.
        :param title: string
        :param season: integer
        :param number: integer
        :param bcast_date: datetime
        :param summary: string
        :return: True if added successfully else False
        """
        if title and season and number and bcast_date and summary and show:
            try:
                Session.add(Episode(show = show, title = title, season = season, number = number,
                        bcast_date = bcast_date, summary = summary))
                return True
            except:
                return False
        return False

    def ModifyEpisode(self, title=None, season=None, number=None, bcast_date=None, summary=None):
        """
        Modify the Episode
        :param title: string
        :param season: integer
        :param number: integer
        :param bcast_date: datetime
        :param summary: string
        :return: True if modified successfully else False
        """
        try:
            if title:
                self.title = title
            if season:    
                self.season = season
            if number:
                self.number = number
            if bcast_date:
                self.bcast_date = bcast_date
            if summary:
                self.summary
            return True
        except:
            return False
    
    #Session.delete(episode) exists...
    def DeleteEpisode(self):
        """
        Delete the Episode
        :return: True if deleted, else False
        """
        try:
            Session.delete(self)
            return True
        except:
            return False