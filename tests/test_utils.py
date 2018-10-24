import os
import requests

import unittest
from unittest.mock import patch

from tests.set_config import set_config

from auklet.utils import *
from auklet.client import DjangoClient

try:
    # For Python 3.0 and later
    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request, HTTPError, URLError


class TestUtils(unittest.TestCase):
    def setUp(self):
        set_config()
        self.client = DjangoClient()

    def test_open_auklet_url(self):
        url = self.client.base_url + "private/devices/config/"
        self.assertEqual(None, open_auklet_url("example.com", "api_key"))
        self.assertEqual(
            "<Response [401]>", str(open_auklet_url(url, "api_key")))

    def test_post_auklet_url(self):
        with patch("auklet.utils.requests.post") as request_mock:
            request_mock.side_effect = requests.HTTPError(None)
            self.assertIsNone(post_auklet_url("example.com", "apikey", {}))
        with patch('requests.api.post') as _post:
            _post.return_value = "123"
            with patch('requests.models.Response.json') as _json:
                _json.return_value = "123"
                self.assertIs(
                    "123", post_auklet_url("http://example.com", "apikey", {}))

    def test_create_auklet_dir(self):
        self.assertTrue(create_dir(".test_auklet"))

    def test_create_dir_temp(self):
        with patch("os.access") as os_access_mock:
            os_access_mock.return_value = False
            self.assertTrue(create_dir(".temp_auklet"))

    def test_create_file(self):
        files = ['.auklet/local.txt', '.auklet/limits',
                 '.auklet/usage', '.auklet/communication']
        for f in files:
            create_file(f)
            file = False
            if os.path.isfile(f):
                file = True
            self.assertTrue(file)

    def test_clear_file(self):
        file_name = "unit_test_temp"
        with open(file_name, "w") as unit_test_temp_file:
            unit_test_temp_file.write("data")
        clear_file(file_name)
        self.assertEqual(os.path.getsize(file_name), 0)
        os.remove(file_name)

    def test_build_url(self):
        extension = str("private/devices/config/")
        self.assertEqual(
            build_url(self.client.base_url, extension),
            self.client.base_url + extension)

    def test_get_mac(self):
        self.assertNotEqual(get_mac(), None)

    def test_get_device_ip(self):
        self.assertIsNotNone(get_device_ip())
        with patch('auklet.utils.u') as _u:
            _u.side_effect = requests.RequestException
            self.assertIsNone(get_device_ip())

    def test_get_agent_version(self):
        self.assertIsNotNone(get_agent_version())

    def test_version_info(self):
        self.assertNotEqual(None, b('b'))
        self.assertNotEqual(None, u(b'u'))

if __name__ == '__main__':
    unittest.main()
