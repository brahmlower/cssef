#!/usr/bin/python
from . import CssefTest
from cssefserver import tasks

class Login(CssefTest):
	def test_credentialSuccess(self):
		endpoint = tasks.Login(self.config, self.db_connection)
		return_dict = endpoint(username = "admin", password = "admin", organization = 1)
		expected_dict = {'content': ['Success'], 'message': [], 'value': 0}
		self.assert_dict_content(return_dict, expected_dict)

	def test_credentialFailUser(self):
		endpoint = tasks.Login(self.config, self.db_connection)
		return_dict = endpoint(username = "fail", password = "admin", organization = 1)
		expected_dict = {'content': [], 'message': ['Incorrect username or password.'], 'value': 1}
		self.assert_dict_content(return_dict, expected_dict)

	def test_credentialFailPassword(self):
		endpoint = tasks.Login(self.config, self.db_connection)
		return_dict = endpoint(username = "admin", password = "fail", organization = 1)
		expected_dict = {'content': [], 'message': ['Incorrect username or password.'], 'value': 1}
		self.assert_dict_content(return_dict, expected_dict)

	def test_credentialFailOrganization(self):
		endpoint = tasks.Login(self.config, self.db_connection)
		return_dict = endpoint(username = "admin", password = "admin", organization = 9001)
		expected_dict = {'content': [], 'message': ['Incorrect username or password.'], 'value': 1}
		self.assert_dict_content(return_dict, expected_dict)

	def test_credentialNoPasswordWithToken(self):
		endpoint = tasks.Login(self.config, self.db_connection)
		return_dict = endpoint(username = "missing", token = "abc123", organization = 1)
		expected_dict = {'content': [], 'message': ['Token may not be used to log in.'], 'value': 2}
		self.assert_dict_content(return_dict, expected_dict)

class RenewToken(CssefTest):
	pass

class AvailableEndpoints(CssefTest):
	pass