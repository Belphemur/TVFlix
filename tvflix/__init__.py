from pyramid.config import Configurator
from sqlalchemy import engine_from_config
import transaction

from .models import Base, Session
from tvflix.models import initialize_sql
from tvflix.models.show import Show
from tvflix.models.user import User


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    config = Configurator(settings=settings)
    initialize_sql(engine)
    config.scan('tvflix.models')
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
