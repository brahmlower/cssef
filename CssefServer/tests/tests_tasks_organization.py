#!/usr/bin/python
import unittest
import os
from cssefserver.account import tasks
from cssefserver.utils import createDatabaseConnection
from cssefserver.utils import Configuration

class CssefTest(unittest.TestCase):
	def setUp(self):
		self.config = Configuration()
		self.config.loadConfigFile(self.config.globalConfigPath)
		self.dbConn = createDatabaseConnection(self.config)

	def tearDown(self):
		self.dbConn.close()
		os.remove(self.config.database_path)

	def assertDictContent(self, returnDict, expectedDict):
		self.assertEqual(returnDict['value'], expectedDict['value'])
		self.assertEqual(returnDict['content'], expectedDict['content'])
		self.assertEqual(returnDict['message'], expectedDict['message'])

class OrganizationAdd(CssefTest):
	def test_onlyNameProvided(self):
		# Prepare the admin token
		self.config.admin_token = "abc123"
		# Instantiate the endpoint
		endpoint = tasks.OrganizationAdd(self.config, self.dbConn)
		# Call the endpoint as if it's been requested through flask
		authDict = {'admin-token': self.config.admin_token}
		orgDict = {'name': 'Test Org'}
		returnDict = endpoint(auth = authDict, **orgDict)
		# Verify that the return data is as expected
		self.assertEqual(returnDict['value'], 0)
		content = returnDict['content'][0]
		self.assertEqual(content['name'], 'Test Org')