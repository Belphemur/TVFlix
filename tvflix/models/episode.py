from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    ForeignKey,
    Text,
    Date,
)

from sqlalchemy.orm import relationship

from ..models import Base


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
        :return: Array of Episodes
        """
        return None
    
    @classmethod
    def AddEpisode(cls,  title, season, number, bcast_date, summary):
        """
        Add the wanted Episode to the database.
        :param title: string
        :param season: integer
        :param number: integer
        :param bcast_date: datetime
        :param summary: string
        :return: True if added successfully else False
        """
        return None

    def ModifyEpisode(self, title, season, number, bcast_date, summary):
        """
        Modify the Episode
        :param title: string
        :param season: integer
        :param number: integer
        :param bcast_date: datetime
        :param summary: string
        :return: True if modified successfully else False
        """
        return None

    def DeleteEpisode(self):
        """
        Delete the Episode
        :return: True if deleted, else False
        """
        return None