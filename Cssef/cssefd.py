#!/usr/bin/python
# To kick off the script, run the following from the python directory:
#   PYTHONPATH=`pwd` python cssefDaemon.py start

import logging
import time
import pkgutil
from daemon import runner
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import engines
from models import Base
from framework.core import getScoringEngine
from framework.core import createScoringEngine
from framework.core import ScoringEngine as ScoringEngineWrapper

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
	enginesModule = 'engines.%s'#.endpoints'
	scoringEngine = getScoringEngine(name = name)
	package = enginesModule % scoringEngine.packageName
	module = __import__(package)
	for i in package.split('.')[1:]:
		module = getattr(module, i)
	return module

def databaseConnection(sqliteFilepath):
	engine = create_engine('sqlite:///' + sqliteFilepath)
	Base.metadata.create_all(engine)
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind = engine)
	return DBSession()

class App():
	def __init__(self):
		self.db = databaseConnection('db.sqlite3')
		self.stdin_path = '/dev/null'
		self.stdout_path = '/var/log/testdaemon/testdaemon.log'
		self.stderr_path = '/var/log/testdaemon/testdaemon.log'
		self.pidfile_path =  '/var/run/testdaemon.pid'
		self.pidfile_timeout = 5
			
	def run(self):
		while True:
			pass

rpcUsername = "guest"
rpcPassword = "guest"
rpcHost = "localhost"
amqpUsername = "guest"
amqpPassword = "guest"
amqpHost = "localhost"
celeryApp = Celery('tasks', backend='rpc://%s:%s@%s//', broker='amqp://%s:%s@%s//')
app = App()

# This daemon should start the celery workers itself. This following link might help with that...
# http://stackoverflow.com/questions/23389104/how-to-start-a-celery-worker-from-a-script-module-main

logger = logging.getLogger("DaemonLog")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("/var/log/testdaemon/testdaemon.log")
handler.setFormatter(formatter)
logger.addHandler(handler)

daemon_runner = runner.DaemonRunner(app)
#This ensures that the logger file handle does not get closed during daemonization
daemon_runner.daemon_context.files_preserve=[handler.stream]
daemon_runner.do_action()