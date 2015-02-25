from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from zope.sqlalchemy import ZopeTransactionExtension

Session = scoped_session(sessionmaker(extension=ZopeTransactionExtension(),
                                      autoflush=True,
                                      autocommit=False,
                                      expire_on_commit=True))
Base = declarative_base()