import os
import unittest
import requests

from mock import patch
from requests import HTTPError

from auklet.utils import *
from auklet.client import DjangoClient
from auklet.errors import AukletConfigurationError

try:
    # For Python 3.0 and later
    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request, HTTPError, URLError


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.client = DjangoClient()

    def test(self):
        print()

    # def test_open_auklet_url(self):
    #     url = self.client.base_url + "private/devices/config/"
    #
    #     with patch('auklet.utils.urlopen') as url_open:
    #         self.assertIsNotNone(open_auklet_url(url, self.client.apikey))
    #
    #         url_open.side_effect = HTTPError(
    #             url=None, code=401, msg=None, hdrs=None, fp=None)
    #         self.assertRaises(AukletConfigurationError,
    #                           lambda: open_auklet_url(url, self.client.apikey))
    #
    #         url_open.side_effect = HTTPError(
    #             url=None, code=None, msg=None, hdrs=None, fp=None)
    #         self.assertRaises(HTTPError,
    #                           lambda: open_auklet_url(url, self.client.apikey))
    #
    #         url_open.side_effect = URLError("")
    #         self.assertIsNone(open_auklet_url(url, self.client.apikey))
    #
    # def test_post_auklet_url(self):
    #     with patch("auklet.utils.requests.post") as request_mock:
    #         request_mock.side_effect = requests.HTTPError(None)
    #         res = post_auklet_url("example.com", "apikey", {})
    #         self.assertIsNone(res)
    #
    # def test_create_auklet_dir(self):
    #     self.assertTrue(create_dir(".test_auklet"))
    #
    # def test_create_dir_temp(self):
    #     with patch("os.access") as os_access_mock:
    #         os_access_mock.return_value = False
    #         self.assertTrue(create_dir(".temp_auklet"))
    #
    # def test_create_file(self):
    #     files = ['.auklet/local.txt', '.auklet/limits',
    #              '.auklet/usage', '.auklet/communication']
    #     for f in files:
    #         file = False
    #         if os.path.isfile(f):
    #             file = True
    #         self.assertTrue(file)
    #
    # def test_clear_file(self):
    #     file_name = "unit_test_temp"
    #     with open(file_name, "w") as unit_test_temp_file:
    #         unit_test_temp_file.write("data")
    #     clear_file(file_name)
    #     self.assertEqual(os.path.getsize(file_name), 0)
    #     os.remove(file_name)
    #
    # def test_build_url(self):
    #     extension = str("private/devices/config/")
    #     self.assertEqual(
    #         build_url(self.client.base_url, extension),
    #         self.client.base_url + extension)
    #
    # def test_get_mac(self):
    #     self.assertNotEqual(get_mac(), None)
    #
    # def test_get_device_ip(self):
    #     self.assertIsNotNone(get_device_ip())
    #     with patch('auklet.utils.Request') as _Request:
    #         _Request.side_effect = HTTPError(None, None, None, None, None)
    #         self.assertIsNone(get_device_ip())
    #         _Request.side_effect = URLError(None)
    #         self.assertIsNone(get_device_ip())
    #         _Request.side_effect = Exception
    #         self.assertIsNone(get_device_ip())
    #
    # def test_get_agent_version(self):
    #     print(get_agent_version())


if __name__ == '__main__':
    unittest.main()
