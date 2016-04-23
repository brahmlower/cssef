#!/usr/bin/python
from . import CssefTest
from cssefserver import tasks

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