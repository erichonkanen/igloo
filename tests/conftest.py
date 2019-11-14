import os
import pytest
import tempfile

from webtest import TestApp

from igloo import db
from igloo import main


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = main(settings={
        'TESTING': True,
        'DATABASE': db_path,
    })
    db.init_db(app.registry)

    cwd = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(cwd, 'data.sql'), 'rb') as f:
        app.registry.db.executescript(f.read().decode('utf8'))

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return TestApp(app)


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/login',
            {'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
