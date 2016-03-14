import os
import sys
import stat
from time import sleep
from getpass import getpass
import yaml
from celery import Celery

versionMajor = '0'
versionMinor = '0'
versionPatch = '3'
version = ".".join([versionMajor, versionMinor, versionPatch])

class Configuration(object):
	"""Contains and loads configuration values

	There is one attribute for each configuration that can be set.
	Configurations can be loaded from a file or dictionary. When loading
	configurations, any hyphens wihtin key values will be converted to
	underscores so that the attribute can be set.
	"""
	def __init__(self):
		# Super global configs
		self.globalConfigPath = "/etc/cssef/cssef.yml"
		self.userDataDir = os.path.expanduser("~/.cssef/")
		self.configPath = self.userDataDir + "cssef.yml"
		# General configurations
		self.verbose = False
		self.organization = None
		self.username = None
		self.password = None
		# Default values for the client configuration
		self.rpc_username = "cssefd"
		self.rpc_password = "cssefd-pass"
		self.rpc_host = "localhost"
		self.amqp_username = "cssefd"
		self.amqp_password = "cssefd-pass"
		self.amqp_host = "localhost"
		# Token configurations
		self.token_auth_enabled = True
		self.token = None
		self.token_file = self.userDataDir + "token"
		self.token_repoll_enabled = False
		# Endpoint caching
		self.endpoint_cache_enabled = True
		self.endpoint_cache_file = self.userDataDir + "endpoint-cache"
		self.endpoint_cache_timeout = '12h'
		# dksl;afjdksl;fjdkls;afjdk;sa
		self.apiConn = None

		# Ensure user data directory exists
		if not os.path.exists(self.userDataDir):
			os.makedirs(self.userDataDir)

	def loadConfigFile(self, configPath):
		"""Load configuration from a file

		This will read a yaml configuration file. The yaml file is converted
		to a dictionary object, which is just passed to `loadConfigDict`.

		Args:
			configPath (str): A filepath to the yaml config file

		Returns:
			None
		"""
		configDict = yaml.load(open(configPath, 'r'))
		self.loadConfigDict(configDict)

	def loadConfigDict(self, configDict):
		"""Load configurations from a dictionary

		This will convert strings with hyphens (-) to underscores (_) that way
		attributes can be added. Underscores are not used in the config files
		because I think they look ugly. That's my only reasoning - deal with
		it. Any key within the dictionary that is not an attribute of the
		class will be ignored (this will be logged).

		Args:
			configDict (dict): A dictionary containing configurations and
				values

		Returns:
			None
		"""
		for i in configDict:
			if hasattr(self, i.replace('-','_')):
				# Set the attribute
				setting = i.replace('-','_')
				value = configDict[i]
				setattr(self, setting, value)
				if self.verbose:
					print "[LOGGING] Configuration '%s' set to '%s'." % (i, value)
			elif type(configDict[i]) == dict:
				# This is a dictionary and may contain additional values
				self.loadConfigDict(configDict[i])
			else:
				# We don't care about it. Just skip it!
				if self.verbose:
					print "[LOGGING] Ignoring invalid setting '%s'." % i

	def loadTokenFile(self):
		"""Load token from a file

		This will try to load the token from the token cache file. If
		successful, it will save the token it finds in the `token` attribute
		for use while sending requests to the server.

		Returns:
			bool: True if token was successfully loaded, otherwise False.
		"""
		# Make sure the file exists
		if not os.path.isfile(self.token_file):
			sys.stderr.write("[WARNING] Token file not found. Cannot use \
				token authentication.")
			sys.stderr.flush()
		# Now make sure that only we have access to it
		filePermissions = os.stat(self.token_file).st_mode
		permissionsDenied = [stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP,
			stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH]
		for i in permissionsDenied:
			if bool(filePermissions & i):
				sys.stderr.write("Token file may not have any permissions for group or other.\n")
				sys.stderr.flush()
				return False
		# Now actually read in the file
		token = open(self.token_file, 'r').read()
		if len(token) > 0:
			self.token = token
			return True
		else:
			if self.verbose:
				print "[LOGGING] Token file empty. Cannot use token authentication."

	def establishApiConnection(self):
		"""Establishes a connection to the celery server

		This sets the attribute `apiConn` to an open connection to the Celery
		server, based on the settings. This connection can be provided to a
		`CeleryEndpoint` to execute a task
		"""
		queueName = 'api' # We're going to have to improve this some day
		rpcUrl = "rpc://%s:%s@%s//" % (self.rpc_username, self.rpc_password, self.rpc_host)
		amqpUrl = "amqp://%s:%s@%s//" % (self.amqp_username, self.amqp_password, self.amqp_host)
		self.apiConn = Celery(queueName, backend = rpcUrl, broker = amqpUrl)

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
			config (Configuration): The current configuration to use
			celeryName (str): The task name as defined by the celery server
			args (list): Arguments that are available to the task

		Attributes:
			config (Configuration): The current configuration to use
			celeryName (str): The task name as defined by the celery server
			args (list): Arguments that are available to the task
		"""
		self.config = config
		self.celeryName = celeryName
		self.args = args

	@classmethod
	def fromDict(cls, config, inputDict):
		"""Creates a CeleryEndpoint object from a dictionary

		Args:
			config (Configuration): The current configuration to use
			inputDict (dict): Dictionary containing necessary values to define
				the celery endpoint

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
		if returnDict['value'] != 0:
			return returnDict
		# Save the returned token
		os.chmod(self.config.token_file, stat.S_IRUSR | stat.S_IWUSR)
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