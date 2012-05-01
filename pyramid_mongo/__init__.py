from pyramid.exceptions import ConfigurationError
from pymongo import Connection

URI = 'mongo.uri'
USERNAME = 'mongo.username'
PASSWORD = 'mongo.password'
DBNAME = 'mongo.db'

def get_connection(config):
    registry = config.registry

    uri = registry.settings.get(URI)

    if uri is None:
        raise ConfigurationError('There is no configured "mongo.uri"')

    return Connection(uri)

def get_db(request, name=None):
    dbname = name
    registry = request.registry

    if name is None:
        dbname = registry.settings.get(DBNAME)

    if dbname is None:
        raise ConfigurationError('There is no defined database name')

    mongodbs = getattr(request, '_mongo_dbs', dict())

    db = mongodbs.get(dbname)

    if db is None:
        conn = getattr(registry, '_mongo_conn', None)

        if conn is None:
            raise ConfigurationError('There is no database connection available')

        db = conn[dbname]

        mongodbs[dbname] = db
        request._mongo_dbs = mongodbs

    username = registry.settings.get(USERNAME)
    password = registry.settings.get(PASSWORD)

    if not username is None and not password is None:
        db.authenticate(username, password)

    def end_request(request):
        db.logout()
        db.connection.end_request() 

    request.add_finished_callback(end_request)

    return db


def includeme(config):
    """
        Get a mongodb instance from the URI in the config file
        mongodb.uri
    """
    config.registry._mongo_conn = get_connection(config)
