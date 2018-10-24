from __future__ import absolute_import, division, unicode_literals

import inspect

try:
    import psutil
except ImportError:  # pragma: no cover
    # Some platforms that applications could be running on require specific
    # installation of psutil which we cannot configure currently
    psutil = None

__all__ = ['Event', 'SystemMetrics', 'FilenameCaches']


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
