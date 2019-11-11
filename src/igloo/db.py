import os
import sqlite3


def _connection(request):
    def close_db(request):
        db = request.registry.pop('db', None)

        if db is not None:
            db.close()

    request.add_finished_callback(close_db)

    return get_db(request.registry)


def connection(event):
    event.request.set_property(_connection, 'db', reify=True)


def get_db(registry):
    db = registry.settings.get('DATABASE')

    if db:
        registry.db = sqlite3.connect(
            db,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        registry.db.row_factory = sqlite3.Row

    return registry.db


# TODO: create cli command to init the db.
def init_db(config):
    db = get_db(config.registry)

    cwd = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(cwd, 'schema.sql'), 'rb') as f:
        db.executescript(f.read().decode('utf8'))

    print('Initialized the database.')
