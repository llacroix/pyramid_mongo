About
=====

pyramid_mongo is intended for use with the default python driver for mongodb

How to use
==========

You have to define at least 3 things in your settings

    mongo.uri = uri of your database (mongodb://localhost/)
    mondo.db = name of the database you want to use

Those two are optional

    mongo.username.dbname = username for authentication to dbname
    mongo.password.dbname = password used for authentication to dbname

Mongodb uri format
==================

The format of the mongodb uri is the one that use mongodb. You can pass
multiple uris to mongo.uri. They must be separated by newlines and they 
must be uniques. MongoDb will not accept two identical uri. But it will
accept uris reffering to the same host and same server if hostnames are 
not identical.

    mongo.uri = localhost
                127.0.0.1

Is something valid and will work. Connection will open 2 connections on the 
default port. 
