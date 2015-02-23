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