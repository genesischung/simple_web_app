import requests
from app.db_postgres import get_db
from psycopg2.extras import Json

def get_next_race():
    """
    Retrieve information about the next Formula 1 race
    :return: dict with season, round, race name, date, time
    """
    url = "https://ergast.com/api/f1/current/next.json"
    response = requests.get(url).json()
    try:
        race = response['MRData']['RaceTable']['Races'][0]
        # return a subset of wanted information
        wanted_keys = ['season', 'round', 'raceName', 'date', 'time']
        data = dict((k, race[k]) for k in wanted_keys if k in race)
        return data
    except:
        return None


def get_results(season=2023, rounds=1):
    """
    Get the race results of a Formula 1 race
    :param season: the year of the season
    :param rounds:
    :return: dict with race name and array of results in json
    """
    url = "http://ergast.com/api/f1/{}/{}/results.json".format(season, rounds)
    response = requests.get(url).json()
    try:
        race = response['MRData']['RaceTable']['Races'][0]
        wanted_keys = ['raceName', 'Results']
        data = dict((k, race[k]) for k in wanted_keys if k in race)

        # write to db
        conn = get_db()
        with conn.cursor() as curs:
            curs.execute("INSERT INTO results (season, round, data) VALUES (%s, %s, %s);",
                            (season, rounds, Json(data)))
        conn.commit()
        # return data to indicate success
        #print("Get results season {} round {}", format(season, rounds))
        return data
    except:
        return None


def get_pitstops(season=2023, rounds=1):
    """
    :param season:
    :param rounds:
    :return:
    """
    url = "http://ergast.com/api/f1/{}/{}/pitstops.json".format(season, rounds)
    response = requests.get(url).json()
    try:
        race = response['MRData']['RaceTable']['Races'][0]
        wanted_keys = ['raceName', 'PitStops']
        data = dict((k, race[k]) for k in wanted_keys if k in race)

        # write to db
        conn = get_db()
        with conn.cursor() as curs:
            curs.execute("INSERT INTO pitstops (season, round, data) VALUES (%s, %s, %s);",
                            (season, rounds, Json(data)))
        conn.commit()
        # return data to indicate success
        #print("Get pitstops season {}, round {}".format(season, rounds))
        return data
    except:
        return None


def get_driver(driver_id='zhou'):
    """
    :param driverID:
    :return:
    """
    url = "http://ergast.com/api/f1/drivers/{}.json".format(driver_id)
    response = requests.get(url).json()
    try:
        driver = response['MRData']['DriverTable']['Drivers'][0]
        fname = driver['givenName']
        lname = driver['familyName']

        # write to db
        conn = get_db()
        with conn.cursor() as curs:
            curs.execute("INSERT INTO drivers (driverID, givenName, familyName) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
                            (driver_id, fname, lname))
        conn.commit()
        # return data to indicate success
        #print("Get driver {}".format(driver_id))
        return driver
    except:
        return None

