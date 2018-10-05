from __future__ import absolute_import

import sys

from .client import get_client

try:
    # Django >= 1.10
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    # Not required for Django <= 1.9, see:
    # https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-pre-django-1-10-style-middleware
    MiddlewareMixin = object


class AukletMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        exc_type, _, traceback = sys.exc_info()
        print("IN PROCESS EXCEPTION: ", exc_type, traceback)
        client = get_client()
        client.produce_event(exc_type, traceback)


class WSGIAukletMiddleware(object):
    """
    A WSGI middleware which will attempt to capture any
    uncaught exceptions and send them to Auklet.
    """

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        app = None
        try:
            app = self.application(environ, start_response)
            for item in app:
                yield item
        # Catch any exception
        except:
            print("IN EXCEPTION OF WSGI MIDDLEWARE")
            self.handle_exception(environ)
            raise

        if hasattr(app, 'close'):
            app.close()

    def handle_exception(self, environ=None):
        exc_type, _, traceback = sys.exc_info()
        print("HANDLE EXCEPTION: ", exc_type, traceback)
        client = get_client()
        client.produce_event(exc_type, traceback)
