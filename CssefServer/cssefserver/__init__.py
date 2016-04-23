import os
import os.path
import logging
# RPC Server related imports
from flask import Flask
from flask import request
from flask import Response
from jsonrpcserver import dispatch
from jsonrpcserver import Methods
# Local imports
from .utils import Configuration
from .utils import createDatabaseConnection
from .account import tasks as accountTasks
import tasks as baseTasks

class CssefServer(object):
	def __init__(self):
		self.config = Configuration()
		# TODO: Idealy we would load configs from multiple source,
		# but we'll add that functionality later on...
		self.config.loadConfigFile(self.config.globalConfigPath)

		# THIS IS SUPER TEMPORARY!
		self.prepareLogging()
		
		# This is the database connection
		self.databaseConnection = None

		# Methods object to pass to the dispatcher when a request is handled
		self.rpcMethods = Methods()

		# The flask instance that handles incoming networking requests
		self.flaskApp = None

	def loadRpcEndpoints(self):
		endpointList = [
			(baseTasks.AvailableEndpoints, 'AvailableEndpoints'),
			(baseTasks.RenewToken, 'RenewToken'),
			(baseTasks.Login, 'Login'),
			(accountTasks.OrganizationAdd, 'organizationAdd'),
			(accountTasks.OrganizationDel, 'organizationDel'),
			(accountTasks.OrganizationSet, 'organizationSet'),
			(accountTasks.OrganizationGet, 'organizationGet'),
			(accountTasks.UserAdd, 'userAdd'),
			(accountTasks.UserDel, 'userDel'),
			(accountTasks.UserSet, 'userSet'),
			(accountTasks.UserGet, 'userGet')]
		for reference, name in endpointList:
			# I'm creating and storing an instance of every since endpoint...
			self.rpcMethods.add_method(reference(self.config, self.databaseConnection), name)

	def prepareLogging(self):
		pass
		# # I don't really know what's going on here. Making an issue to fix this later
		# # Make sure the files exist first
		# makeLogFiles(self.config)
		# # Set up the loggers (kinda... i suck at this)
		# logger = logging.getLogger("CssefDaemonLog")
		# logger.setLevel(logging.DEBUG)
		# formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
		# if self.config.cssef_stdout != '':
		# 	handler = logging.FileHandler(self.config.cssef_stdout)
		# 	handler.setFormatter(formatter)
		# 	logger.addHandler(handler)

	def start(self):
		self.databaseConnection = createDatabaseConnection(self.config)
		self.loadRpcEndpoints()
		self.flaskApp = Flask(__name__)
		self.flaskApp.add_url_rule('/', 'index', self.index, methods = ['POST'])
		# This next line can throw a permissions error:
		# IOError: [Errno 13] Permission denied: '/var/log/cssef/error.log'
		# This should be caught and handleds, and possibly reported to the daemon?
		logging.basicConfig(filename='/var/log/cssef/error.log',level=logging.DEBUG)
		self.flaskApp.run(debug = False)

	# This function shouldn't live here forever
	def index(self):
		r = dispatch(self.rpcMethods, request.get_data().decode('utf-8'))
		return Response(str(r), r.http_status, mimetype = 'application/json')

# Dumpy old logging methods
def makeLogFiles(config):
	# Now create the log files within that directory
	files = [config.cssef_stderr, config.cssef_stdout]
	for i in files:
		if i == '':
			continue
		# Get the directory the file should be in
		log_directory = "/".join(i.split('/')[:-1])
		if not os.path.exists(log_directory):
			os.makedirs(log_directory)
		# Now create the files in that directory
		if not os.path.isfile(i):
			open(i, 'a').close()

# Import plugins
def importPlugins(config):
	pluginList = []
	if config.installed_plugins:
		for moduleName in config.installed_plugins:
			pluginList.append(__import__(moduleName))
	return pluginList