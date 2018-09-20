.. raw:: html
    <p align="center">

.. image:: https://s3.amazonaws.com/auklet/static/auklet_python.png
    :target: https://auklet.io
    :align: center
    :width: 1000
    :alt: Auklet - Problem Solving Software for Python

.. raw:: html

    </p>

Auklet for Python
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


This is the official Python agent for `Auklet`_, official supports 2.7.9+ and 3.4-3.7, and
runs on most posix based operating systems (Debian, Ubuntu Core, Raspbian, QNX, etc).

Features
--------
- Automatic report of unhandled exceptions
- Automatic Function performance issue reporting
- Location, system architecture, and system metrics identification for all issues
- Ability to define data usage restriction


Compliance
----------
Auklet is an edge first application performance monitor and as such
after 1.0 releases of our packages we maintain the following compliance levels:

- Automotive Safety Integrity Level B (ASIL B)

If there are additional compliances that your industry requires please contact
the team at `hello@auklet.io`_.


Quickstart
----------

To install the agent with *pip*::

    pip install auklet-django

To setup Auklet monitoring for you application simply include it in your
`INSTALLED_APPS`:

.. sourcecode:: python

    INSTALLED_APPS = (
    ...,
    'auklet',
    ...,
)

Then go and create an application at https://app.auklet.io/ to get your
config settings:

.. sourcecode:: python

    AUKLET_CONFIG = {
        "api_key": "<API_KEY>",
        "app_id": "<APP_ID>",
        "release": "<CURRENT_COMMIT_HASH"
    }

To set up default django middleware error handling add the auklet middleware
to the end of your middleware configs:

.. sourcecode:: python

    MIDDLEWARE = (
        ...,
        "auklet.middleware.AukletMiddleware",
    )

Alternatively to set up the wsgi middleware modify your `wsgi.py`:

.. sourcecode:: python

    import os
    from django.core.wsgi import get_wsgi_application
    from django.conf import settings
    from auklet.middleware import WSGIAukletMiddleware

    application = get_wsgi_application()
    application = WSGIAukletMiddleware(application)


Authorization
^^^^^^^^^^^^^
To authorize your application you need to provide both an API key and app id.
These values are available in the connection settings of your application as
well as during initial setup.


Release Tracking
^^^^^^^^^^^^^^^^
To track releases and identify which devices are running what version of code
we currently require that you provide the commit hash of your deployed code.
This value needs to be passed into the constructor through `release`.
The value needs to be the commit hash that represents the
deployed version of your application. There are a couple ways for which to set
this based upon the style of deployment of your application.


Resources
---------
* `Auklet`_
* `Python Documentation`_
* `Issue Tracker`_

.. _Auklet: https://auklet.io
.. _hello@auklet.io: mailto:hello@auklet.io
.. _ESG-USA: https://github.com/ESG-USA
.. _ESG Organization: https://github.com/ESG-USA
.. _Python Documentation: https://docs.auklet.io/docs/python-integration
.. _Issue Tracker: https://github.com/aukletio/Auklet-Agent-Python/issues
