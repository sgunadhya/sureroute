from pyramid.config import Configurator
from sqlalchemy import engine_from_config


print("hello")

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('deform_static', 'deform:static', cache_max_age=3600)
    config.add_static_view('deform_bootstrap_static', 'deform_bootstrap:static', cache_max_age=3600)
    config.add_jinja2_search_path("sureroute:templates")
    config.add_route('home', '/')
    config.add_route('sureroute', '/sureroutes')
    config.add_route('quickfixes', '/quickfixes')
    config.add_route('add_sureroute', '/sureroute/new')
    config.add_route('add_quickfix', '/quickfix/new')
    config.add_route('sureroute_results', '/sureroute/{id}')
    config.add_route('test', '/test')
    config.add_route('test1', '/test1')

    config.scan()
    return config.make_wsgi_app()

# if __name__ == '__main__':
#     server = make_server('0.0.0.0', 8080, main())
#     server.serve_forever()
