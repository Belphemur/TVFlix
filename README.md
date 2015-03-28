[![Build Status](https://secure.travis-ci.org/Belphemur/TVFlix.png?branch=master)](http://travis-ci.org/Belphemur/TVFlix) [![Coverage Status](https://img.shields.io/coveralls/Belphemur/TVFlix.svg)](https://coveralls.io/r/Belphemur/TVFlix?branch=master)
#TVFlix README
##Framework
SQLAchemy, Pyramid and Cornice

##Dependencies
pyramid, pyramid_tm, SQLAlchemy, cornice, transaction, zope.sqlalchemy, waitress, nose, coverage

##Getting Started
--for windows you don't need to use '$VENV/bin/'
- cd <directory containing this file>

- $VENV/bin/python setup.py develop

- $VENV/bin/initialize_tvflix_db development.ini

- $VENV/bin/pserve development.ini

- more information in: http://docs.pylonsproject.org/docs/pyramid/en/latest/tutorials/wiki2/installation.html

##URL
- http://127.0.0.1:8081/tvflix/

##test users
-admin: username == admin, apikey == admin
-normal user: username == user, apikey == user

##Run tests
- start enviroment

- cd <directory containing this file>

###basic tests:
- nosetests -v tvflix

### coverage tests:
- nosetests --cover-package=tvflix --cover-erase --with-coverage


