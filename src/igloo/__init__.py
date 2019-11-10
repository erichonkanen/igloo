import os

from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.session import SignedCookieSessionFactory

from igloo import auth
from igloo import blog
from igloo import db
from igloo import routes


def main(settings={
    'SECRET_KEY': 'dev',
    'DATABASE': os.path.join(os.getcwd(), 'igloo.sql'),
}):
    # create and configure the app
    config = Configurator(settings=settings)
    config.set_session_factory(SignedCookieSessionFactory('secret'))

    # set up jinja2.
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('templates/')

    # import routes, views, static, etc.
    config.include(routes)
    config.scan(auth)
    config.scan(blog)
    config.add_static_view(name='static', path='static')

    # set up database.
    config.add_subscriber(db.connection, NewRequest)
    config.add_request_method(auth.user, 'user')

    app = config.make_wsgi_app()

    return app
