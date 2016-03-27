from celery import Celery
from utils import Configuration
from models import establishDatabaseConnection

# We need to build the configuration object before importing a few objects,
# since they rely on it VERY heavily
config = Configuration()
config.loadConfigFile(config.globalConfigPath)

from modelbase import Base
from cssefserver.account import models

# Import the listed available plugins
if config.installed_plugins:
	for moduleName in config.installed_plugins:
		__import__("%s.models" % moduleName)

# Establish a database connection to use
DatabaseConnection = establishDatabaseConnection()

# Build a list of available endpoints
celeryTasks = []
celeryTasks.append('cssefserver.tasks')
celeryTasks.append('cssefserver.account.tasks')

plugins = []

# Import the listed available plugins
if config.installed_plugins:
	for moduleName in config.installed_plugins:
		celeryTasks.append("%s.tasks" % moduleName)
		plugins.append(__import__(moduleName))

# Start the celery app
CssefCeleryApp = Celery('api', backend = config.rpc_url, broker = config.amqp_url, include = celeryTasks)