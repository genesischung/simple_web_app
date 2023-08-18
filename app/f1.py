from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort



from app.auth import login_required
from app.db import get_db

bp = Blueprint('f1', __name__)


@bp.route('/')
def index():
    db = get_db()
    return render_template('index.html', text="Hello World!")


@bp.route("/message", methods=["POST"])
@login_required
def echo_input():
    input_text = request.form.get("user_input", "")
    return render_template('index.html', text=input_text)

@bp.route("/health")
def health_check():
    return render_template('health_check.html'), 200

