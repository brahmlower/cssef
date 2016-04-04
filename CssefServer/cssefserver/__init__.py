import os
import os.path
import logging
from celery import Celery
from celery.bin import worker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelbase import Base
from utils import Configuration

from cssefserver.tasks import *
from cssefserver.account.tasks import *
from cssefserver.account.tasks import *

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

		# List of celery task modules
		self.celeryTaskList = []

		# This is the worker instance
		self.celeryWorker = None

		# This is the connection to the message passing queue
		self.celeryApp = None

	def loadCeleryTasks(self):
		# start with the framework tasks. These are hardcoded because they
		# will always be here!
		#self.celeryTaskList.append('cssefserver.tasks.CssefTasks')
		#self.celeryTaskList.append('cssefserver.account.tasks')

		# Import the listed available plugins
		# if self.config.installed_plugins:
		# 	for moduleName in self.config.installed_plugins:
		# 		self.celeryTaskList.append("%s.tasks" % moduleName)
		pass

	def prepareLogging(self):
		# I don't really know what's going on here. Making an issue to fix this later
		logger, handler = configureLogger(self.config)

	def createDatabaseConnection(self):
		"""Returns a database session for the specified database"""
		# We're importing the plugin models to make sure they get synced
		# when the database is instantiated. I don't think this is the
		# best place for this though
		if self.config.installed_plugins:
			for moduleName in self.config.installed_plugins:
				__import__("%s.models" % moduleName)

		# Now actually create the database instantiation
		databaseEngine = create_engine('sqlite:///' + self.config.database_path)
		Base.metadata.create_all(databaseEngine)
		Base.metadata.bind = databaseEngine
		DatabaseSession = sessionmaker(bind = databaseEngine)
		self.databaseConnection = DatabaseSession()
		return self.databaseConnection

	def createCeleryConnection(self, queue = None, backend = None, broker = None, include = None):
		if not queue:
			queue = self.config.celery_queue
		if not backend:
			backend = self.config.rpc_url
		if not broker:
			broker = self.config.amqp_url
		if not include:
			include = self.celeryTaskList
		self.celeryApp = Celery(queue, backend = backend, broker = broker, include = include)
		return self.celeryApp

	def start(self):
		self.loadCeleryTasks()
		self.createDatabaseConnection()
		self.createCeleryConnection()
		self.celeryWorker = worker.worker(app = self.celeryApp)
		self.celeryWorker.run(**self.config.getCeleryOptions())

# Dumpy old logging methods
def makeLogFiles(config):
	files = [
		config.cssef_stderr,
		config.cssef_stdout,
		config.celery_stderr,
		config.celery_stdout]

	# Now create the log files within that directory
	for i in files:
		# Get the directory the file should be in
		log_directory = "/".join(i.split('/')[:-1])
		if not os.path.exists(log_directory):
			os.makedirs(log_directory)
		# Now create the files in that directory
		if not os.path.isfile(i):
			open(i, 'a').close()

def configureLogger(config):
	# Make sure the files exist first
	makeLogFiles(config)
	# Set up the loggers (kinda... i suck at this)
	logger = logging.getLogger("CssefDaemonLog")
	logger.setLevel(logging.DEBUG)
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	handler = logging.FileHandler(config.cssef_stdout)
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	return logger, handler

# Import plugins
def importPlugins():
	pluginList = []
	if config.installed_plugins:
		for moduleName in config.installed_plugins:
			pluginList.append(__import__(moduleName))
	return pluginList