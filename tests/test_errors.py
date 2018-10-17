import sys
import unittest

from auklet.errors \
    import AukletException, AukletConnectionError, AukletConfigurationError


class TestAukletException(unittest.TestCase):
    def test_auklet_exception(self):
        if sys.version_info < (3,):
            self.assertEqual(
                str(AukletException(Exception)),
                "<type 'exceptions.Exception'>")
        else:
            self.assertEqual(
                str(AukletException(Exception)),
                "<class 'Exception'>")


class TestAukletConnectionError(unittest.TestCase):
    def test_auklet_connection_error(self):
        self.assertEqual(str(AukletConnectionError()), "")


class TestAukletConfigurationError(unittest.TestCase):
    def test_auklet_configuration_error(self):
        self.assertEqual(str(AukletConfigurationError()), "")


if __name__ == '__main__':
    unittest.main()
