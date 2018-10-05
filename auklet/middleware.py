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
