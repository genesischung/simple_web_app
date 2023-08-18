"""
test web
"""


def test_index(client, auth):
    response = client.get('/')
    assert b"Guest" in response.data
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'Logged In' in response.data
    assert b'Enter your message:' in response.data

    response = client.post('/message', data={'user_input': "test message"})
    assert b'test message' in response.data

