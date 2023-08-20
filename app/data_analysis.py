from datetime import datetime
from dateutil import parser
from app.db_postgres import get_db
import app.data_collection as data_collection

from flask import Blueprint, render_template

from psycopg2.extras import RealDictCursor

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
        next_race = float(response[0])
        countdown = next_race - datetime.now().timestamp()
    else:
        countdown = -99999

    # if current race has not ended
    # return the current countdown
    if countdown > -21600.0:
        return render_template('countdown.html', time=next_race)

    # if countdown not in db
    # or is already finished
    # recall the api for the next race
    else:
        data = data_collection.get_next_race()
        # get the date and time from input
        time = parser.parse(data['date'] + ' ' + data['time'])

        # calculate time till next race in seconds
        next_race = time.timestamp()

        # add the countdown time to db
        query = "INSERT INTO info (name, data) VALUES ('nextrace', '{}')".format(
            str(next_race))
        conn = get_db()
        with conn.cursor() as curs:
            curs.execute(query)
            conn.commit()

        return render_template('countdown.html', time=next_race)


@bp.route("/getdriver/<driver_id>")
def lookup_driver(driver_id):
    """
    look up a driver in DB
    if driver not in DB,
    call data_collection to get info
    :param driver_id:
    :return: driver's first and last name
    """
    conn = get_db()
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute("SELECT * FROM drivers WHERE driverID = %s", (driver_id,))
        driver = curs.fetchone()
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

