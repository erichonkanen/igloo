import os

from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.session import SignedCookieSessionFactory

from igloo import auth
from igloo import blog
from igloo import db
from igloo import serializer
from igloo import routes


def main(settings={
    'SECRET_KEY': 'dev',
    'DATABASE': os.path.join(os.getcwd(), 'igloo.sql'),
}):
    # create and configure the app.
    config = Configurator(settings=settings)

    # set up session.
    session_factory = SignedCookieSessionFactory(
        'secret', serializer=serializer.Serializer())
    config.set_session_factory(session_factory)

    # set up jinja2.
    config.include('pyramid_jinja2')
    config.add_jinja2_search_path('templates/')

    # import routes, views, static, etc.
    config.include(routes)
    config.scan(auth)
    config.scan(blog)
    config.add_static_view(name='static', path='static')

    # set up database.
    db.init_db(config.registry)
    config.add_subscriber(db.connection, NewRequest)
    config.add_request_method(auth.user, 'user')

    app = config.make_wsgi_app()

    return app
