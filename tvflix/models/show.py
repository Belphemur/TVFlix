from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    Text,
)

from ..models import Base

class Show(Base):
    __tablename__ = "Shows"
    show_id = Column(Integer, primary_key=True)
    showlabel = Column(Unicode(100), nullable=False)
    title = Column(Unicode(100), nullable=False)
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer)
    bcast_day = Column(Integer)
    summary = Column(Text, nullable=False)
    channel = Column(Unicode(25), nullable=False)
    