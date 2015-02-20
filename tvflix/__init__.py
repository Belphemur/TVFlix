from pyramid.config import Configurator
from sqlalchemy import engine_from_config

#global variable 
engine = None
    
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """  
    global engine
    
    engine = engine_from_config(settings, 'sqlalchemy.')
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()
