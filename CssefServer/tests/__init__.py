import unittest
import os

try:
    import systemd
except:
    import sys
    try:
        from unittest.mock import MagicMock
    except ImportError:
        from mock import MagicMock

    sys.modules['systemd'] = MagicMock()

from cssefserver import Configuration
from cssefserver.databaseutils import create_database_connection


class CssefTest(unittest.TestCase):
    def setUp(self):
        self.config = Configuration()
        self.database_connection = create_database_connection()

    def tearDown(self):
        self.database_connection.close()

    def assert_dict_content(self, return_dict, expected_dict):
        self.assertEqual(return_dict['value'], expected_dict['value'])
        self.assertEqual(return_dict['content'], expected_dict['content'])
        self.assertEqual(return_dict['message'], expected_dict['message'])