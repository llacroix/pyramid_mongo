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
        from pyramid_zodbconn import get_connection
        return get_connection(config)

    def test_without_include(self):
         self.assertRaises(ConfigurationError, self._callFUT, self.config)

    def test_without_uri(self):
        self.assertRaises(ConfigurationError, self._callFUT, self.config)
        
    def test_with_invalid_uri(self):
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
        from pyramid_zodbconn import get_db
        return get_db(request, dbname=dbname)

    def _makeRequest(self):
        request = testing.DummyRequest()
        # other things
        return request

class Test_includeme(TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()
