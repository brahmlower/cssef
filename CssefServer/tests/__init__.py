import unittest
import os
from cssefserver.utils import create_database_connection
from cssefserver.utils import Configuration
class CssefTest(unittest.TestCase):
	def setUp(self):
		self.config = Configuration()
		self.config.load_config_file(self.config.global_config_path)
		self.config.database_path = "./db.sqlite3"
		self.dbConn = create_database_connection(self.config)

	def tearDown(self):
		self.dbConn.close()
		os.remove(self.config.database_path)

	def assert_dict_content(self, return_dict, expected_dict):
		self.assertEqual(return_dict['value'], expected_dict['value'])
		self.assertEqual(return_dict['content'], expected_dict['content'])
		self.assertEqual(return_dict['message'], expected_dict['message'])