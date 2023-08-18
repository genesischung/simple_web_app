import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.jinja_env.auto_reload = True
    app.config["DEBUG"] = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["EXPLAIN_TEMPLATE_LOADING"] = True
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'web.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # connect db
    from . import db
    db.init_app(app)

    # blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    # f1 site
    from . import f1
    app.register_blueprint(f1.bp)
    app.add_url_rule('/', endpoint='index')


# a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

