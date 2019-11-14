def test_index(client, auth):
    response = client.get('/')
    assert b"Log In" in response.body
    assert b"Register" in response.body

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.body
    assert b'test title' in response.body
    assert b'by test on 2018-01-01' in response.body
    assert b'test\nbody' in response.body
    assert b'href="http://localhost/blog/1/update"' in response.body
