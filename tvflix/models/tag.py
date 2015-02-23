from sqlalchemy import (
    Column,
    Integer,
    Unicode,
)

from ..models import Base

class Tag(Base):
    __tablename__ = "Tags"
    tag_id = Column(Integer, primary_key=True)
    name = Column(Unicode(25), nullable=False)