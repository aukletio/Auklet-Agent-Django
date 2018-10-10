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
        client = get_client()
        client.produce_event(exc_type, traceback)

    def process_view(self, request, view_func, callback_args, callback_kwargs):
        client = get_client(monitor=True)
        client.monitoring.start()
        response = view_func(request, *callback_args, **callback_kwargs)
        client.monitoring.stop()
        client.produce_stack(client.monitoring.get_stack())
        return response
