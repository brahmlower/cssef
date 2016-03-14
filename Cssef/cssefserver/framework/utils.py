import os
import yaml
import traceback
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cssefserver.framework.models import Base

class CssefObjectDoesNotExist(Exception):
	'An exception for when the requested object does not exist - not needed I think'
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return repr(self.message)

class Configuration(object):
	"""Contains and loads server configuration values

	There is one attribute for each configuration that can be set.
	Configurations can be loaded from a file or dictionary. When loading
	configurations, any hyphens wihtin key values will be converted to
	underscores so that the attribute can be set.
	"""
	def __init__(self):
		print "Making config object!"
		# Super global configs
		self.globalConfigPath = "/etc/cssef/cssefd.yml"
		self.admin_token = ""
		self.pidfile = ""
		# SQLAlchemy configurations
		self.database_table_prefix = "cssef_"
		self.database_path = None
		# General configurations
		self.verbose = False
		# Default values for the rabbitmq configuration
		self.rpc_username = "cssefd"
		self.rpc_password = "cssefd-pass"
		self.rpc_host = "localhost"
		self.amqp_username = "cssefd"
		self.amqp_password = "cssefd-pass"
		self.amqp_host = "localhost"
		# Logging configurations
		self.cssef_loglevel = ""
		self.cssef_stderr = ""
		self.cssef_stdout = ""
		self.celery_loglevel = ""
		self.celery_stderr = ""
		self.celery_stdout = ""

	@property
	def rpc_url(self):
		return "rpc://%s:%s@%s//" % (self.rpc_username, self.rpc_password, self.rpc_host)

	@property
	def amqp_url(self):
		return "amqp://%s:%s@%s//" % (self.amqp_username, self.amqp_password, self.amqp_host)

	def loadConfigFile(self, configPath):
		"""Load configuration from a file

		This will read a yaml configuration file. The yaml file is converted
		to a dictionary object, which is just passed to `loadConfigDict`.

		Args:
			configPath (str): A filepath to the yaml config file

		Returns:
			None
		"""
		configDict = yaml.load(open(configPath, 'r'))
		self.loadConfigDict(configDict)

	def loadConfigDict(self, configDict):
		"""Load configurations from a dictionary

		This will convert strings with hyphens (-) to underscores (_) that way
		attributes can be added. Underscores are not used in the config files
		because I think they look ugly. That's my only reasoning - deal with
		it. Any key within the dictionary that is not an attribute of the
		class will be ignored (this will be logged).

		Args:
			configDict (dict): A dictionary containing configurations and
				values

		Returns:
			None
		"""
		for i in configDict:
			if hasattr(self, i.replace('-','_')):
				# Set the attribute
				setting = i.replace('-','_')
				value = configDict[i]
				setattr(self, setting, value)
				if self.verbose:
					print "[LOGGING] Configuration '%s' set to '%s'." % (i, value)
			elif type(configDict[i]) == dict:
				# This is a dictionary and may contain additional values
				self.loadConfigDict(configDict[i])
			else:
				# We don't care about it. Just skip it!
				if self.verbose:
					print "[LOGGING] Ignoring invalid setting '%s'." % i

	def establishApiConnection(self):
		"""Establishes a connection to the celery server

		This sets the attribute `apiConn` to an open connection to the Celery
		server, based on the settings. This connection can be provided to a
		`CeleryEndpoint` to execute a task
		"""
		queueName = 'api' # We're going to have to improve this some day
		self.apiConn = Celery(queueName, backend = self.rpc_url, broker = self.amqp_url)

	def establishDatabaseConnection(self):
		'Returns a database session for the specified database'
		dbEngine = create_engine('sqlite:///' + self.database_path)
		Base.metadata.create_all(dbEngine)
		Base.metadata.bind = dbEngine
		DBSession = sessionmaker(bind = dbEngine)
		return DBSession()

