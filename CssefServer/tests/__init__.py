import unittest
import os
#from cssefserver import Configuration
from cssefserver.utils import create_database_connection

class CssefTest(unittest.TestCase):
    def setUp(self):
        # self.config = Configuration()
        # self.config.load_settings_file(self.config.global_config_path)
        # self.config.database_path = ""
        self.database_connection = create_database_connection("")

    def tearDown(self):
        self.database_connection.close()

    def assert_dict_content(self, return_dict, expected_dict):
        self.assertEqual(return_dict['value'], expected_dict['value'])
        self.assertEqual(return_dict['content'], expected_dict['content'])
        self.assertEqual(return_dict['message'], expected_dict['message'])