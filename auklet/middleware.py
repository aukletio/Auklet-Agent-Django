from __future__ import absolute_import

import sys
from contextlib import contextmanager

from .client import get_client

try:
    # Django >= 1.10
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    # Not required for Django <= 1.9, see:
    # https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-pre-django-1-10-style-middleware
    MiddlewareMixin = object


def report_exception():
    exc_type, _, traceback = sys.exc_info()
    print("HANDLE EXCEPTION: ", exc_type, traceback)
    client = get_client()
    client.produce_event(exc_type, traceback)


@contextmanager
def handle_exception():
    try:
        yield
    except (StopIteration, GeneratorExit):
        raise
    except SystemExit as e:
        if e.code != 0:
            report_exception()
        raise
    except Exception:
        report_exception()
        raise


class ClosingIterator(object):
    """
    An iterator that is implements a ``close`` method as-per
    WSGI recommendation.
    """

    def __init__(self, iterable, environ):
        self.environ = environ
        self._close = getattr(iterable, 'close', None)
        self.iterable = iter(iterable)
        self.closed = False

    def __iter__(self):
        return self

    def __next__(self):
        try:
            with handle_exception():
                return next(self.iterable)
        except StopIteration:
            # We auto close here if we reach the end because some WSGI
            # middleware does not really like to close things.  To avoid
            # massive leaks we just close automatically at the end of
            # iteration.
            self.close()
            raise

    def close(self):
        if self.closed:
            return
        try:
            if self._close is not None:
                with handle_exception():
                    self._close()
        finally:
            self.closed = True


class AukletMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        report_exception()


class WSGIAukletMiddleware(object):
    """
    A WSGI middleware which will attempt to capture any
    uncaught exceptions and send them to Auklet.
    """

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        with handle_exception():
            iterable = self.application(environ, start_response)
        return ClosingIterator(iterable, environ)
