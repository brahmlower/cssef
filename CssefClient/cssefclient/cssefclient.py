import os
import sys
from time import sleep
import yaml
from celery import Celery

versionMajor = '0'
versionMinor = '0'
versionPatch = '3'
version = ".".join([versionMajor, versionMinor, versionPatch])

def getConn(config):
	"""Establishes a connection to the celery server

	Args:
		config (Configuration): An instance of a Configuration object

	Returns:
		This will return an instance of Celery, which is connected to the
		server specified in the provided Configuration object. This Celery
		object can be provided to CeleryEndpoint object to execute a task.
	"""
	rpcUrl = "rpc://%s:%s@%s//" % (config.rpc_username, config.rpc_password, config.rpc_host)
	amqpUrl = "amqp://%s:%s@%s//" % (config.amqp_username, config.amqp_password, config.amqp_host)
	return Celery('api', backend = rpcUrl, broker = amqpUrl)

class Configuration(object):
	def __init__(self):
		# Super global configs
		self.globalConfigPath = "/etc/cssef/cssef.yml"
		self.configPath = os.path.expanduser("~/.cssef/cssef.yml")
		# Default values for the client configuration
		self.rpc_username = "cssefd"
		self.rpc_password = "cssefd-pass"
		self.rpc_host = "localhost"
		self.amqp_username = "cssefd"
		self.amqp_password = "cssefd-pass"
		self.amqp_host = "localhost"
		# Token configurations
		self.token_auth_enabled = True
		self.token = ''
		self.token_file = os.path.expanduser("~/.cssef/token")
		self.token_repoll_enabled = False
		# Endpoint caching
		self.endpoint_cache_enabled = True
		self.endpoint_cache_file = os.path.expanduser("~/.cssef/endpoint-cache")
		self.endpoint_cache_timeout = '12h'
		# dksl;afjdksl;fjdkls;afjdk;sa
		self.apiConn = None

	def loadConfigFile(self, configPath):
		"""
		This will convert strings with hyphens (-) to underscores (_) that way
		attributes can be added. Underscores are not used in the config files
		because I think they look ugly. That's my only reasoning - deal with it.
		"""
		configDict = yaml.load(open(configPath, 'r'))
		self.loadConfigDict(configDict)

	def loadConfigDict(self, configDict):
		for i in configDict:
			if hasattr(self, i.replace('-','_')):
				# Set the attribute
				setting = i.replace('-','_')
				value = configDict[i]
				setattr(self, setting, value)
				print "[LOGGING] Configuration '%s' set to '%s'." % (i, value)
			elif type(configDict[i]) == dict:
				# This is a dictionary and may contain additional values
				self.loadConfigDict(configDict[i])
			else:
				# We don't care about it. Just skip it!
				print "[LOGGING] Ignoring invalid setting '%s'." % i

	def loadToken(self):
		try:
			token = open(self.token_file, 'r').read()
			if len(token) > 0:
				self.token = token
			else:
				print "[LOGGING] Token file empty. Cannot use token authentication."
		except IOError:
			print "[LOGGING] Token file not found. Cannot use token authentication."

	def establishApiConnection(self):
		"""Establishes a connection to the celery server

		Returns:
			This will return an instance of Celery, which is connected to the
			server specified in the provided Configuration object. This Celery
			object can be provided to CeleryEndpoint object to execute a task.
		"""
		rpcUrl = "rpc://%s:%s@%s//" % (self.rpc_username, self.rpc_password, self.rpc_host)
		amqpUrl = "amqp://%s:%s@%s//" % (self.amqp_username, self.amqp_password, self.amqp_host)
		self.apiConn = Celery('api', backend = rpcUrl, broker = amqpUrl)

class Argument(object):
	def __init__(self, displayName, name = None, keyword = False, optional = False):
		self.displayName = displayName
		if not name:
			self.name = self.displayName.lower()
		else:
			self.name = name
		self.keyword = keyword
		self.optional = optional

	def helpFormat(self, *args, **kwargs):
		return '--%s' % self.name

class CeleryEndpoint(object):
	"""Base class to represent a celery task on the server.
	 
	This class gets subclassed by other classes to define a specific
	task on the cssef server.
	"""
	def __init__(self, config, celeryName, args):
		"""
		Args:
			celeryName (str): The task name as defined by the celery server
			args (list): Arguments that are available to the task

		Attributes:
			apiConn (None): This is an empty value to hold the celery server
				connection
			celeryName (str):
			args (list):
		"""
		self.config = config
		self.celeryName = celeryName
		self.args = args

	@classmethod
	def fromDict(cls, config, inputDict):
		"""Creates a CeleryEndpoint object from a dictionary

		Args:
			inputDict (dict): Dictionary containing necessary values to define
				the celery endpoint
			apiConn (Celery): The celery server connection to use to execute
				the request

		Returns:
			An instance of CeleryEndpoint that has been filled with the
			information defined in the provided dictionary is returned.

		Example:
			<todo>
		"""
		args = []
		instance = cls(config, inputDict['celeryName'], args)
		instance.name = inputDict['name']
		return instance

	def execute(self, *args, **kwargs):
		"""Calls the celery task on the remote server

		Args:
			*args: Arguments to pass to the celery task on the server.
			**kwargs: Keyword arguments to pass to the celery task on the
				server.

		Returns:
			The task data is returned as it's provided. Cssef tasks should
			always return a standard dictionary object. TODO: Maybe force some
			checking here to cast anything that does not comply into that
			dictionary.
		"""
		task = self.config.apiConn.send_task(self.celeryName, args = args, kwargs = kwargs)
		return task.get()

############################################
# General endpoints
############################################
class AvailableEndpoints(CeleryEndpoint):
	def __init__(self, config):
		"""Instiantiates a new instance of AvailableEndpoints.
 
		This is hardcoded because this task/endpoint will be available on all
		configurations of the server.
		
		Args:
			apiConn (Celery): A connection object to the celery server.
		Attributes:
			apiConn (Celery): The celery connection to use
			celeryName (str): The task name to call through Celery
			args (list): The required arguments while calling the celery task
		"""
		self.config = config
		self.celeryName = 'availableEndpoints'
		self.args = []

class Login(CeleryEndpoint):
	def __init__(self, config):
		self.celeryName = 'login'
		self.args = []
		self.config = config

	def execute(self, **kwargs):
		if not self.config.token_auth_enabled:
			# Bail if token authentication is disabled
			print "[ERROR] Logging in requires that token authentication be \
				enabled. Set 'token_auth_enabled: True' in your \
				configuration."
			return None
		# Attempt to log in
		returnDict = super(Login, self).execute(**kwargs)
		if returnDict['value'] != 0:
			return returnDict
		# Save the returned token
		open(self.config.token_file, 'w').write(returnDict['content'][0])
		returnDict['content'] = ["Authentication was successful."]
		return returnDict

class Logout(CeleryEndpoint):
	def __init__(self, config):
		self.celeryName = 'logout'
		self.args = []
		self.config = config

	def execute(self):
		pass