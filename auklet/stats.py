from __future__ import absolute_import, division, unicode_literals

import six
import inspect
from uuid import uuid1
from pstats import Stats

try:
    import psutil
except ImportError:  # pragma: no cover
    # Some platforms that applications could be running on require specific
    # installation of psutil which we cannot configure currently
    psutil = None

__all__ = ['Function', 'AukletProfilerStats', 'Event', 'SystemMetrics',
           'FilenameCaches']


class Event(object):
    __slots__ = ['trace', 'exc_type', 'line_num']

    def __init__(self, exc_type, tb, tree):
        self.exc_type = exc_type.__name__
        self.line_num = tb.tb_lineno
        self._build_traceback(tb, tree)

    def __iter__(self):
        yield "stackTrace", self.trace
        yield "excType", self.exc_type

    def _convert_locals_to_string(self, local_vars):
        for key in local_vars:
            if type(local_vars[key]) != str and type(local_vars[key]) != int:
                local_vars[key] = str(local_vars[key])
        return local_vars

    def _build_traceback(self, trace, tree):
        tb = []
        while trace:
            frame = trace.tb_frame
            path = tree.get_filename(frame.f_code, frame)
            tb.append({"functionName": frame.f_code.co_name,
                       "filePath": path,
                       "lineNumber": frame.f_lineno,
                       "locals":
                           self._convert_locals_to_string(frame.f_locals)})
            trace = trace.tb_next
        self.trace = tb


class FilenameCaches(object):
    cached_filenames = {}

    def get_filename(self, code, frame):
        key = code.co_code
        file_name = self.cached_filenames.get(code.co_code, None)
        if file_name is None:
            try:
                file_name = inspect.getsourcefile(frame) or \
                            inspect.getfile(frame)
            except (TypeError, AttributeError):
                # These functions will fail if the frame is of a
                # built-in module, class or function
                return None
            self.cached_filenames[key] = file_name
        return file_name


class SystemMetrics(object):
    cpu_usage = 0.0
    mem_usage = 0.0
    inbound_network = 0
    outbound_network = 0
    prev_inbound = 0
    prev_outbound = 0

    def __init__(self):
        if psutil is not None:
            self.cpu_usage = psutil.cpu_percent(interval=1)
            self.mem_usage = psutil.virtual_memory().percent
            network = psutil.net_io_counters()
            self.prev_inbound = network.bytes_recv
            self.prev_outbound = network.bytes_sent

    def __iter__(self):
        yield "cpuUsage", self.cpu_usage
        yield "memoryUsage", self.mem_usage
        yield "inboundNetwork", self.inbound_network
        yield "outboundNetwork", self.outbound_network

    def update_network(self, interval):
        if psutil is not None:
            network = psutil.net_io_counters()
            self.inbound_network = (network.bytes_recv -
                                    self.prev_inbound) / interval
            self.outbound_network = (network.bytes_sent -
                                     self.prev_outbound) / interval
            self.prev_inbound = network.bytes_recv
            self.prev_outbound = network.bytes_sent


def contains_profiler(func_tuple):
    """Helper function that checks to see if the tuple contains
    the INVALID_PROFILE_FUNC in any string value of the tuple."""
    has_profiler = False
    for value in func_tuple:
        if isinstance(value, six.string_types):
            has_profiler |= '_lsprof.Profiler' in value
    return has_profiler


class AukletProfilerStats(Stats):
    root = None

    def get_root_func(self):
        if self.root is None:
            for func, (cc, nc, tt, ct, callers) in self.stats.items():
                if len(callers) == 0 and not contains_profiler(func):
                    self.root = func
                    break
        return self.root


class Function(object):
    callees = []

    def __init__(self, statobj, func, depth=0, stats=None,
                 id=0, parent_ids=[]):
        self.statobj = statobj
        self.func = func
        if stats:
            self.stats = stats
        else:
            self.stats = statobj.stats[func][:4]
        self.depth = depth
        self.id = id
        self.parent_ids = parent_ids

    def __dict__(self):
        return {
            "functionName": self.func[2],
            "lineNumber": self.func[1],
            "filePath": self.func[0],
            "nCalls": self.count(),
            "totalTime": self.total_time(),
            "timePerCall": self.total_time_per_call(),
            "callees": self.get_callees()
        }

    def get_callees(self):
        callees = []
        for callee in self.callees:
            if self.id in callee.parent_ids:
                callee.parent_ids.remove(self.id)
                callees.append(callee.__dict__())
        return callees

    def subfuncs(self):
        for func, stats in self.statobj.all_callees[self.func].items():
            yield Function(self.statobj,
                           func,
                           self.depth + 1,
                           stats=stats,
                           id=str(uuid1()),
                           parent_ids=self.parent_ids + [self.id])

    def count(self):
        return self.stats[1]

    def total_time(self):
        return self.stats[2]

    def total_time_per_call(self):
        _, nc, tt, _ = self.stats
        if nc == 0:
            return 0
        return tt / nc
