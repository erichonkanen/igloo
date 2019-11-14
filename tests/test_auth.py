import pytest


def test_register(client, app):
    assert client.get('/register').status_code == 200

    response = client.post(
        '/register',
        {'username': 'a', 'password': 'a'},
    )

    assert response.status_code == 302
    assert 'http://localhost/login' == response.headers['Location']
    assert app.registry.db.execute(
        "select * from user where username = 'a'",
    ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/register',
        {'username': username, 'password': password}
    )
    assert message in response.body


def test_login(client, auth):
    assert client.get('/login').status_code == 200

    response = auth.login()

    assert response.headers['Location'] == 'http://localhost/'

    resp = client.get('/')

    assert resp.status_code == 200


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    resp = auth.login(username, password)

    assert message in resp.body


def test_logout(client, auth):
    auth.login()

    resp = auth.logout()

    assert resp.headers['Location'] == 'http://localhost/'
    assert resp.status_code == 302
