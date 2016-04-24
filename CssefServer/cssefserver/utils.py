import os
import abc
import yaml
import traceback
import logging
# Database related imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .modelbase import Base
from .errors import CssefException
from .errors import IncorrectCredentials

class Configuration(object):
    """Contains and loads server configuration values

    There is one attribute for each configuration that can be set.
    Configurations can be loaded from a file or dictionary. When loading
    configurations, any hyphens wihtin key values will be converted to
    underscores so that the attribute can be set.
    """
    def __init__(self):
        # Super global configs
        self.globalConfigPath = "/etc/cssef/cssefd.yml"
        self.admin_token = ""
        self.pidfile = ""
        # SQLAlchemy configurations
        self.database_table_prefix = "cssef_"
        self.database_path = None
        # General configurations
        self.verbose = False
        self.auth_failover = True
        # Logging configurations
        self.cssef_loglevel = ""
        self.cssef_stderr = ""
        self.cssef_stdout = ""
        self.celery_loglevel = ""
        self.celery_stderr = ""
        self.celery_stdout = ""
        # Plugin configurations
        self.installed_plugins = []

    def loadConfigFile(self, configPath):
        """Load configuration from a file

        This will read a yaml configuration file. The yaml file is converted
        to a dictionary object, which is just passed to `loadConfigDict`.

        Args:
            configPath (str): A filepath to the yaml config file

        Returns:
            None
        """
        try:
            configDict = yaml.load(open(configPath, 'r'))
        except IOError:
            print "[WARNING] Failed to load config file at '%s'." % configPath
            return
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

class CssefRPCEndpoint(object):
    takesKwargs = True
    onRequestArgs = []
    def __init__(self, config, databaseConnection):
        self.config = config
        self.databaseConnection = databaseConnection

    def __call__(self, **kwargs):
        argsList = []
        # This builds the list of arguments we were told are expected
        # by the overloaded onRequest() method
        for i in self.onRequestArgs:
            argsList.append(kwargs.get(i))
        for i in self.onRequestArgs:
            try:
                kwargs.pop(i)
            except KeyError:
                x = getEmptyReturnDict()
                x['value'] = 1
                x['message'] = "Missing required argument '%s'." % i
                return x
        print kwargs
        # Now call the onRequest method that actually handles the request.
        # Here we're determining if we should pass it kwargs or not (the
        # subclass tells us yes or no). This is surrounded by a catch
        # to handle various errors that may crop up
        try:
            if self.takesKwargs:
                return self.onRequest(*argsList, **kwargs)
            else:
                return self.onRequest(*argsList)
        except CssefException as e:
            return e.asReturnDict()
        except Exception as e:
            return handleException(e)

    @abc.abstractmethod
    def onRequest(self, *args, **kwargs):
        pass

class CssefObjectDoesNotExist(Exception):
    'An exception for when the requested object does not exist - not needed I think'
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)

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
                # We'll try to find it in the classes model
                tmpDict[i] = getattr(self.model, i)
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

def createDatabaseConnection(config):
    """Returns a database session for the specified database"""
    # We're importing the plugin models to make sure they get synced
    # when the database is instantiated. I don't think this is the
    # best place for this though
    if config.installed_plugins:
        for moduleName in config.installed_plugins:
            __import__("%s.models" % moduleName)

    # Now actually create the database instantiation
    databaseEngine = create_engine('sqlite:///' + config.database_path)
    Base.metadata.create_all(databaseEngine)
    Base.metadata.bind = databaseEngine
    DatabaseSession = sessionmaker(bind = databaseEngine)
    return DatabaseSession()

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