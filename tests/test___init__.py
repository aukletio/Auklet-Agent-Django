import unittest
import cProfile

from auklet.monitoring import AukletViewProfiler

try:
    # For Python 3.0 and later
    from unittest.mock import patch
except ImportError:
    # Fall back to Python 2's mock
    from mock import patch


class TestAukletViewProfiler(unittest.TestCase):
    def setUp(self):
        self.auklet_view_profiler = AukletViewProfiler()

    def test_process_view(self):
        with patch('cProfile.Profile.runcall') as _runcall:
            _runcall.return_value = True
            self.assertTrue(
                self.auklet_view_profiler.process_view(
                    (), self.auklet_view_profiler, (), {}))

    def test_create_stack(self):
        with patch('auklet.monitoring.AukletProfilerStats') \
                as _AukletProfilerStats:
            with patch('auklet.monitoring.Function') as _Function:
                _AukletProfilerStats.side_effect = self.AukletProfilerStats
                _Function.side_effect = self.Function
                self.auklet_view_profiler.profiler = cProfile.Profile()
                self.assertIsNotNone(
                    self.auklet_view_profiler.create_stack('', ''))
        self.assertIsNone(AukletViewProfiler.create_stack(self, '', ''))

    class AukletProfilerStats:
        @staticmethod
        def __init__(profiler):
            pass

        @staticmethod
        def calc_callees():
            pass

        @staticmethod
        def get_root_func():
            return True

    class Function:
        stats = [1, 1, 1, 1]
        callees = []

        @staticmethod
        def __init__(stats, root_func, depth):
            pass

        def get_callees(self):
            return [self.SubFunc]

        class SubFunc:
            stats = [1, 1, 1, 1]

            @staticmethod
            def get_callees():
                return []
