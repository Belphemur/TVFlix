from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Table
)

from ..models import Base
from ..models.tag import Tag
    
Shows_Tag = Table('Shows_Tags', Base.metadata,
    Column('show_id', Integer, ForeignKey('Shows.show_id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('Tags.tag_id'), primary_key=True))