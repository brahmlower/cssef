from celery import Celery
from utils import Configuration


# Build the initial configuration
config = Configuration()
config.loadConfigFile(config.globalConfigPath)

# Establish a database connection to use
DatabaseConnection = config.establishDatabaseConnection()

# Build a list of available endpoints
celeryTasks = []
celeryTasks.append('cssefserver.framework.api')
celeryTasks.append('cssefserver.modules.account.api')

plugins = []

# Import the listed available plugins
for moduleName in config.installed_plugins:
	celeryTasks.append("%s.tasks" % moduleName)
	plugins.append(__import__(moduleName))

# Start the celery app
CssefCeleryApp = Celery('api', backend = config.rpc_url, broker = config.amqp_url, include = celeryTasks)