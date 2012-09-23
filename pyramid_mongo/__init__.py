from pyramid.exceptions import ConfigurationError
from pyramid.settings import asbool
from pymongo import Connection

URI = 'mongo.uri'
MONGOENGINE = 'mongo.mongoengine'
USERNAME = 'mongo.username'
PASSWORD = 'mongo.password'
DBNAME = 'mongo.db'
GREENLETS = 'mongo.use_greenlets'

def get_connection(config, conn_cls=None):
    """get_connection creates a connection to one or more mongodb server. 
       It take as argument a config that should have the "mongo.uri" set 
       to a string separated by new lines for each server. 

       The uri must be of a form acceptable by mongodb. 
       http://www.mongodb.org/display/DOCS/Connections
    """

    if conn_cls is None:
        conn_cls = Connection
        
    registry = config.registry

    uri = registry.settings.get(URI)
    greenlets = registry.settings.get(GREENLETS)

    if uri is None:
        raise ConfigurationError('There is no configured "mongo.uri"')

    # Spliting configs to get more than one uri
    if not isinstance(uri, list):
        uri = uri.splitlines()

    kargs = {
        'use_greenlets':  asbool(greenlets)
    }

    return conn_cls(uri, **kargs)

def get_db(request, name=None):
    """get_db opens a handle for a database using a connection.
       the primary database is defined by the setting "mongo.db".

       If passed "name" as argument, get_db will return a different 
       database than the one set in the settings. 

       If you have mongo.username and mongo.password set, it will try
       to connecto to the database.

       Here is an example
       
       mongo.uri = 127.0.0.1
                   localhost
       mongo.db = blog

       mongo.username.blog = theuser
       mongo.password.blog = thepassword

       mongo.username.blog2 = theuser2
       mongo.password.blog2 = thepassword2
    """

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
            raise ConfigurationError(
                'There is no database connection available')

        db = conn[dbname]

        mongodbs[dbname] = db
        request._mongo_dbs = mongodbs

    username = registry.settings.get(USERNAME + '.' + dbname)
    password = registry.settings.get(PASSWORD + '.' + dbname)

    if not username is None and not password is None:
        db.authenticate(username, password)

    def end_request(request):
        db.logout()
        db.connection.end_request() 

    request.add_finished_callback(end_request)

    return db

def setup_mongoengine(config):
    # Simple setup mongoengine 
    from mongoengine import connection
    print "Loading mongoengine"
    registry = config.registry

    connection._connections['default'] = config.registry._mongo_conn
    connection._connection_settings['default'] = {
        'name': registry.settings.get(DBNAME),
        'username': registry.settings.get(USERNAME),
        'password': registry.settings.get(PASSWORD),
    }

def includeme(config, get_connection=get_connection):
    # get_connection passed for testing
    """
        Get a mongodb instance from the URI in the config file
        mongodb.uri
    """
    config.registry._mongo_conn = get_connection(config)
    
    mongoengine = asbool(config.registry.settings.get(MONGOENGINE))
    if mongoengine and config.registry._mongo_conn:
        setup_mongoengine(config)
