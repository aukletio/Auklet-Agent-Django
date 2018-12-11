import unittest

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
        self.auklet_view_profiler.process_view(
            (1, 2, 3), self.Profiler, (1, 1), {})

    def tearDown(self):
        self.auklet_view_profiler = None

    def test_create_stack(self):
        self.assertIsNone(AukletViewProfiler.create_stack(self, '', ''))
        with patch('auklet.monitoring.Function') as _Function:
            _Function.side_effect = self.Function
            self.assertIsNotNone(
                self.auklet_view_profiler.create_stack('', ''))

    class Profiler:
        stats = ""

        def __init__(self, *args, **kw):
            pass

        @staticmethod
        def create_stats():
            pass

    class Function:
        callees = []

        def __init__(self, statobj, func, depth=0,stats=None, id=0,
                     parent_ids=[]):
            self.stats = [1, 1, 1, 1]

        def get_callees(self):
            return [self.SubFunction]

        class SubFunction:
            stats = [1, 1, 1, 1]

            @staticmethod
            def get_callees():
                return []
