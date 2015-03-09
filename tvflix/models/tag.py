from sqlalchemy import (
    Column,
    Integer,
    Unicode,
)

from sqlalchemy.orm import relationship

from ..models import Base
from ..models.show_tag import Shows_Tag

class Tag(Base):
    __tablename__ = "Tags"
    tag_id = Column(Integer, primary_key=True)
    name = Column(Unicode(25), nullable=False)
    
    show = relationship("Show", secondary=Shows_Tag, lazy='joined')