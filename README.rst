.. raw:: html
    <p align="center">

.. image:: https://s3.amazonaws.com/auklet/static/github_readme_django.png
    :target: https://auklet.io
    :align: center
    :width: 1000
    :alt: Auklet - Problem Solving Software for Django

.. raw:: html

    </p>

Auklet for Django
=================
.. image:: https://img.shields.io/pypi/v/auklet.svg
    :target: https://pypi.python.org/pypi/auklet
    :alt: PyPi page link -- version

.. image:: https://img.shields.io/pypi/l/auklet.svg
    :target: https://pypi.python.org/pypi/auklet
    :alt: PyPi page link -- Apache 2.0 License

.. image:: https://img.shields.io/pypi/pyversions/auklet.svg
    :target: https://pypi.python.org/pypi/auklet
    :alt: PyPi page link -- Python Versions

.. image:: https://api.codeclimate.com/v1/badges/7c2cd3bc63a70ac7fd73/maintainability
   :target: https://codeclimate.com/repos/5a54e10be3d6cb4d7d0007a8/maintainability
   :alt: Code Climate Maintainability

.. image:: https://api.codeclimate.com/v1/badges/7c2cd3bc63a70ac7fd73/test_coverage
   :target: https://codeclimate.com/repos/5a54e10be3d6cb4d7d0007a8/test_coverage
   :alt: Test Coverage


This is the official Django agent for `Auklet`_, official supports Django 1.7+ and
runs on most posix based operating systems (Debian, Ubuntu Core, Raspbian, QNX, etc).

Features
--------
- Automatic report of unhandled exceptions
- Location, system architecture, and system metrics identification for all issues


Quickstart
----------

To install the agent with *pip*::

    pip install auklet-django

To setup Auklet monitoring for you application simply include it in your
`INSTALLED_APPS`:

.. sourcecode:: python

    INSTALLED_APPS = (
        'auklet',
        ...,
    )

To set up default django middleware error handling add the auklet middleware
to the end of your middleware configs:

.. sourcecode:: python

    MIDDLEWARE = (
        ...,
        "auklet.middleware.AukletMiddleware",
    )

NOTE: If you are already using an error handling middleware which returns a response you need to disable it or add:

.. sourcecode:: python

    got_request_exception.send(sender=self, request=request)

to the line before you return a response, this ensures that the signal is
sent to the Auklet middleware

Then go and create an application at https://app.auklet.io/ to get your
config settings:

.. sourcecode:: python

    AUKLET_CONFIG = {
        "api_key": "<API_KEY>",
        "application": "<APPLICATION>",
        "organization": "<ORGANIZATION>"
    }

See the [Advanced Setup](https://github.com/aukletio/Auklet-Agent-Django/blob/master/advanced_setup.rst) section if you would like to configure Auklet using a
WSGI middleware rather than the built in Django middleware. Please note that you should only use one
or the other.

NOTE: The django application must have write permission to the directory
it is executing in.


Authorization
^^^^^^^^^^^^^
To authorize your application you need to provide both an API key and app id.
These values are available in the connection settings of your application as
well as during initial setup.


Release Tracking
^^^^^^^^^^^^^^^^
Optionally, you can track releases and identify which servers are running
what variant of code. To do this you may provide the commit hash of your
deployed code and a version string you can modify.
This release value needs to be passed into the settings variable through the
`release` key and your custom version must be passed via the `version` key.
The `release` value needs to be the commit hash that represents the
deployed version of your application. And the `version` value is a
string that you can set to whatever value you wish to define your versions.

.. sourcecode:: python

    AUKLET_CONFIG = {
        "api_key": "<API_KEY>",
        "application": "<APPLICATION>",
        "organization": "<ORGANIZATION>",
        "release": "<GIT_COMMIT_HASH>",
        "version": "1.2.3"
    }


Resources
---------
* `Auklet`_
* `Python Documentation`_
* `Issue Tracker`_

.. _Auklet: https://auklet.io
.. _hello@auklet.io: mailto:hello@auklet.io
.. _Python Documentation: https://docs.auklet.io/docs/python-integration
.. _Issue Tracker: https://github.com/aukletio/Auklet-Agent-Django/issues
