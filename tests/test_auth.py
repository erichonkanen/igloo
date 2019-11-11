import pytest


def test_register(client, app):
    assert client.get('/register').status_code == 200

    response = client.post(
        '/register',
        {'username': 'a', 'password': 'a'},
    )

    assert response.status_code == 200

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
