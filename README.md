[![Build Status](https://secure.travis-ci.org/Belphemur/TVFlix.png?branch=master)](http://travis-ci.org/Belphemur/TVFlix) [![Coverage Status](https://img.shields.io/coveralls/Belphemur/TVFlix.svg)](https://coveralls.io/r/Belphemur/TVFlix?branch=master)
#TVFlix README
##Framework
SQLAchemy, Pyramid and Cornice

##Dependencies
pyramid, pyramid_tm, SQLAlchemy, cornice, transaction, zope.sqlalchemy, waitress, nose, coverage

##Getting Started

###Virtual Environment
First you need to install/create a virtual environment: [How to](http://docs.python-guide.org/en/latest/dev/virtualenvs/)

Once you've activited it follow the next steps.

###Install the application
- cd ``directory containing this file``

- python setup.py develop

- initialize_tvflix_db development.ini

- pserve development.ini

- more information in: [Pyramid Installation Guide](http://docs.pylonsproject.org/docs/pyramid/en/latest/tutorials/wiki2/installation.html)

###URL
- http://127.0.0.1:8081/tvflix/

###Test Users
- admin: username == admin, apikey == admin

- normal user: username == user, apikey == user

##Run tests
- start enviroment

- cd ``directory containing this file``

###basic tests:
- nosetests -v tvflix

### coverage tests:
- nosetests --cover-package=tvflix --cover-erase --with-coverage


