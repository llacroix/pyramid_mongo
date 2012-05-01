import unittest                                                                                                                                        
from pyramid import testing
from unittest import TestCase
from pyramid.exceptions import ConfigurationError
from pymongo.errors import AutoReconnect

class Test_get_connection(TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def _callFUT(self, config):
        from pyramid_mongo import get_connection
        return get_connection(config)

    def test_without_include(self):
         self.assertRaises(ConfigurationError, self._callFUT, self.config)

    def test_without_uri(self):
        self.assertRaises(ConfigurationError, self._callFUT, self.config)
        
    def test_with_invalid_uri(self):
        from pymongo.errors import ConfigurationError
        self.config.registry.settings['mongo.uri'] = "1"
        self.assertRaises(AutoReconnect, self._callFUT, self.config)
        self.config.registry.settings['mongo.uri'] = ""
        self.assertRaises(ConfigurationError, self._callFUT, self.config)

    def test_with_valid_uri(self):
        self.config.registry.settings['mongo.uri'] = "mongodb://localhost/"
        conn = self._callFUT(self.config)
        self.assertEqual(type(conn).__name__, 'Connection')

class Test_get_db(TestCase):

    def _callFUT(self, request, dbname=None):
        from pyramid_mongo import get_db
        return get_db(request, name=dbname)

    def _makeRequest(self):
        request = testing.DummyRequest()
        # other things
        request._mongo_dbs = dict()
        request.registry.settings = dict()
        return request

    def test_without_name(self):
        request = self._makeRequest()
        #del request.registry._mongo_conn
        self.assertRaises(ConfigurationError, self._callFUT, request)
    
    def test_without_conn_with_name(self):
        request = self._makeRequest()

        if hasattr(request.registry, '_mongo_conn'):
            delattr(request.registry, '_mongo_conn')

        self.assertRaises(ConfigurationError, self._callFUT, request, 'fun')

    def test_with_existing_db(self):
        request = self._makeRequest()
        request._mongo_dbs = dict(test=DummyDB())
        db = self._callFUT(request, 'test')
        self.assertEqual(db, request._mongo_dbs['test'])

    def test_with_new_db(self):
        request = self._makeRequest()
        request.registry._mongo_conn = DummyConnection()
        db = self._callFUT(request, 'test')
        db2 = request._mongo_dbs['test']
        self.assertEqual(db, db2)

    def test_auth(self):
        request = self._makeRequest()
        request.registry._mongo_conn = DummyConnection()
        
        request.registry.settings['mongo.username'] = 'fun'
        request.registry.settings['mongo.password'] = 'fusdn'
        db = self._callFUT(request, 'test')
        self.assertEqual(db.authenticated, False)

        request.registry.settings['mongo.username'] = 'admin'
        request.registry.settings['mongo.password'] = 'fun'
        db = self._callFUT(request, 'test')
        self.assertEqual(db.authenticated, True)


class Test_includeme(TestCase):
    def _callFUT(self, config):
        from pyramid_mongo import includeme
        return includeme(config)

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_with_normal_config(self):

        if hasattr(self.config.registry, '_mongo_conn'):
            delattr(self.config.registry, '_mongo_conn')

        self.config.registry.settings['mongo.uri'] = 'localhost'
        self.config.registry.settings['mongo.db'] = 'blog'
        self._callFUT(self.config)
        self.assertEqual(hasattr(self.config.registry, '_mongo_conn'), True)

class DummyDB(object):

    def authenticate(self, username, password):
        self.authenticated = username == 'admin' and password == 'fun'
        return self.authenticated

class DummyConnection(object):
    def __getitem__(self, name):
        return DummyDB()
