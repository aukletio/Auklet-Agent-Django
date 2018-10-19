from __future__ import absolute_import

import sys
import threading
from auklet.monitoring import AukletViewProfiler
from auklet.utils import get_monitor

from .client import get_client

try:
    # Django >= 1.10
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    # Not required for Django <= 1.9, see:
    # https://docs.djangoproject.com/en/1.10/topics/http/middleware/#upgrading-pre-django-1-10-style-middleware
    MiddlewareMixin = object


class AukletMiddleware(MiddlewareMixin):
    modules = {}

    def process_request(self, request):
        self.modules[threading.current_thread().ident] = AukletViewProfiler()
        return None

    def process_exception(self, request, exception):
        exc_type, _, traceback = sys.exc_info()
        client = get_client()
        client.produce_event(exc_type, traceback)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if get_monitor():
            profiler = self.__class__.modules.get(threading.current_thread().ident)
            return profiler.process_view(
                request, view_func, view_args, view_kwargs)
        return view_func(request, *view_args, **view_kwargs)

    def process_response(self, request, response):
        if get_monitor():
            profiler = self.__class__.modules.get(threading.current_thread().ident)
            res = profiler.create_stack(request, response)
            client = get_client()
            client.produce_stack(res, res.statobj.total_tt,
                                 res.statobj.total_calls)
        return response
