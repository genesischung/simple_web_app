from app import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'


def test_index_response_code(app, client):
    response = client.get('/')
    assert response.status_code == 200


def test_index_headers(app, client):
    response = client.get('/')
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'


def test_health(client, auth):
    response = client.get('/health')
    assert response.status_code == 200


def test_messageboard(client, auth):
    response = client.get('/messageboard')
    assert response.status_code == 200

def test_pitstops(client, auth):
    response = client.get('/pitstops')
    assert response.status_code == 200
