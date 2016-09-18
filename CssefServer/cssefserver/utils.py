import abc
import traceback
from systemd import journal
import yaml
# Database related imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.exc
from cssefserver.modelbase import BASE as Base
from cssefserver.errors import CssefException
from cssefserver.errors import CssefObjectDoesNotExist

class Configuration(object):
    """Contains and loads server configuration values

    There is one attribute for each configuration that can be set.
    Configurations can be loaded from a file or dictionary. When loading
    configurations, any hyphens wihtin key values will be converted to
    underscores so that the attribute can be set.
    """
    def __init__(self):
        # Super global configs
        self.global_config_path = "/etc/cssef/cssef-server.yml"
        self.admin_token = ""
        # SQLAlchemy configurations
        self.database_table_prefix = "cssef_"
        self.database_path = None
        # General configurations
        self.auth_failover = True
        # Logging configurations
        self.cssef_loglevel = ""
        self.cssef_stderr = ""
        self.cssef_stdout = ""
        # Plugin configurations
        self.installed_plugins = []
        self.endpoint_sources = []

    def load_config_file(self, config_path):
        """Load configuration from a file

        This will read a yaml configuration file. The yaml file is converted
        to a dictionary object, which is just passed to `load_config_dict`.

        Args:
            config_path (str): A filepath to the yaml config file

        Returns:
            None
        """
        try:
            config_dict = yaml.load(open(config_path, 'r'))
        except IOError:
            print "[WARNING] Failed to load configuration file at '%s'." % config_path
            return
        self.load_config_dict(config_dict)

    def load_config_dict(self, config_dict):
        """Load configurations from a dictionary

        This will convert strings with hyphens (-) to underscores (_) that way
        attributes can be added. Underscores are not used in the config files
        because I think they look ugly. That's my only reasoning - deal with
        it. Any key within the dictionary that is not an attribute of the
        class will be ignored (this will be logged).

        Args:
            config_dict (dict): A dictionary containing configurations and
                values

        Returns:
            None
        """
        for i in config_dict:
            if hasattr(self, i.replace('-', '_')):
                # Set the attribute
                setting = i.replace('-', '_')
                value = config_dict[i]
                setattr(self, setting, value)
                journal.send(message="Configuration '%s' set to '%s'." % (i, value))
            elif isinstance(config_dict[i], dict):
                # This is a dictionary and may contain additional values
                self.load_config_dict(config_dict[i])
            else:
                # We don't care about it. Just skip it!
                journal.send(message="Ignoring invalid configuration '%s'." % i)

class CssefRPCEndpoint(object):
    """Base class for RPC endpoints

    This class provides the functionality and utilities to create new RPC
    endpoints, consumable by clients.
    """
    name = None
    rpc_name = None
    menu_path = None
    takesKwargs = True
    onRequestArgs = []
    def __init__(self, config, database_connection):
        self.config = config
        self.database_connection = database_connection

    def __call__(self, **kwargs):
        args_list = []
        # This builds the list of arguments we were told are expected
        # by the overloaded on_request() method
        for i in self.onRequestArgs:
            args_list.append(kwargs.get(i))
        for i in self.onRequestArgs:
            try:
                kwargs.pop(i)
            except KeyError:
                return_dict = get_empty_return_dict()
                return_dict['value'] = 1
                return_dict['message'] = ["Missing required argument '%s'." % i]
                return return_dict
        # Now call the on_request method that actually handles the request.
        # Here we're determining if we should pass it kwargs or not (the
        # subclass tells us yes or no). This is surrounded by a catch
        # to handle various errors that may crop up
        try:
            if self.takesKwargs:
                return self.on_request(*args_list, **kwargs)
            else:
                return self.on_request(*args_list)
        except CssefException as err:
            return err.as_return_dict()
        except Exception as err:
            return handle_exception(err)

    @classmethod
    def info_dict(cls):
        tmp_dict = {}
        tmp_dict['name'] = cls.name
        tmp_dict['rpc_name'] = cls.rpc_name
        tmp_dict['menu_path'] = cls.menu_path
        tmp_dict['reference'] = cls
        return tmp_dict

    @abc.abstractmethod
    def on_request(self, *args, **kwargs):
        """Abstract method for endpoint work

        This method is where work specifically for fufilling requests goes.
        When the RPC class is called, on_request() is called and wrapped in
        error handling and message passing so the subclass doesn't need to
        deal with it.

        This method **must** return a dictionary. For best results (for the
        client), that dictionary should conform to the "return_dict" structure
        losely defined in the code base. That structure being ``{'value': int,
        'message': [string], content: [string]}``
        """
        pass

