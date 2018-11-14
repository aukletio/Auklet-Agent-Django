import unittest

from tests.set_config import set_config

from auklet.middleware import AukletMiddleware

try:
    # For Python 3.0 and later
    from unittest.mock import patch
except ImportError:
    # Fall back to Python 2's mock
    from mock import patch


class TestAukletMiddleware(unittest.TestCase):
    def setUp(self):
        set_config()
        self.middleware = AukletMiddleware()

    def test_process_exception(self):
        with patch('sys.exc_info') as _exc_info:
            with patch('auklet.client.DjangoClient.produce_event') as _produce_event:
                _produce_event.side_effect = self.produce_event
                _exc_info.side_effect = self.exc_info
                self.middleware.process_exception("", "")
                self.assertTrue(test_produce_event)

    def exc_info(self):
        return self.ExcType, None, self.Traceback

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

    def produce_event(self, type, traceback):
        global test_produce_event
        test_produce_event = True


if __name__ == "__main__":
    unittest.main()
