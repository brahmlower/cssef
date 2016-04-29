from cssefclient.utils import RPCEndpoint
from cssefclient.utils import saveTokenFile

class AvailableEndpoints(RPCEndpoint):
	def __init__(self, config):
		"""Instiantiates a new instance of AvailableEndpoints.

		This is hardcoded because this task/endpoint will be available on all
		configurations of the server.

		Args:
			config (Configuration): The current configuration to use

		Attributes:
			config (Configuration): The current configuration to use
			endpointName (str): The rpc endpoint name
			args (list): The required arguments while calling the rpc endpoint
		"""
		self.config = config
		self.rpc_name = 'availableendpoints'

class RenewToken(RPCEndpoint):
	def __init__(self, config):
		self.config = config
		self.rpc_name = 'renewtoken'

	def execute(self, **kwargs):
		print kwargs
		# # Populate the arguments to pass to the login
		# # Here we only need the username and the token
		# if not kwargs.get('username'):
		# 	kwargs['username'] = self.config.username
		# if not kwargs.get('organization'):
		# 	kwargs['organization'] = self.config.organization
		# if not kwargs.get('token'):
		# 	kwargs['token'] = self.config.token
		# Attempt to log in
		returnDict = super(RenewToken, self).execute(**kwargs.get('auth'))
		if returnDict.value != 0:
			return returnDict
		token = returnDict.content[0]
		saveTokenFile(self.config.token_file, token)
		returnDict.content = ["Token rewnewal was successful."]
		return returnDict

class Login(RPCEndpoint):
	def __init__(self, config):
		self.config = config
		self.rpc_name = 'login'

	def execute(self, **kwargs):
		if not self.config.token_auth_enabled:
			# Bail if token authentication is disabled
			if self.config.verbose:
				print "[ERROR] Logging in requires that token authentication be \
					enabled. Set 'token_auth_enabled: True' in your \
					configuration."
			return None
		# Attempt to log in
		returnDict = super(Login, self).execute(**kwargs.get('auth'))
		if returnDict.value != 0:
			return returnDict
		# Save the returned token
		token = returnDict.content[0]
		saveTokenFile(self.config.token_file, token)
		returnDict.content = ["Authentication was successful."]
		return returnDict

class Logout(RPCEndpoint):
	def __init__(self, config):
		self.rpc_name = 'logout'
		self.config = config

	def execute(self):
		pass
