import unittest
import threading

from django.test import TestCase, override_settings


from auklet.client import DjangoClient, get_client, init_client
from auklet.errors import AukletConfigurationError

from tests.set_config import set_config

try:
    # For Python 3.0 and later
    from unittest.mock import patch
except ImportError:
    # Fall back to Python 2's mock
    from mock import patch


class TestDjangoClientInit(TestCase):
    def setUp(self):
        self.client = DjangoClient()

    @override_settings(AUKLET_CONFIG={"api_key": None,
                                      "application": "123",
                                      "organization": "123"})
    def test___init___no_api_key(self):
        self.assertRaises(AukletConfigurationError,
                          lambda: self.client.__init__())

    @override_settings(AUKLET_CONFIG={"api_key": "123",
                                      "application": None,
                                      "organization": "123"})
    def test___init___no_appid(self):
        self.assertRaises(AukletConfigurationError,
                          lambda: self.client.__init__())

    @override_settings(AUKLET_CONFIG={"api_key": "123",
                                      "application": "123",
                                      "organization": None})
    def test___init___no_org_id(self):
        self.assertRaises(AukletConfigurationError,
                          lambda: self.client.__init__())


class TestDjangoClient(unittest.TestCase):
    def setUp(self):
        set_config()
        self.django_client = DjangoClient()

    def test_produce_event(self):
        global produce_test
        with patch('auklet.broker.MQTTClient.produce') as _produce:
            _produce.side_effect = self.produce
            self.django_client.produce_event(self.Type, self.Traceback)
        self.assertTrue(produce_test)
        produce_test = False

    def test_produce_stack(self):
        global produce_test
        init_client()
        with patch('auklet.broker.MQTTClient.produce') as _produce:
            _produce.side_effect = self.produce
            self.django_client.produce_stack(self.Stack, 1, 1)
        self.assertTrue(produce_test)
        produce_test = False

    class Type:
        __name__ = ""

    class Traceback:
        class FCode:
            class CoCode:
                co_code = ""
                co_name = ""
            f_code = CoCode()
            f_lineno = 0
            f_locals = [1, 1]
        tb_lineno = 0
        tb_frame = FCode()
        tb_next = None

    @staticmethod
    def produce(data, data_type="event"):
        global produce_test
        produce_test = True

    class Stack():
        def as_dict(self):
            return {}

    class Modules(object):
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


class TestClient(unittest.TestCase):
    def setUp(self):
        set_config()

    def test_get_client(self):
        self.assertIsNotNone(get_client())
        global _client
        _client = None
        self.assertIsNotNone(get_client())

    def test_init_client(self):
        init_client()
        client = DjangoClient()
        self.assertIsNotNone(client)


if __name__ == "__main__":
    unittest.main()
