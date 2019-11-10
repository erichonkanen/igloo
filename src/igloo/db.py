import os
import sqlite3


def _connection(request):
    def close_db(request):
        db = request.registry.pop('db', None)

        if db is not None:
            db.close()

    request.add_finished_callback(close_db)

    return get_db(request)


def connection(event):
    event.request.set_property(_connection, 'db', reify=True)


def get_db(request):
    db = request.registry.settings.get('DATABASE')

    if db:
        request.registry.db = sqlite3.connect(
            db,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        request.registry.db.row_factory = sqlite3.Row

    return request.registry.db


# TODO: create cli command to init the db.
def init_app(config):
    db = get_db(config)

    cwd = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(cwd, 'schema.sql'), 'rb') as f:
        db.executescript(f.read().decode('utf8'))

    print('Initialized the database.')
