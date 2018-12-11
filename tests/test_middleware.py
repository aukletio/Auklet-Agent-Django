import unittest
import threading

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

    def test_process_request(self):
        self.assertIsNone(self.middleware.process_request(''))
        self.assertIsNotNone(self.middleware.modules)

    def test_process_exception(self):
        with patch('sys.exc_info') as _exc_info:
            with patch('auklet.client.DjangoClient.produce_event') as _produce_event:
                _produce_event.side_effect = self.produce_event
                _exc_info.side_effect = self.exc_info
                self.middleware.process_exception('', '')
                self.assertTrue(test_produce_event)

    def test_process_view(self):
        self.assertTrue(
            self.middleware.process_view('', self.view_func, '', {}))
        with patch('auklet.middleware.get_monitor') as _get_monitor:
            AukletMiddleware.process_view(self, '', self.view_func, '', {})
        self.assertTrue(process_view_test)

    def test_process_response(self):
        with patch('auklet.middleware.get_monitor') as _get_monitor:
            with patch('auklet.client.DjangoClient.produce_stack') as _produce_stack:
                _get_monitor.return_value = True
                _produce_stack.side_effect = self.produce_stack
                AukletMiddleware.process_response(self, '', '')
        self.assertTrue(produce_stack_test)

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

    @staticmethod
    def produce_event(type, traceback):
        global test_produce_event
        test_produce_event = True

    @staticmethod
    def view_func(request, *args, **kwargs):
        return True

    class Modules:
        @staticmethod
        def process_view(request, view_func, view_args, view_kwargs):
            global process_view_test
            process_view_test = True

        @staticmethod
        def create_stack(request, response):
            class Res:
                class StatObj:
                    total_tt = 0
                    total_calls = 0

                statobj = StatObj
            return Res

    modules = {threading.current_thread().ident: Modules}

    @staticmethod
    def produce_stack(stack, total_time, total_calls):
        global produce_stack_test
        produce_stack_test = True


if __name__ == "__main__":
    unittest.main()
