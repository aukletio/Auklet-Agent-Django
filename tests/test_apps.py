import unittest
from unittest.mock import patch

from auklet.apps import AukletConfig


class TestAukletConfig(unittest.TestCase):
    def test_ready(self):
        with patch('auklet.client.init_client') as _init_client:
            _init_client.side_effect = self.init_client
            AukletConfig.ready(AukletConfig)
            self.assertTrue(init_client_test)

    def init_client(self):
        global init_client_test    # Variable used to see if function is called
        init_client_test = True


if __name__ == '__main__':
    unittest.main()