class ModelWrapper(object):
    """ The base class for wrapping SQLAlchemy model objects

    This class provides utilities for interacting with SQLAlchemy models
    in a clean manner. This should be subclassed by any other objects that
    will need to wrap a SQLAlchemy model object.
    """
    __metaclass__ = abc.ABCMeta
    class ObjectDoesNotExist(CssefObjectDoesNotExist):
        def __init__(self, message):
            self.message = message

        def __str__(self):
            return repr(self.message)

    model_object = None
    fields = []

    def __init__(self, db_conn, model):
        self.db_conn = db_conn
        self.model = model
        self.define_properties()

    def define_properties(self):
        for i in self.fields:
            if not hasattr(self, i):
                attribute_get = self.__class__.dec_get(self, i)
                attribute_set = self.__class__.dec_set(self, i)
                prop = property(attribute_get, attribute_set)
                setattr(self.__class__, i, prop)

    def dec_get(self, attribute):
        def default_get(self):
            return getattr(self.model, attribute)

        return default_get

    def dec_set(self, attribute):
        def default_set(self, value):
            setattr(self.model, attribute, value)
            self.db_conn.commit()
        return default_set

    def get_id(self):
        return self.model.pkid

    def edit(self, **kwargs):
        for i in kwargs:
            if i in self.fields:
                setattr(self, i, kwargs[i])

    def delete(self):
        self.db_conn.delete(self.model)
        self.db_conn.commit()

    def as_dict(self):
        tmp_dict = {}
        tmp_dict['id'] = self.get_id()
        for i in self.fields:
            try:
                tmp_dict[i] = getattr(self, i)
            except AttributeError:
                # The field is not an attribute of the subclassed model wrapper
                # We'll try to find it in the classes model
                tmp_dict[i] = getattr(self.model, i)
        return tmp_dict

    @classmethod
    def count(cls, db_conn, **kwargs):
        return db_conn.query(cls.model_object).filter_by(**kwargs).count()

    @classmethod
    def search(cls, db_conn, **kwargs):
        model_object_list = db_conn.query(cls.model_object).filter_by(**kwargs)
        cls_list = []
        for i in model_object_list:
            cls_list.append(cls(db_conn, i))
        return cls_list

    @classmethod
    def from_database(cls, db_conn, pkid):
        try:
            return cls.search(db_conn, pkid=pkid)[0]
        except IndexError:
            return None

    @classmethod
    def from_dict(cls, db_conn, kw_dict):
        model_object_inst = cls.model_object() #pylint: disable=not-callable
        cls_inst = cls(db_conn, model_object_inst)
        for i in kw_dict:
            if i in cls_inst.fields:
                setattr(cls_inst, i, kw_dict[i])
        db_conn.add(cls_inst.model)
        db_conn.commit()
        return cls_inst

def create_database_connection(database_path):
    """Returns a database session for the specified database"""
    journal.send(message='Initializing database connection')
    database_engine = create_engine('sqlite:///' + database_path)
    try:
        Base.metadata.create_all(database_engine)
    except sqlalchemy.exc.OperationalError as error:
        journal.send(message='Failed to open or sync database file: %s' % database_path)
        raise error
    Base.metadata.bind = database_engine
    database_session = sessionmaker(bind=database_engine)
    return database_session()

def handle_exception(err):
    return_dict = get_empty_return_dict()
    return_dict['value'] = 1
    return_dict['message'] = traceback.format_exc().splitlines()
    journal.send(message="(error %d): Encountered runtime error with given id %d. Observe the following stack trace:" % (return_dict['value'], return_dict['value']))
    for i in return_dict['message']:
        journal.send(message="(error %d): %s" % (return_dict['value'], i))
    return return_dict

def get_empty_return_dict():
    return {
        'value': 0,
        'message': 'Success',
        'content': []
    }
