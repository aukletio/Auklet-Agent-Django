import unittest

from auklet.monitoring.logging import AukletLogging


class TestAukletLogging(unittest.TestCase):
    def setUp(self):
        self.auklet_logging = AukletLogging()

    def base_test_log(self, function):
        self.assertRaises(
            NotImplementedError, lambda: function(
                msg="", data_type=str))

    def test_log(self):
        self.base_test_log(self.auklet_logging.log)

    def test_debug(self):
        self.base_test_log(self.auklet_logging.debug)

    def test_info(self):
        self.base_test_log(self.auklet_logging.info)

    def test_warning(self):
        self.base_test_log(self.auklet_logging.warning)

    def test_error(self):
        self.base_test_log(self.auklet_logging.error)

    def test_critical(self):
        self.base_test_log(self.auklet_logging.critical)


if __name__ == '__main__':
    unittest.main()
