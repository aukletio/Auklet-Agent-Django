import unittest
from unittest.mock import patch

from settings import AUKLET_CONFIG
from tests.set_config import set_config

from auklet.client import DjangoClient, get_client, init_client
from auklet.errors import AukletConfigurationError


class TestDjangoClient(unittest.TestCase):
    def setUp(self):
        set_config()
        self.client = DjangoClient()

    def test___init__(self):
        AUKLET_CONFIG["api_key"] = None
        self.assertRaises(
            AukletConfigurationError, lambda: DjangoClient.__init__(self))
        AUKLET_CONFIG["api_key"] = "123"

        AUKLET_CONFIG["application"] = None
        self.assertRaises(
            AukletConfigurationError, lambda: DjangoClient.__init__(self))
        AUKLET_CONFIG["application"] = "123"

        AUKLET_CONFIG["organization"] = None
        self.assertRaises(
            AukletConfigurationError, lambda: DjangoClient.__init__(self))
        AUKLET_CONFIG["organization"] = "123ß"

    def test_build_event_data(self):
        self.assertIsNotNone(
            self.client.build_event_data(
                type=self.Type, traceback=self.Traceback))

    def test_build_msgpack_event_data(self):
        self.assertIsNotNone(
            self.client.build_msgpack_event_data(
                type=self.Type, traceback=self.Traceback))

    def test_produce_event(self):
        with patch('auklet.broker.MQTTClient.produce') as _produce:
            _produce.side_effect = self.produce
            self.client.produce_event(self.Type, self.Traceback)
            self.assertTrue(test_produce)

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

    def produce(self, data):
        global test_produce
        test_produce = True


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
