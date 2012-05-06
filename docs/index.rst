pyramid_mongo
================

Overview
--------

A package which provides integration between the Pyramid web application
server and the `MongoDB` object database.


Installation
------------

Install using setuptools, e.g. (within a virtualenv)::

  $ easy_install pyramid_mongo

  $ pip install pyramid_mongo

Setup
-----

Once ``pyramid_mongo`` is installed, you must use the ``config.include``
mechanism to include it into your Pyramid project's configuration.  In your
Pyramid project's ``__init__.py``:

.. code-block:: python
   :linenos:

   config = Configurator(.....)
   config.include('pyramid_mongo')

Alternately you can use the ``pyramid.includes`` configuration value in your
``.ini`` file:

.. code-block:: ini
   :linenos:

   [app:myapp]
   pyramid.includes = pyramid_mongo

Using
-----

For :mod:`pyramid_mongo` to work properly, you must add at least two
setting to your of your Pyramid's ``.ini`` file configuration (or to the
``settings`` dictionary if you're not using ini configuration):
``mongo.uri`` and ``mongo.db``  For example:

.. code-block:: ini

   [app:myapp]
   ...
   mongo.uri = mongodb://localhost/
   mongo.db = mongo_pyramid
   ...

The ``mongo.uri`` parameter is a URL which describes a mongodb connection uri.

Once you've both included the ``pyramid_mongo`` into your configuration
via ``config.include('pyramid_mongo')`` and you've added a
``mongo.uri`` setting to your configuration, you can then use the
:func:`pyramid_mongo.get_db` API in your Pyramid application, most
commonly in a Pyramid *root factory*:

.. code-block:: python
   :linenos:

    from pyramid_mongo import get_db

    class MyModel(object):
        __parent__ = __name__ = None

        def to_dict(self):
            return dict()

    def root_factory(request):
        db = get_db(request)

        root = db.root.find_one()
        if not root:
            root = MyModel()
            db.root.insert(root.to_dict())

        return root

The :func:`pyramid_mongo.get_db` API returns a MongoDB database to
the main database you've specified via ``mongo.db`` in your
configuration.

When the request is finalized, the database you've opened via
``get_db`` will be freeed to the next thread.

Examples
++++++++

Some examples

More Information
----------------

.. toctree::
   :maxdepth: 1

   api.rst
   tutorials/index.rst
   glossary.rst


Reporting Bugs / Development Versions
-------------------------------------

Visit http://github.com/llacroix/pyramid_mongo to download development or
tagged versions.

Visit http://github.com/llacroix/pyramid_mongo/issues to report bugs.

Indices and tables
------------------

* :ref:`glossary`
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
