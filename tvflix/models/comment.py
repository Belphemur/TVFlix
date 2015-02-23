from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Text,
    DateTime,
)
from sqlalchemy.orm import relationship

from ..models import Base

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