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

    def GetCommentForShow(self,Show):
        """
        Return the only comment that the user wrote for the wanted show.
        :param Show: Show
        :return: None if the comment doesn't exists, else the Comment
        """
        if Show:
            comment = Session.query(Comment).filter(and_(Comment.show_id == Show.show_id, Comment.user_id == self.user_id)).first()
            if comment:
                return comment
        return None
    