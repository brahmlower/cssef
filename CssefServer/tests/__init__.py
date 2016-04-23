import unittest
import os
from cssefserver.utils import createDatabaseConnection
from cssefserver.utils import Configuration
class CssefTest(unittest.TestCase):
	def setUp(self):
		self.config = Configuration()
		self.config.loadConfigFile(self.config.globalConfigPath)
		self.config.database_path = "./db.sqlite3"
		self.dbConn = createDatabaseConnection(self.config)

	def tearDown(self):
		self.dbConn.close()
		os.remove(self.config.database_path)

	def assertDictContent(self, returnDict, expectedDict):
		self.assertEqual(returnDict['value'], expectedDict['value'])
		self.assertEqual(returnDict['content'], expectedDict['content'])
		self.assertEqual(returnDict['message'], expectedDict['message'])