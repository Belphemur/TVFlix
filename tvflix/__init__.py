from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import Base, Session
from tvflix.models import initialize_sql


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    config = Configurator(settings=settings)
    initialize_sql(engine)
    config.scan('tvflix.models')
    config.include("cornice")
    config.add_static_view('static', 'static', cache_max_age=3600)
    
    config.scan()
    return config.make_wsgi_app()
