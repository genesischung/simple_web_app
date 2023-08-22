import pytest
from app import data_collection

'''
Test data collection
'''


def test_get_next_race(mocker):
    mocker_requests = mocker.patch("app.data_collection.requests")
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'MRData': {'xmlns': 'http://ergast.com/mrd/1.5',
                                                  'series': 'f1',
                                                  'url': 'http://ergast.com/api/f1/current/next.json',
                                                  'limit': '30',
                                                  'offset': '0',
                                                  'total': '1',
                                                  'RaceTable': {'season': '2023',
                                                                'round': '13',
                                                                'Races': [{'season': '2023',
                                                                           'round': '13',
                                                                           'url': 'https://en.wikipedia.org/wiki/2023_Dutch_Grand_Prix',
                                                                           'raceName': 'Dutch Grand Prix',
                                                                           'Circuit': {'circuitId': 'zandvoort',
                                                                                       'url': 'http://en.wikipedia.org/wiki/Circuit_Zandvoort',
                                                                                       'circuitName': 'Circuit Park Zandvoort',
                                                                                       'Location': {'lat': '52.3888',
                                                                                                    'long': '4.54092',
                                                                                                    'locality': 'Zandvoort',
                                                                                                    'country': 'Netherlands'}},
                                                                           'date': '2023-08-27',
                                                                           'time': '13:00:00Z',
                                                                           'FirstPractice': {'date': '2023-08-25', 'time': '10:30:00Z'},
                                                                           'SecondPractice': {'date': '2023-08-25', 'time': '14:00:00Z'},
                                                                           'ThirdPractice': {'date': '2023-08-26', 'time': '09:30:00Z'},
                                                                           'Qualifying': {'date': '2023-08-26', 'time': '13:00:00Z'}}]}}}

    mocker_requests.get.return_value = mock_response

    assert data_collection.get_next_race() == {'season': '2023',
                                               'round': '13',
                                               'raceName': 'Dutch Grand Prix',
                                               'date': '2023-08-27',
                                               'time': '13:00:00Z'}


import pytest
from app import data_collection


def test_get_results(mocker):
    mocker_requests = mocker.patch("app.data_collection.requests")
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'MRData': {'xmlns': 'http://ergast.com/mrd/1.5',
                                                  'series': 'f1',
                                                  'url': 'http://ergast.com/api/f1/2023/1/results.json',
                                                  'limit': '30',
                                                  'offset': '0',
                                                  'total': '20',
                                                  'RaceTable': {'season': '2023',
                                                                'round': '1',
                                                                'Races': [{'season': '2023',
                                                                           'round': '1',
                                                                           'url': 'https://en.wikipedia.org/wiki/2023_Bahrain_Grand_Prix',
                                                                           'raceName': 'Bahrain Grand Prix',
                                                                           'Circuit': {'circuitId': 'bahrain',
                                                                                       'url': 'http://en.wikipedia.org/wiki/Bahrain_International_Circuit',
                                                                                       'circuitName': 'Bahrain International Circuit',
                                                                                       'Location': {'lat': '26.0325',
                                                                                                    'long': '50.5106',
                                                                                                    'locality': 'Sakhir',
                                                                                                    'country': 'Bahrain'}},
                                                                           'date': '2023-03-05',
                                                                           'time': '15:00:00Z',
                                                                           'Results': [{'number': '1',
                                                                                        'position': '1',
                                                                                        'positionText': '1',
                                                                                        'points': '25',
                                                                                        'Driver': {'driverId': 'max_verstappen',
                                                                                                   'permanentNumber': '33',
                                                                                                   'code': 'VER',
                                                                                                   'url': 'http://en.wikipedia.org/wiki/Max_Verstappen',
                                                                                                   'givenName': 'Max',
                                                                                                   'familyName': 'Verstappen',
                                                                                                   'dateOfBirth': '1997-09-30',
                                                                                                   'nationality': 'Dutch'},
                                                                                        'Constructor': {'constructorId': 'red_bull',
                                                                                                        'url': 'http://en.wikipedia.org/wiki/Red_Bull_Racing',
                                                                                                        'name': 'Red Bull',
                                                                                                        'nationality': 'Austrian'},
                                                                                        'grid': '1',
                                                                                        'laps': '57',
                                                                                        'status': 'Finished',
                                                                                        'Time': {'millis': '5636736', 'time': '1:33:56.736'},
                                                                                        'FastestLap': {'rank': '6',
                                                                                                       'lap': '44',
                                                                                                       'Time': {'time': '1:36.236'},
                                                                                                       'AverageSpeed': {'units': 'kph', 'speed': '202.452'}}},
                                                                                       {'number': '11',
                                                                                        'position': '2',
                                                                                        'positionText': '2',
                                                                                        'points': '18',
                                                                                        'Driver': {'driverId': 'perez',
                                                                                                   'permanentNumber': '11',
                                                                                                   'code': 'PER',
                                                                                                   'url': 'http://en.wikipedia.org/wiki/Sergio_P%C3%A9rez',
                                                                                                   'givenName': 'Sergio',
                                                                                                   'familyName': 'Pérez',
                                                                                                   'dateOfBirth': '1990-01-26',
                                                                                                   'nationality': 'Mexican'},
                                                                                        'Constructor': {'constructorId': 'red_bull',
                                                                                                        'url': 'http://en.wikipedia.org/wiki/Red_Bull_Racing',
                                                                                                        'name': 'Red Bull',
                                                                                                        'nationality': 'Austrian'},
                                                                                        'grid': '2',
                                                                                        'laps': '57',
                                                                                        'status': 'Finished',
                                                                                        'Time': {'millis': '5648723', 'time': '+11.987'},
                                                                                        'FastestLap': {'rank': '7',
                                                                                                       'lap': '37',
                                                                                                       'Time': {'time': '1:36.344'},
                                                                                                       'AverageSpeed': {'units': 'kph', 'speed': '202.225'}}}]}]}}}
    mocker_requests.get.return_value = mock_response

    mock_db = mocker.patch("app.data_collection.get_db")
    mock_con = mock_db.return_value
    mock_cur = mock_con.cursor.return_value
    mock_cur.execute.return_value = None
    mock_con.commit.return_value = None

    assert 'raceName' in data_collection.get_results()
    assert 'Results' in data_collection.get_results()


