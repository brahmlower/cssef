from getpass import getpass
from cssefclient.utils import CeleryEndpoint
from cssefclient.utils import saveAuthToken

class AvailableEndpoints(CeleryEndpoint):
	def __init__(self, config):
		"""Instiantiates a new instance of AvailableEndpoints.
 
		This is hardcoded because this task/endpoint will be available on all
		configurations of the server.
		
		Args:
			config (Configuration): The current configuration to use

		Attributes:
			config (Configuration): The current configuration to use
			celeryName (str): The task name to call through Celery
			args (list): The required arguments while calling the celery task
		"""
		self.config = config
		self.celeryName = 'AvailableEndpoints'
		self.args = []

class RenewToken(CeleryEndpoint):
	def __init__(self, config):
		self.config = config
		self.celeryName = 'RenewToken'

	def execute(self, **kwargs):
		# Populate the arguments to pass to the login
		# Here we only need the username and the token
		if not kwargs.get('username'):
			kwargs['username'] = self.config.username
		if not kwargs.get('organization'):
			kwargs['organization'] = self.config.organization
		if not kwargs.get('token'):
			kwargs['token'] = self.config.token
		# Attempt to log in
		returnDict = super(RenewToken, self).execute(**kwargs)
		if returnDict.value != 0:
			return returnDict
		token = returnDict.content[0]
		saveAuthToken(self.config.token_file, token)
		returnDict.content = ["Token rewnewal was successful."]
		return returnDict

class Login(CeleryEndpoint):
	def __init__(self, config):
		self.config = config
		self.celeryName = 'Login'
		self.args = []

	def execute(self, **kwargs):
		if not self.config.token_auth_enabled:
			# Bail if token authentication is disabled
			if config.verbose:
				print "[ERROR] Logging in requires that token authentication be \
					enabled. Set 'token_auth_enabled: True' in your \
					configuration."
			return None
		if not kwargs.get('username'):
			kwargs['username'] = self.config.username
		if not kwargs.get('organization'):
			kwargs['organization'] = self.config.organization
		if not kwargs.get('password'):
			kwargs['password'] = getpass()
		# Attempt to log in
		returnDict = super(Login, self).execute(**kwargs)
		if returnDict.value != 0:
			return returnDict
		# Save the returned token
		token = returnDict.content[0]
		saveAuthToken(self.config.token_file, token)
		returnDict.content = ["Authentication was successful."]
		return returnDict

class Logout(CeleryEndpoint):
	def __init__(self, config):
		self.celeryName = 'logout'
		self.args = []
		self.config = config

	def execute(self):
		pass