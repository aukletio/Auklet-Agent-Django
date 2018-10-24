import os
import ast
import unittest

from mock import patch
from tests import data_factory

from auklet.client import DjangoClient
from auklet.broker import MQTTClient


def recreate_files():
    os.system("touch .auklet/version")
    os.system("touch .auklet/communication")
    os.system("touch .auklet/usage")
    os.system("touch .auklet/limits")


class TestMQTTBroker(unittest.TestCase):
    data = ast.literal_eval(str(data_factory.MonitoringDataFactory()))
    config = ast.literal_eval(str(data_factory.ConfigFactory()))

    def setUp(self):
        self.client = DjangoClient
        self.broker = MQTTClient("http://example.com", "1", "", "", "", "http://example.com/", ".auklet")

    def test_get_certs(self):
        os.system("touch .auklet/ca.pem")
        self.assertTrue(self.broker._get_certs())
        os.system("rm .auklet/ca.pem")
        self.assertFalse(self.broker._get_certs())
        with patch('auklet.broker.urlopen') as _urlopen:
            _urlopen.return_value = self._Res
            self.broker._get_certs()
        with open(".auklet/ca.pem", "rb") as file:
            self.assertEqual(b'data', file.read())
        os.system("rm .auklet/ca.pem")

    def test_on_disconnect(self):
        def debug(msg):
            global debug_msg
            debug_msg = msg

        with patch('logging.debug') as _debug:
            _debug.side_effect = debug
            self.broker.on_disconnect(None, "", 1)
            self.assertIsNotNone(debug_msg)

    def test_create_producer(self):
        self.assertTrue(self.broker.create_producer())
        with patch('auklet.broker.MQTTClient._get_certs') as get_certs:
            get_certs.return_value = True
            with patch('paho.mqtt.client.Client') as _Client:
                _Client.side_effect = self.Client
                self.broker.create_producer()
                self.assertTrue(connect_test)

    def test_produce(self):
        with patch('paho.mqtt.client.Client.publish') as _publish:
            with patch('auklet.broker.MQTTClient._get_certs') as get_certs:
                with patch('paho.mqtt.client.Client') as _Client:
                    _publish.side_effect = self.Client.publish
                    get_certs.return_value = True
                    _Client.side_effect = self.Client
                    self.broker.produce(self.data)
                    self.assertTrue(disconnect_test)

    class _Res:
        @staticmethod
        def read():
            return b"data"

    class Client:
        def __init__(self, client_id, protocol, transport):
            pass

        def username_pw_set(self, username, password):
            pass

        def enable_logger(self):
            pass

        def tls_set_context(self):
            pass

        def on_disconnect(self):
            pass

        def connect(self, host, port):
            global connect_test
            connect_test = True

        def disconnect(self):
            global disconnect_test
            disconnect_test = True

        def publish(self, topic, payload):
            return self.Producer

        class Producer:
            @staticmethod
            def wait_for_publish():
                pass


if __name__ == '__main__':
    unittest.main()
