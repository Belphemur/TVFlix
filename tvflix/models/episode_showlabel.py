from sqlalchemy.sql.schema import Table
from ..models import Base

__author__ = 'Antoine'


Episode_ShowLabel = Table("Episode_ShowLabel",  Base.metadata, autoload=True)