class ModelWrapper(object):
	""" The base class for wrapping SQLAlchemy model objects

	This class provides utilities for interacting with SQLAlchemy models
	in a clean manner. This should be subclassed by any other objects that
	will need to wrap a SQLAlchemy model object.
	"""
	class ObjectDoesNotExist(CssefObjectDoesNotExist):
		def __init__(self, message):
			self.message = message

		def __str__(self):
			return repr(self.message)

	modelObject = None
	fields = None

	def __init__(self, db, model):
		self.db = db
		self.model = model

	def getId(self):
		return self.model.pkid

	def edit(self, **kwargs):
		for i in kwargs:
			if i in self.fields:
				setattr(self, i, kwargs[i])

	def delete(self):
		self.db.delete(self.model)
		self.db.commit()

	def asDict(self):
		tmpDict = {}
		tmpDict['id'] = self.getId()
		for i in self.fields:
			try:
				tmpDict[i] = getattr(self, i)
			except AttributeError:
				# The field is not an attribute of the subclassed model wrapper
				# We'll try to find it in the classes modesl
				tmpDict[i] = getattr(self.mode, i)
		return tmpDict

	@classmethod
	def count(cls, db, **kwargs):
		return db.query(cls.modelObject).filter_by(**kwargs).count()

	@classmethod
	def search(cls, db, **kwargs):
		modelObjectList = db.query(cls.modelObject).filter_by(**kwargs)
		clsList = []
		for i in modelObjectList:
			clsList.append(cls(db, i))
		return clsList

	@classmethod
	def fromDatabase(cls, db, pkid):
		try:
			return cls.search(db, pkid = pkid)[0]
		except IndexError:
			return None

	@classmethod
	def fromDict(cls, db, kwDict):
		modelObjectInst = cls.modelObject()
		clsInst = cls(db, modelObjectInst)
		for i in kwDict:
			if i in clsInst.fields:
				setattr(clsInst, i, kwDict[i])
		db.add(clsInst.model)
		db.commit()
		return clsInst

def returnError(errorName, *args):
	returnDict = getEmptyReturnDict()
	if errorName == 'multiple_users_found':
		returnDict['value'] = 1
		returnDict['message'] = ["Multiple users returned by search:", args]
	elif errorName == 'no_user_provided':
		returnDict['value'] = 1
		returnDict['message'] = ["No username provided."]
	elif errorName == 'no_organization_provided':
		returnDict['value'] = 1
		returnDict['message'] = ["No organization provided."]
	elif errorName == 'user_not_found':
		returnDict['value'] = 1
		returnDict['message'] = ["Unable to find user object."]
	elif errorName == 'user_auth_failed':
		returnDict['value'] = 1
		returnDict['message'] = ["Authentication failed."]
	elif errorName == 'user_permission_denied':
		returnDict['value'] = 1
		returnDict['message'] = ["Permission is denied."]
	else:
		returnDict['value'] = 1
		returnDict['message'] = ["General undefined error."]
	return returnDict

def handleException(e):
	# todo
	# log the full stacktrace!
	returnDict = getEmptyReturnDict()
	returnDict['value'] = 1
	returnDict['message'] = traceback.format_exc().splitlines()
	return returnDict

def getEmptyReturnDict():
	return {
		'value': 0,
		'message': 'Success',
		'content': []
	}

def modelDel(cls, pkid):
	config = Configuration()
	config.loadConfigFile(config.globalConfigPath)
	db = config.establishDatabaseConnection()
	if pkid == "*":
		# todo: implement a wildcard
		returnDict = getEmptyReturnDict()
		returnDict['value'] = 1
		returnDict['message'] = ["Wildcards are not implemented yet."]
		return returnDict
	elif type(pkid) == str and "-" in pkid:
		x = pkid.split("-")
		if len(x) == 2:
			try:
				for pkid in range(int(x[0]), int(x[1])+1):
					modelObj = cls.fromDatabase(db, pkid)
					if modelObj:
						modelObj.delete()
			except ValueError:
				# One of the ranges provided could not be cast as an integer. Return error.
				returnDict = getEmptyReturnDict()
				returnDict['value'] = 1
				returnDict['message'] = ["Range value could not be cast to integer. Expected integer range like 1-4. Got '%s' instead." % pkid]
				return returnDict
		else:
			print x
			returnDict = getEmptyReturnDict()
			returnDict['value'] = 1
			returnDict['message'] = ["Expected integer range like 1-4. Got '%s' instead." % pkid]
			return returnDict
	elif type(pkid) == int:
		modelObj = cls.fromDatabase(db, pkid)
		modelObj.delete()
	else:
		# We don't know what the hell we were given. Disregard it and thow an error :(
		returnDict = getEmptyReturnDict()
		returnDict['value'] = 1
		returnDict['message'] = ["Expected integer value (5) or range (2-7). Got '%s' of type %s instead." % (str(pkid), str(type(pkid)))]
	return getEmptyReturnDict()

def modelSet(cls, pkid, **kwargs):
	config = Configuration()
	config.loadConfigFile(config.globalConfigPath)
	db = config.establishDatabaseConnection()
	modelObj = cls.fromDatabase(db, pkid)
	modelObj.edit(**kwargs)
	returnDict = getEmptyReturnDict()
	returnDict['content'].append(modelObj.asDict())
	return returnDict

def modelGet(cls, **kwargs):
	config = Configuration()
	config.loadConfigFile(config.globalConfigPath)
	db = config.establishDatabaseConnection()
	modelObjs = cls.search(db, **kwargs)
	returnDict = getEmptyReturnDict()
	for i in modelObjs:
		returnDict['content'].append(i.asDict())
	return returnDict