import datetime
from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Text,
    DateTime,
)
from sqlalchemy.orm import relationship

from ..models import Base, Session


class Comment(Base):
    __tablename__ = 'Comments'
    comment_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'), nullable=True)
    show_id = Column(Integer, ForeignKey('Shows.show_id'), nullable=False)
    comment = Column(Text, nullable=False)
    posted = Column(DateTime, nullable=False)
    updated = Column(DateTime)

    user = relationship("User", backref='Comment', foreign_keys=[user_id])
    show = relationship("Show", backref='Comment', foreign_keys=[show_id])

    @classmethod
    def AddComment(cls, message, Show, User):
        """
        Add the wanted comment to the database. Check if the User have already posted a comment for the Show.
        :param message: string
        :param Show: Show
        :param User: User
        :return: True if added successfully else False
        """
        if User and Show:
            comment = User.GetCommentForShow(Show)
            if not comment:
                Session.add(Comment(comment=message, user=User, show=Show, posted=datetime.datetime.now()))
                Session.flush()
                return True
        return None

    def ModifyComment(self, message):
        """
        Modify the message of the comment
        :param message: string
        :return: True if modified else False
        """
        try:
            self.comment = message
            self.updated = datetime.datetime.now()
            return True
        except:
            return False
    
    #i would rather use Session.delete(comment)
    def DeleteComment(self):
        """
        Delete the comment
        :return: True if deleted, else False
        """
        try:
            Session.delete(self)
            return True
        except:
            return False
