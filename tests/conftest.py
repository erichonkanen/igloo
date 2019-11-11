import pytest

from webtest import TestApp

from igloo import main


@pytest.fixture
def app():
    app = main()

    yield app


@pytest.fixture
def client(app):
    return TestApp(app)


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='aa', password='aa'):
        return self._client.post(
            '/login',
            {'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
