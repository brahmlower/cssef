import os
import stat
from getpass import getpass
from cssefclient.utils import CeleryEndpoint

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
		self.celeryName = 'availableEndpoints'
		self.args = []

class Login(CeleryEndpoint):
	def __init__(self, config):
		self.config = config
		self.celeryName = 'login'
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
		if not os.path.exists(self.config.token_file):
			# The file doesn't exist yet, make it
			open(self.config.token_file, 'a').close()
		os.chmod(self.config.token_file, stat.S_IRUSR | stat.S_IWUSR)
		open(self.config.token_file, 'w').write(returnDict.content[0])
		returnDict.content = ["Authentication was successful."]
		return returnDict

class Logout(CeleryEndpoint):
	def __init__(self, config):
		self.celeryName = 'logout'
		self.args = []
		self.config = config

	def execute(self):
		pass