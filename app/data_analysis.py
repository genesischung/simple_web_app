from datetime import datetime
from dateutil import parser
from app.db_postgres import get_db
import app.data_collection as data_collection

from flask import Blueprint, render_template

from psycopg2.extras import RealDictCursor, Json

from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(None, path=None)
metrics.info('data_analysis_app_info', 'Data Analysis app info', version='1.0.3')


bp = Blueprint('data_analysis', __name__, url_prefix='/analysis')
@bp.route('/countdown')
def time_until_next_race():
    """
    if race in db is completed
    call data_collection for new next race
    :return: timestamp of next race from db
    """

    # check if info is in DB
    conn = get_db()
    with conn.cursor() as curs:
        curs.execute("SELECT data from info where name = (%s) ORDER BY id DESC", ("nextrace",))
        response = curs.fetchone()

    if response is not None:
        # get countdown in seconds from db
        next_race = response[0]
        countdown = next_race['time'] - datetime.now().timestamp()
    else:
        countdown = -99999

    # if current race has not ended
    # return the current countdown
    if countdown > -21600.0:
        return render_template('countdown.html', data=next_race)

    # if countdown not in db
    # or is already finished
    # recall the api for the next race
    else:
        data = data_collection.get_next_race()
        # get the date and time from input
        time = parser.parse(data['date'] + ' ' + data['time'])

        # calculate time till next race in seconds
        wanted_keys = ['season', 'round']
        next_race = dict((k, data[k]) for k in wanted_keys if k in data)
        next_race['time'] = time.timestamp()
        next_race['racename'] = data['raceName']

        # add the countdown time to db
        query = "INSERT INTO info (name, data) VALUES ('nextrace', {})".format(
            Json(next_race))
        conn = get_db()
        with conn.cursor() as curs:
            curs.execute(query)
            conn.commit()

        return render_template('countdown.html', data=next_race)


@bp.route("/getdriver/<driver_id>")
def lookup_driver(driver_id):
    """
    look up a driver in DB
    if driver not in DB,
    call data_collection to get info
    :param driver_id:
    :return: driver's first and last name
    """
    try:
        conn = get_db()
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute("SELECT * FROM drivers WHERE driverID = %s", (driver_id,))
            driver = curs.fetchone()
    except:
        return render_template('driver.html', driver_id=driver_id,
                                fname='DB connection failed')
    if driver is None:
        driver = data_collection.get_driver(driver_id)
        fname = driver['givenName']
        lname = driver['familyName']
    else:
        fname = driver['givenname']
        lname = driver['familyname']
    return render_template('driver.html',
                            driver_id=driver_id,
                            fname=fname,
                            lname=lname)


@bp.route('/get_new_driver/<driver_id>')
def get_new_driver(driver_id):
    """
    :param driver_id:
    :return: the full name of a driver not in DB
    """
    driver = data_collection.get_driver(driver_id)
    # if lookup failed, return the driver_id
    if driver is None:
        print("get new driver {} failed".format(driver_id))
        return driver_id
    fname = driver['givenName']
    lname = driver['familyName']
    return fname + ' ' + lname

@bp.route('/alldrivers')
def get_all_drivers():
    """
    :return: a dict containing all driverID to driver names
    """
    try:
        conn = get_db()
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute("SELECT * FROM drivers;")
            drivers = curs.fetchall()
    except:
        # when DB connection is down
        # return a offline dict from 2023 season
        return {'albon': 'Alexander Albon',
                'alonso': 'Fernando Alonso',
                'bottas': 'Valtteri Bottas',
                'de_vries': 'Nyck de Vries',
                'gasly': 'Pierre Gasly',
                'hamilton': 'Lewis Hamilton',
                'hulkenberg': 'Nico Hülkenberg',
                'kevin_magnussen': 'Kevin Magnussen',
                'leclerc': 'Charles Leclerc',
                'max_verstappen': 'Max Verstappen',
                'norris': 'Lando Norris',
                'ocon': 'Esteban Ocon',
                'perez': 'Sergio Pérez',
                'piastri': 'Oscar Piastri',
                'ricciardo': 'Daniel Ricciardo',
                'russell': 'George Russell',
                'sainz': 'Carlos Sainz',
                'sargeant': 'Logan Sargeant',
                'stroll': 'Lance Stroll',
                'tsunoda': 'Yuki Tsunoda',
                'zhou': 'Guanyu Zhou'}

    if drivers is None:
        return None

    # create a dict to map driverid to driver full name
    mapper = dict()
    for d in drivers:
        mapper[d['driverid']] = "{} {}".format(d['givenname'], d['familyname'])

    return mapper



def to_seconds(timestr):
    """
    helper function to convert time string to seconds
    :param timestr:
    :return:
    """
    seconds = 0
    for part in timestr.split(':'):
        seconds = seconds*60 + float(part)
    return seconds

@bp.route("/pitstops/<season>/<rounds>")
def pitstop(season, rounds):
    """
    Compare the pitstops in a race
    """
    try:
        conn = get_db()
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute("SELECT * FROM pitstops WHERE season = %s AND round = %s;", (season, rounds,))
            data = curs.fetchone()
    except:
        return render_template('pitstops.html', race_name="Database Down... Please Try Again")
    if data is None:
        data = data_collection.get_pitstops(season, rounds)
    else:
        data = data['data']

    race_name = str(season) + ' ' + data['raceName']

    # sort the list based on pitstop time
    pitstop_data = sorted(data['PitStops'], key=lambda d:to_seconds(d['duration']))
    mapper = get_all_drivers()

    # append driver name to list
    for p in pitstop_data:
        if p['driverId'] in mapper:
            p['driverName'] = mapper[p['driverId']]
        else:
            print("get new driver", p['driverId'], flush=True)
            p['driverName'] = get_new_driver(p['driverId'])

    return render_template('pitstops.html', race_name=race_name, pitstop_data=pitstop_data)


