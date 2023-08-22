"""
test web
"""


def test_guest(client, auth):
    response = client.get('/')
    assert b"Guest" in response.data
    assert b"Log In" in response.data
    assert b"Register" in response.data


def test_loggedin(client, auth):
    auth.login()
    response = client.get('/')
    print(response.data)
    assert b'Log Out' in response.data
    assert b'Logged in as' in response.data