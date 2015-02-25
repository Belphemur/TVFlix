from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    and_
)
from sqlalchemy.orm import relationship
from sqlalchemy.types import Boolean

from ..models import Base, Session
from ..models.comment import Comment


class User(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True)
    username = Column(Unicode(155), nullable=False)
    password = Column(Unicode(100), nullable=False)
    api_key = Column(Unicode(64), nullable=False)
    admin = Column(Boolean)
    comments = relationship("Comment")
    comments_dynamic = relationship("Comment", lazy="dynamic")

    @classmethod
    def GetUserByApiKey(cls, apiKey):
        """
        Return an user based on their API_KEY
        :param apiKey: string
        :return: an User if found else None
        """
        user = Session.query(User).filter(User.api_key == apiKey).first()
        if user:
            return user
        return None

    def GetCommentForShow(self, show):
        """
        Return the only comment that the user wrote for the wanted show.
        :param show: Show
        :return: None if the comment doesn't exists, else the Comment
        """
        if show:
            comment = self.comments_dynamic.filter(Comment.show == show).first()
            if comment:
                return comment
        return None
    