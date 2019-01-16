import sys
import unittest

from auklet.stats import Event, FilenameCaches, SystemMetrics, \
    AukletProfilerStats, Function, contains_profiler

try:
    # For Python 3.0 and later
    from unittest.mock import patch
except ImportError:
    # Fall back to Python 2's mock
    from mock import patch


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.event = Event(self.ExcType, self.Traceback, self.Tree)

    def test___iter__(self):
        for value in self.event.__iter__():
            self.assertIsNotNone(value)

    def test_convert_locals_to_string(self):
        self.assertNotEqual(
            self.event._convert_locals_to_string(
                local_vars={"key": "value"}), None)
        self.assertNotEqual(
            self.event._convert_locals_to_string(
                local_vars={"key": True}), None)

    def test__build_traceback(self):
        self.event._build_traceback(self.Traceback, self.Tree)
        self.assertIsNotNone(self.event.trace)

    class ExcType:
        __name__ = ""

    class Traceback:
        class TbFrame:
            class CoCode:
                co_code = None
                co_name = ""
            f_code = CoCode
            f_lineno = 0
            f_locals = [0, 0]
        tb_lineno = ""
        tb_frame = TbFrame
        tb_next = None

    class Tree:
        @staticmethod
        def get_filename(f_code, frame):
            return ""


class TestFilenameCache(unittest.TestCase):
    def setUp(self):
        self.filename_caches = FilenameCaches()

    def test_get_filename(self):
        self.filename_caches.cached_filenames.clear()
        self.filename_caches.cached_filenames['file_name'] = "file_name"
        self.assertEqual(
            self.filename_caches.get_filename(
                code=self.get_code(), frame="frame"),
            self.get_code().co_code)

        self.filename_caches.cached_filenames.clear()
        self.filename_caches.cached_filenames['file_name'] = None
        self.assertIsNone(self.filename_caches.get_filename(
            code=self.get_code(), frame="frame"))

        with patch('inspect.getsourcefile') as _get_source_file:
            _get_source_file.return_value = "file_name"
            self.assertIsNotNone(self.filename_caches.get_filename(
                code=self.get_code(), frame="frame"))

    def get_code(self):
        class Code:
            co_code = "file_name"
            co_firstlineno = 0
            co_name = ""
        return Code


class TestSystemMetrics(unittest.TestCase):
    def setUp(self):
        self.system_metrics = SystemMetrics()

    def test___iter__(self):
        for value in self.system_metrics.__iter__():
            self.assertIsNotNone(value)

    def test_update_network(self):
        self.system_metrics.update_network(1)
        self.assertIsNotNone(self.system_metrics.inbound_network)
        self.assertIsNotNone(self.system_metrics.outbound_network)
        self.assertIsNotNone(self.system_metrics.prev_inbound)
        self.assertIsNotNone(self.system_metrics.prev_outbound)


class TestAukletProfilerStats(unittest.TestCase, AukletProfilerStats):
    def setUp(self):
        self.profiler = AukletProfilerStats

    def test_get_root_function(self):
        with patch('auklet.stats.contains_profiler') as _contains_profiler:
            _contains_profiler.return_value = None
            self.profiler.root = None
            self.profiler.stats = {1: ('', '', '', '', '')}
            self.assertIs(1, self.profiler.get_root_func(self))


class TestFunction(unittest.TestCase):
    def setUp(self):
        self.function = Function("", [1, 2, 3], stats=['', '', ''])

    def test___init__(self):
        self.function.__init__(self.StatObj, 0)

    def test_as_dict(self):
        patcher = patch('auklet.stats.Function.get_formatted_callees',
                        self._get_formatted_callees)
        if sys.version_info < (3,):
            patcher.start()
        self.function.stats = ['', 1, 1, '']
        self.function.id = 1
        self.function.depth = 0
        self.function.callees = [self.Callee]
        self.assertIsNotNone(self.function.as_dict())
        self.function.stats = ['', 0, 1, '']
        self.assertIsNotNone(self.function.as_dict())

    def test_get_callees(self):
        self.function.func = 0
        self.function.statobj = self.StatObj
        self.assertIsNotNone(next(self.function.get_callees()))

    class Callee:
        parent_ids = [1, 1]
        depth = 1

        def as_dict(self):
            return {}

    def _get_formatted_callees(self):
        return 0

    class StatObj:
        all_callees = [{1: ""}]
        stats = [[1, 1, 1, 1], ""]


class TestStats(unittest.TestCase):
    def test_contains_profiler(self):
        self.assertFalse(contains_profiler(""))
        self.assertFalse(contains_profiler(" lsprof.Profiler"))


if __name__ == "__main__":
    unittest.main()
