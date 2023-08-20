from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)

from prometheus_flask_exporter import PrometheusMetrics
from app.auth import login_required
from app.db_postgres import init_db

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
    input_text = request.form.get("user_input", "")
    return render_template('index.html', text=input_text)

@bp.route("/health")
@by_path_counter
def health_check():
    return render_template('health_check.html'), 200


@bp.route("/init_db", methods=["POST"])
def init():
    init_db()
    return render_template('index.html', text="Database initialized")



