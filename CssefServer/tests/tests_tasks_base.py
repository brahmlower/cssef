#!/usr/bin/python
import unittest
import os
from cssefserver import tasks
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

class Login(CssefTest):
	def test_credentialSuccess(self):
		endpoint = tasks.Login(self.config, self.dbConn)
		returnDict = endpoint(username = "admin", password = "admin", organization = 1)
		expectedDict = {'content': ['Success'], 'message': [], 'value': 0}
		self.assertDictContent(returnDict, expectedDict)

	def test_credentialFailUser(self):
		endpoint = tasks.Login(self.config, self.dbConn)
		returnDict = endpoint(username = "fail", password = "admin", organization = 1)
		expectedDict = {'content': [], 'message': ['Incorrect username or password.'], 'value': 1}
		self.assertDictContent(returnDict, expectedDict)

	def test_credentialFailPassword(self):
		endpoint = tasks.Login(self.config, self.dbConn)
		returnDict = endpoint(username = "admin", password = "fail", organization = 1)
		expectedDict = {'content': [], 'message': ['Incorrect username or password.'], 'value': 1}
		self.assertDictContent(returnDict, expectedDict)

	def test_credentialFailOrganization(self):
		endpoint = tasks.Login(self.config, self.dbConn)
		returnDict = endpoint(username = "admin", password = "admin", organization = 9001)
		expectedDict = {'content': [], 'message': ['Incorrect username or password.'], 'value': 1}
		self.assertDictContent(returnDict, expectedDict)

	def test_credentialNoPasswordWithToken(self):
		endpoint = tasks.Login(self.config, self.dbConn)
		returnDict = endpoint(username = "missing", token = "abc123", organization = 1)
		expectedDict = {'content': [], 'message': ['Token may not be used to log in.'], 'value': 2}
		self.assertDictContent(returnDict, expectedDict)

class RenewToken(CssefTest):
	pass

class AvailableEndpoints(CssefTest):
	pass