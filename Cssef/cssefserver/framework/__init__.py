from celery import Celery
from utils import Configuration

config = Configuration()
config.loadConfigFile(config.globalConfigPath)
DatabaseConnection = config.establishDatabaseConnection()
CssefCeleryApp = Celery('api', backend = config.rpc_url, broker = config.amqp_url)