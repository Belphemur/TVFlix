from sqlalchemy import (
    Column,
    Integer,
    Unicode,
)

from ..models import Base

class User(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True)
    username = Column(Unicode(155), nullable=False)
    password = Column(Unicode(100), nullable=False)
    api_key = Column(Unicode(64), nullable=False)
    