def test_get_pitstops(mocker):
    mocker_requests = mocker.patch("app.data_collection.requests")
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'MRData': {'xmlns': 'http://ergast.com/mrd/1.5',
                                                 'series': 'f1',
                                                 'url': 'http://ergast.com/api/f1/2023/1/pitstops.json',
                                                 'limit': '30',
                                                 'offset': '0',
                                                 'total': '50',
                                                 'RaceTable': {'season': '2023',
                                                               'round': '1',
                                                               'Races': [{'season': '2023',
                                                                          'round': '1',
                                                                          'url': 'https://en.wikipedia.org/wiki/2023_Bahrain_Grand_Prix',
                                                                          'raceName': 'Bahrain Grand Prix',
                                                                          'Circuit': {'circuitId': 'bahrain',
                                                                                      'url': 'http://en.wikipedia.org/wiki/Bahrain_International_Circuit',
                                                                                      'circuitName': 'Bahrain International Circuit',
                                                                                      'Location': {'lat': '26.0325',
                                                                                                   'long': '50.5106',
                                                                                                   'locality': 'Sakhir',
                                                                                                   'country': 'Bahrain'}},
                                                                          'date': '2023-03-05',
                                                                          'time': '15:00:00Z',
                                                                          'PitStops': [{'driverId': 'gasly',
                                                                                        'lap': '9',
                                                                                        'stop': '1',
                                                                                        'time': '18:18:56',
                                                                                        'duration': '25.885'},
                                                                                       {'driverId': 'norris',
                                                                                        'lap': '10',
                                                                                        'stop': '1',
                                                                                        'time': '18:20:31',
                                                                                        'duration': '32.766'}]}]}}}

    mocker_requests.get.return_value = mock_response

    mock_db = mocker.patch("app.data_collection.get_db")
    mock_con = mock_db.return_value
    mock_cur = mock_con.cursor.return_value
    mock_cur.execute.return_value = None
    mock_con.commit.return_value = None

    assert 'raceName' in data_collection.get_pitstops()
    assert 'PitStops' in data_collection.get_pitstops()


def test_get_driver(mocker):
    mocker_requests = mocker.patch("app.data_collection.requests")
    mock_response = mocker.MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'MRData': {'xmlns': 'http://ergast.com/mrd/1.5',
                                                  'series': 'f1',
                                                  'url': 'http://ergast.com/api/f1/drivers/zhou.json',
                                                  'limit': '30',
                                                  'offset': '0',
                                                  'total': '1',
                                                  'DriverTable': {'driverId': 'zhou',
                                                                  'Drivers': [{'driverId': 'zhou',
                                                                               'permanentNumber': '24',
                                                                               'code': 'ZHO',
                                                                               'url': 'http://en.wikipedia.org/wiki/Zhou_Guanyu',
                                                                               'givenName': 'Guanyu',
                                                                               'familyName': 'Zhou',
                                                                               'dateOfBirth': '1999-05-30',
                                                                               'nationality': 'Chinese'}]}}}

    mocker_requests.get.return_value = mock_response

    mock_db = mocker.patch("app.data_collection.get_db")
    mock_con = mock_db.return_value
    mock_cur = mock_con.cursor.return_value
    mock_cur.execute.return_value = None
    mock_con.commit.return_value = None

    assert data_collection.get_driver() == {'driverId': 'zhou',
                                            'permanentNumber': '24',
                                            'code': 'ZHO',
                                            'url': 'http://en.wikipedia.org/wiki/Zhou_Guanyu',
                                            'givenName': 'Guanyu',
                                            'familyName': 'Zhou',
                                            'dateOfBirth': '1999-05-30',
                                            'nationality': 'Chinese'}