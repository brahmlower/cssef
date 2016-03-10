import sys
from time import sleep
from celery import Celery
import ConfigParser

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
	return Celery(
		'api',
		backend = config.rpcUrl,
		broker = config.amqpUrl)

class Configuration(object):
	def __init__(self, configFilePath):
		self.rawConfig = ConfigParser.ConfigParser()
		self.rawConfig.read(configFilePath)

	@property
	def amqpUrl(self):
		username = self.rawConfig.get('celery', 'amqp_username')
		password = self.rawConfig.get('celery', 'amqp_password')
		host = self.rawConfig.get('celery', 'amqp_host')
		return 'amqp://%s:%s@%s//' % (username, password, host)

	@property
	def rpcUrl(self):
		username = self.rawConfig.get('celery', 'rpc_username')
		password = self.rawConfig.get('celery', 'rpc_password')
		host = self.rawConfig.get('celery', 'rpc_host')
		return 'rpc://%s:%s@%s//' % (username, password, host)

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

	def __init__(self, celeryName, args):
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
		self.apiConn = None
		self.celeryName = celeryName
		self.args = args

	@classmethod
	def fromDict(cls, inputDict, apiConn):
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
		# Parse the arguments
		args = []
		#for i in inputDict['arguments']:
		#	pass
		# Now create the instance
		instance = cls(inputDict['celeryName'], args)
		instance.name = inputDict['name']
		instance.apiConn = apiConn
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
		task = self.apiConn.send_task(
			self.celeryName,
			args = args,
			kwargs = kwargs)
		return task.get()

class ServerEndpoints(object):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		result = AvailableEndpoints(self.apiConn).execute()
		if result['value'] != 0:
			raise Exception
		for i in result['content']:
			for k in i['endpoints']:
				instance = CeleryEndpoint.fromDict(k, self.apiConn)
				setattr(self, k['celeryName'], instance)

############################################
# General endpoints
############################################
class AvailableEndpoints(CeleryEndpoint):
	def __init__(self, apiConn):
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
		self.apiConn = apiConn
		self.celeryName = 'availableEndpoints'
		self.args = []