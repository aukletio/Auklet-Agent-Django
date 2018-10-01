<p align="center"><a href="https://auklet.io"><img src="https://s3.amazonaws.com/auklet/static/github_readme_django.png" alt="Auklet - Problem Solving Software for Django"></a></p>

# Auklet for Django
<a href="https://pypi.python.org/pypi/django-auklet" alt="PyPi page link -- version"><img src="https://img.shields.io/pypi/v/django-auklet.svg" /></a>
<a href="https://pypi.python.org/pypi/django-auklet" alt="PyPi page link -- Apache 2.0 License"><img src="https://img.shields.io/pypi/l/django-auklet.svg" /></a>
<a href="https://pypi.python.org/pypi/django-auklet" alt="Python Versions"><img src="https://img.shields.io/pypi/pyversions/django-auklet.svg" /></a>

This is the official Django agent for [Auklet][brochure_site]. It officially supports Django 1.7+, and runs on most POSIX-based operating systems (Debian, Ubuntu Core, Raspbian, QNX, etc).

## Features
- Automatic report of unhandled exceptions
- Location, system architecture, and system metrics identification for all issues

## Quickstart
To install the agent with _pip_:

```bash
pip install django-auklet
```

To setup Auklet monitoring for you application simply include it in your `INSTALLED_APPS`:

```python
INSTALLED_APPS = (
    'auklet',
    ...,
)
```

Then go and create an application at https://app.auklet.io/ to get your
config settings:

```python
AUKLET_CONFIG = {
    "api_key": "<API_KEY>",
    "application": "<APPLICATION>",
    "organization": "<ORGANIZATION>"
}
```

### Authorization
To authorize your application you need to provide both an API key and app ID. These values are available in the connection settings of your application as well as during initial setup.


### Release Tracking
Optionally, you can track releases and identify which servers are running what variant of code. To do this you may provide the commit hash of your deployed code and a version string you can modify. This release value needs to be passed into the settings variable through the `release` key and your custom version must be passed via the `version` key. The `release` value needs to be the commit hash that represents the deployed version of your application. And the `version` value is a string that you can set to whatever value you wish to define your versions.

```python
AUKLET_CONFIG = {
    "api_key": "<API_KEY>",
    "application": "<APPLICATION>",
    "organization": "<ORGANIZATION>",
    "release": "<GIT_COMMIT_HASH>",
    "version": "1.2.3"
}
```

### Middleware Error Handling
To set up default Django middleware error handling, add the Auklet middleware to the end of your middleware configs:

```python
MIDDLEWARE = (
    ...,
    "auklet.middleware.AukletMiddleware",
)
```

If you are already using an error handling middleware which returns a response, you need to disable it or do the following before you return a response; this ensures that the signal is sent to the Auklet middleware.

```python
got_request_exception.send(sender=self, request=request)
```

If you wish to set up Auklet using a WSGI middleware instead of the default Django middleware, you can do so as shown below. Please note that you should only use WSGI or Django middleware, not both.

```python
import os
from django.core.wsgi import get_wsgi_application
from django.conf import settings
from auklet.middleware import WSGIAukletMiddleware

application = get_wsgi_application()
application = WSGIAukletMiddleware(application)
```

## Resources
- [Auklet][brochure_site]
- [Python Documentation](https://docs.auklet.io/docs/python-integration)
- [Issue Tracker](https://github.com/aukletio/Auklet-Agent-Django/issues)

[brochure_site]: https://auklet.io
