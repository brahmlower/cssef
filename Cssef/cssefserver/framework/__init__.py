from celery import Celery
# # Todo: pull the backend url from the config file instead of hardcoding
CssefCeleryApp = Celery(
	'api',
	backend='rpc://cssefd:cssefd-pass@localhost//',
	broker='amqp://cssefd:cssefd-pass@localhost//')

# Todo: pull the sqlite database path from the config file instead of hardcoding
dbPath = '/home/sk4ly/Documents/cssef/Cssef/db.sqlite3'