import sys
from time import sleep
from celery import Celery
import ConfigParser

versionMajor = '0'
versionMinor = '0'
versionPatch = '3'
version = ".".join([versionMajor, versionMinor, versionPatch])

def getConn(config):
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

class Endpoint(object):
	def __init__(self, name):
		self.name = name.lower()
		self.args = []

	def help(self, *args, **kwargs):
		helpRows = []
		helpRows.append('Endpoint: %s' % self.name)
		for i in self.args:
			helpRows.append(i.helpFormat(*args, **kwargs))
		return helpRows

class CeleryEndpoint(Endpoint):
	def __init__(self, celeryName, args):
		#super(CeleryEndpoint, self).__init__(self, celeryName)
		self.apiConn = None
		self.celeryName = celeryName
		self.args = args

	@classmethod
	def fromDict(cls, inputDict, apiConn):
		# Parse the arguments
		args = []
		for i in inputDict['arguments']:
			pass
		# Now create the instance
		instance = cls(inputDict['celeryName'], args)
		instance.name = inputDict['name']
		instance.apiConn = apiConn
		return instance

	def execute(self, *args, **kwargs):
		task = self.apiConn.send_task(
			self.celeryName,
			args = args,
			kwargs = kwargs)
		return task.get()

############################################
# General endpoints
############################################
class AvailableEndpoints(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'availableEndpoints'
		self.args = []