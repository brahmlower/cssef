#!/usr/bin/python
from . import CssefTest
from cssefserver import tasks

class Login(CssefTest):
	def test_credential_success(self):
		endpoint = tasks.Login(self.config, self.db_connection)
		return_dict = endpoint(username = "admin", password = "admin", organization = 1)
		expected_dict = {'content': ['Success'], 'message': [], 'value': 0}
		self.assert_dict_content(return_dict, expected_dict)

	def test_credential_fail_user(self):
		endpoint = tasks.Login(self.config, self.db_connection)
		return_dict = endpoint(username = "fail", password = "admin", organization = 1)
		expected_dict = {'content': [], 'message': ['Incorrect username or password.'], 'value': 1}
		self.assert_dict_content(return_dict, expected_dict)

	def test_credential_fail_password(self):
		endpoint = tasks.Login(self.config, self.db_connection)
		return_dict = endpoint(username = "admin", password = "fail", organization = 1)
		expected_dict = {'content': [], 'message': ['Incorrect username or password.'], 'value': 1}
		self.assert_dict_content(return_dict, expected_dict)

	def test_credential_fail_organization(self):
		endpoint = tasks.Login(self.config, self.db_connection)
		return_dict = endpoint(username = "admin", password = "admin", organization = 9001)
		expected_dict = {'content': [], 'message': ['Incorrect username or password.'], 'value': 1}
		self.assert_dict_content(return_dict, expected_dict)

	def test_credential_no_password_with_token(self):
		endpoint = tasks.Login(self.config, self.db_connection)
		return_dict = endpoint(username = "missing", token = "abc123", organization = 1)
		expected_dict = {'content': [], 'message': ['Token may not be used to log in.'], 'value': 2}
		self.assert_dict_content(return_dict, expected_dict)

class RenewToken(CssefTest):
	pass

class AvailableEndpoints(CssefTest):
	pass