[![Build Status](https://secure.travis-ci.org/Belphemur/TVFlix.png?branch=master)](http://travis-ci.org/Belphemur/TVFlix) [![Coverage Status](https://img.shields.io/coveralls/Belphemur/TVFlix.svg)](https://coveralls.io/r/Belphemur/TVFlix?branch=master)
#TVFlix README
##Framework
SQLAchemy, Pyramid and Cornice

##Dependencies
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

###basic tests:
- nosetests -v tvflix

### coverage tests:
- nosetests --cover-package=tvflix --cover-erase --with-coverage

