#TVFlix README
##Framework
SQLAchemy and Pyramid

##dependencies
pyramid, pyramid_tm, SQLAlchemy, transaction, zope.sqlalchemy, waitress, nose

##Getting Started
- cd <directory containing this file>

- $VENV/bin/python setup.py develop

- $VENV/bin/initialize_tvflix_db development.ini

- $VENV/bin/pserve development.ini

- more information in: http://docs.pylonsproject.org/docs/pyramid/en/latest/tutorials/wiki2/installation.html

##Run tests
- start enviroment

- cd <directory containing this file>

- $VENV/bin/nosetests -v tvflix

