import unittest

try:
    # For Python 3.0 and later
    from unittest.mock import patch
except ImportError:
    # Fall back to Python 2's mock
    from mock import patch


class TestAukletConfig(unittest.TestCase):
    # No need to test this function at this time, but is there if needed
    pass


if __name__ == '__main__':
    unittest.main()
