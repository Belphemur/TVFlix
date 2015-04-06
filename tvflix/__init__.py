from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import Base, Session
from tvflix.models import initialize_sql
from pyramid.view import view_config

@view_config(route_name='client', renderer='templates/mytemplate.pt')
def client_view(request):
    return dict(project='TvFlix')



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    config = Configurator(settings=settings)
    initialize_sql(engine)
    config.scan('tvflix.models')
    config.include("cornice")
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route(name='client',pattern='client/')
    
    config.scan()
    return config.make_wsgi_app()
