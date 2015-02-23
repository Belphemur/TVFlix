from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Table
)

#from sqlalchemy.orm import relationship

from ..models import Base

'''class Shows_Tag(Base):
    __tablename__ = "Shows_Tags"
    show_id = Column(Integer, ForeignKey('Shows.show_id'), nullable=False)
    tag_id = Column(Integer, ForeignKey('Tags.tag_id'), nullable=False)
    
    show = relationship("Show", backref='Shows_Tag', foreign_keys=[show_id])
    tag = relationship("Tag", backref='Shows_Tag', foreign_keys=[tag_id])'''
    
Shows_Tag = Table('Shows_Tags', Base.metadata,
    Column('show_id', Integer, ForeignKey('Shows.show_id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('Tags.tag_id'), primary_key=True))