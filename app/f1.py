import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)

from prometheus_flask_exporter import PrometheusMetrics
from app.auth import login_required
from app.db_postgres import init_db, get_db

from psycopg2.extras import RealDictCursor
import pika

bp = Blueprint('f1', __name__)

# Prometheus instance
# will be bind to app  in create_app()
# in __init__.py
metrics = PrometheusMetrics(None, group_by='endpoint', path='/metrics')
metrics.info('f1_app_info', 'F1 web app info', version='1.0.3')

by_path_counter = metrics.counter(
    'by_path_counter', 'Request count by request paths',
    labels={'path': lambda: request.path}
)


@bp.route('/')
@by_path_counter
def index():
    return render_template('index.html', text="Hello")


@bp.route("/message", methods=["POST"])
@login_required
@by_path_counter
def echo_input():
    # get the input message
    input_text = request.form.get("user_input", "")
    # get the logged in user name
    try:
        username = g.user['username']
    except:
        username = "Guest"

    # send the message to AMQP server
    url = os.environ.get("CLOUDAMQP_URL")
    if url is None:
        print("No CLOUDAMQP_URL env variable")
        return redirect('/messageboard')

    try:
        connection = pika.BlockingConnection(pika.URLParameters(url))
    except pika.exceptions.AMQPConnectionError as err:
        print("failed to connect AMQP")

    query = "INSERT INTO messages (username, message) VALUES ('{}', '{}');".format(
        username, input_text
    )

    try:
        channel = connection.channel()
        channel.queue_declare(queue='message_queue', durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='message_queue',
            body=query,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        connection.close()
    except:
        print("Failed to send the message")

    return redirect('/messageboard')


@bp.route("/health")
@by_path_counter
def health_check():
    return render_template('health_check.html'), 200


@bp.route("/init_db")
def init():
    # init_db()
    return render_template('index.html', text="Database initialized")


@bp.route("/messageboard")
def messageboard():
    conn = get_db()
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute("SELECT * from messages;")
        response = curs.fetchall()
    return render_template('messageboard.html', messages=response)


@bp.route("/pitstops")
def show_pitstop():
    return render_template('pitstops.html')
