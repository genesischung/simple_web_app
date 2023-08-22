import app.data_analysis
import pytest
from app import data_analysis

'''
Test data_analysis
'''

def test_countdown(app, client):
    response = client.get('/analysis/countdown')
    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'


def test_pitstops(app, client):
    response = client.get('/analysis/pitstops/2023/1')
    assert response.status_code == 200
    assert 'Content-Type' in response.headers
    assert response.headers['Content-Type'] == 'text/html; charset=utf-8'


def test_to_seconds():
    time1 = "1:23.123"
    assert data_analysis.to_seconds(time1) == 83.123
    time2 = "23.233"
    assert data_analysis.to_seconds(time2) == 23.233


def test_get_driver(mocker):
    mock_func = mocker.patch("app.data_collection.get_driver")
    mock_func.return_value = {'givenName': 'Hello', 'familyName': 'World'}
    assert data_analysis.get_new_driver('test') == "Hello World"


def test_lookup_driver(mocker):
    mock_db = mocker.patch("app.data_analysis.get_db")
    mock_con = mock_db.return_value
    mock_cur = mock_con.cursor.return_value
    mock_cur.execute.return_value = None
    mock_con.fetchone.return_value = {'driverId': 'zhou',
                                      'givenName':'Guanyu',
                                      'familyName':'Zhou'}

    mock_render = mocker.patch("app.data_analysis.render_template")
    mock_render.return_value = None

    assert data_analysis.lookup_driver('zhou') == None

