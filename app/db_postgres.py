import click
from flask import current_app, g
import psycopg2


def get_db():
    if 'db' not in g:
        try:
            g.db = psycopg2.connect(current_app.config['DATABASE_URL'],
                                    keepalives=1,
                                    keepalives_idle=30,
                                    keepalives_interval=10,
                                    keepalives_count=5)
        except:
            print("Unable to connect to Database")

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with db.cursor() as curs:
        with current_app.open_resource('schema.sql') as f:
            queries = f.read().decode('utf8')
            curs.execute(queries)
            '''
            for q in queries:
                print("query:" + q, flush=True)
                curs.execute(q)
            '''

    db.commit()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
