import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cssefserver'))
from cssefserver import Configuration
from cssefserver import CssefServer
from cssefserver.databaseutils import create_database_connection

class CssefTest(unittest.TestCase):
    def setUp(self):
        self.server = CssefServer(config=Configuration())
        self.server.database_connection = create_database_connection(self.server.config.database_path)

    def assert_dict_content(self, return_dict, expected_dict):
        self.assertEqual(return_dict['value'], expected_dict['value'])
        self.assertEqual(return_dict['content'], expected_dict['content'])
        self.assertEqual(return_dict['message'], expected_dict['message'])