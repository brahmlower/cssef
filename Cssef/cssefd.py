#!/usr/bin/python
# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python cssefDaemon.py start
from __future__ import absolute_import
import logging
import time
import atexit
import os.path
import pkgutil
import ConfigParser
from daemon import runner
from time import sleep
#from celery import Celery
from celery.bin import worker

import engines

from framework.core import getScoringEngine
from framework.core import createScoringEngine
from framework.core import ScoringEngine as ScoringEngineWrapper
from api import celeryApp
from framework.utils import databaseConnection

def createEngineModules(self):
	package = engines
	for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
		try:
			#scoringEngineEntry = getScoringEngine(packageName = modname)
			mod = importScoringEngine(modname)
			mod.run()
		except OperationalError:
			return None
		except ScoringEngineWrapper.ObjectDoesNotExist:
			createScoringEngine({'name': modname, 'packageName': modname})
			mod = importScoringEngine(modname)
			mod.run()

def importScoringEngine(name):
	enginesModule = 'engines.%s'
	scoringEngine = getScoringEngine(name = name)
	package = enginesModule % scoringEngine.packageName
	module = __import__(package)
	for i in package.split('.')[1:]:
		module = getattr(module, i)
	return module

class CssefDaemon(object):
	def __init__(self):
		# Prepare logging information
		# Required by python-daemon
		self.stdin_path = '/dev/null'
		self.stdout_path = config.rawConfig.get('logging', 'cssef_stdout')
		self.stderr_path = config.rawConfig.get('logging', 'cssef_stderr')
		#self.pidfile_path = '/var/run/cssefd.pid'
		self.pidfile_path = '/home/sk4ly/Documents/cssef/Cssef/cssefd.pid'
		self.pidfile_timeout = 5
		self.celeryWorker = None

	def run(self):
		celeryOptions = {
			'broker': config.amqpUrl,
			'backend': config.rpcUrl,
			'loglevel': 'DEBUG',
			'logfile': config.rawConfig.get('logging', 'celery_stdout'),
			'traceback': True
		}
		atexit.register(self.stop)
		self.celeryWorker = worker.worker(app = celeryApp)
		self.celeryWorker.run(**celeryOptions)

	def stop(self):
		del(self.celeryWorker)
		engines = reload(engines)
		getScoringEngine = reload(getScoringEngine)
		createScoringEngine = reload(createScoringEngine)
		ScoringEngineWrapper = reload(ScoringEngineWrapper)
		celeryApp = reload(celeryApp)
		databaseConnection = reload(databaseConnection)

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

def configureLoggingFiles():
	files = [
		config.rawConfig.get('logging', 'cssef_stderr'),
		config.rawConfig.get('logging', 'cssef_stdout'),
		config.rawConfig.get('logging', 'celery_stderr'),
		config.rawConfig.get('logging', 'celery_stdout')]
	for i in files:
		if not os.path.isfile(i):
			open(i, 'a').close()

def configureLogger():
	# Get the logger started ASAP
	logger = logging.getLogger("CssefDaemonLog")
	logger.setLevel(logging.DEBUG)
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	handler = logging.FileHandler(config.rawConfig.get('logging', 'cssef_stdout'))
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	return logger, handler

if __name__ == "__main__":
	config = Configuration('cssef.conf')
	configureLoggingFiles()
	logger, handler = configureLogger()
	#db = databaseConnection('db.sqlite3')

	daemonRunner = runner.DaemonRunner(CssefDaemon())
	#This ensures that the logger file handle does not get closed during daemonization
	daemonRunner.daemon_context.files_preserve = [handler.stream]
	daemonRunner.do_action()