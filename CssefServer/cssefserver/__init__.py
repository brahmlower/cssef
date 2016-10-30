import os
import os.path
import abc
import traceback
from systemd import journal
import yaml
# RPC Server related imports
from jsonrpcserver import dispatch
from jsonrpcserver import Methods
# Local imports
from cssefserver.databaseutils import create_database_connection
from cssefserver.utils import EndpointOutput
from cssefserver.errors import CssefException
from cssefserver.errors import CssefObjectDoesNotExist
from cssefserver.errors import CssefPluginMalformedName

class CssefServer(object):
    """The CSSEF Server object

    The server coordinates the tracking of configurations, plugins,
    endpoints, database connection and socket connection (via jsonrpcserver) for
    incoming requests.
    """
    def __init__(self, config=None):
        if not config:
            self.config = Configuration()

        # This is the database connection
        self.database_connection = None

        # Methods object to pass to the dispatcher when a request is handled
        self.rpc_methods = Methods()

        # List of endpoint sources
        self.endpoint_sources = []

        # The list of plugins we will be running with
        self.plugin_manager = PluginManager(module_list = self.config.installed_plugins)
        #self.plugins = []

    def load_endpoint_sources(self):
        from cssefserver.account import tasks as account_tasks
        from cssefserver import tasks as base_tasks
        temp_list = []
        temp_list.append(base_tasks.endpoint_source())
        temp_list.append(account_tasks.endpoint_source())
        for plugin in self.plugin_manager.available_plugins:
            temp_list.append(plugin.endpoint_info())
        self.endpoint_sources = temp_list

    #def load_source_endpoints(self, source):
    #    journal.send(message="Loading endpoints from source '%s'." % source['name']) #pylint: disable=no-member
    #    for endpoint in source['endpoints']:
    #        # Instantiate the endpoint and pass it a reference to the server
    #        instance = endpoint['reference'](self)
    #        self.rpc_methods.add_method(instance, endpoint['rpc_name'])

    def load_endpoints(self):
        """Instantiates RPC endpoints

        The RPC endpoing objects are all instantiated once, and then simply
        called any time a request is received for that endpoint. After the
        endpoint has been instantiated, it is added to the ``self.rpc_methods``
        object, which is provided to the jsonrpcserver to define request routing.

        Returns:
            None
        """
        journal.send(message="Loading endpoints from %d sources." % len(self.endpoint_sources))
        for source in self.endpoint_sources:
            journal.send(message="Loading endpoints from source '%s'." % source['name']) #pylint: disable=no-member
            for endpoint in source['endpoints']:
                # Instantiate the endpoint and pass it a reference to the server
                instance = endpoint['reference'](self)
                self.rpc_methods.add_method(instance, endpoint['rpc_name'])

    def start(self):
        """Starts running the service

        This will start the process of importing plugins, creating the
        database connection, loading the rpc endpoints, and then registering
        and starting the builtin httpserver that is wrapped by the jsonrpcserver.

        TODO: I may eventually change this so that this **only** starts the
        rpcserver, meaning the rest of the work can be done elsewhere, which
        would allow for better flexabiltiy and error handling.

        Returns:
            None
        """

        # Plugin imports *must* happen before making the database connection
        # otherwise tables won't be made for plugins
        journal.send(message='Starting plugin import') #pylint: disable=no-member
        #self.plugins = import_plugins(self.config.installed_plugins)
        # The database connection *must* be initialized before loading the rpc
        # endpoints, otherwise the endpoints will get the default value for
        # the database_connection, which is None (breaks everything)
        self.database_connection = create_database_connection(self.config.database_path)
        # Load the RCP Endpoints, instantiating each one and making it
        # available for the web server
        self.load_endpoint_sources()
        self.load_endpoints()
        # Start listening for rpc requests
        journal.send(message='Starting httpserver') #pylint: disable=no-member
        self.rpc_methods.serve_forever()

class Configuration(object):
    """Contains and loads server configuration values

    There is one attribute for each configuration that can be set.
    Configurations can be loaded from a file or dictionary. When loading
    configurations, any hyphens wihtin key values will be converted to
    underscores so that the attribute can be set.
    """
    def __init__(self):
        # Super global configs
        self.admin_token = ""
        # SQLAlchemy configurations
        self.database_table_prefix = ""
        self.database_path = ""
        # General configurations
        self.auth_failover = True
        self.auth_token_salt = ""
        # Logging configurations
        self.cssef_loglevel = ""
        self.cssef_stderr = ""
        self.cssef_stdout = ""
        # Plugin configurations
        self.installed_plugins = []

    def _clean_setting(self, string):
        return string.replace('-', '_')

    def _valid_setting(self, string):
        return hasattr(self, self._clean_setting(string))

    def set_setting(self, setting_name, setting_value):
        if not self._valid_setting(setting_name):
            raise ValueError("Invalid configuration setting {}".format(setting_name))
        setting_name = self._clean_setting(setting_name)
        setattr(self, setting_name, setting_value)

    def from_file(self, settings_file_path):
        """Load configuration from a file

        This will read a yaml configuration file. The yaml file is converted
        to a dictionary object, which is just passed to `load_settings_dict`.

        Args:
            settings_file_path (str): A filepath to the yaml config file

        Returns:
            None
        """
        with open(settings_file_path, 'r') as settings_file:
            settings_dict = yaml.load(settings_file)
        self.from_dict(settings_dict)

    def from_dict(self, settings_dict):
        """Load configurations from a dictionary

        This will convert strings with hyphens (-) to underscores (_) that way
        attributes can be added. Underscores are not used in the config files
        because I think they look ugly. That's my only reasoning - deal with
        it. Any key within the dictionary that is not an attribute of the
        class will be ignored (this will be logged).

        Args:
            settings_dict (dict): A dictionary containing configurations and
                values

        Returns:
            None
        """
        for i in settings_dict:
            try:
                self.set_setting(i, settings_dict[i])
                journal.send(message="Configuration '%s' set to '%s'." % (i, settings_dict[i])) #pylint: disable=no-member
            except ValueError:
                journal.send(message="Ignoring invalid configuration '%s'." % i) #pylint: disable=no-member

class PluginManager(object):
    def __init__(self, module_list = None):
        self.available_plugins = []
        if module_list != None:
            self.import_from_list(module_list)

    def import_from_string(self, module_string):
        if len(module_string.split(".")) != 2:
            raise errors.CssefPluginMalformedName(module_string)
        module_name = module_string.split(".")[0]
        class_name = module_string.split(".")[1]
        try:
            module = __import__(module_name)
            plugin_class_ref = getattr(module, class_name)
            self.available_plugins.append(plugin_class_ref())
            journal.send(message='Plugin import success: {}'.format(module_string)) #pylint: disable=no-member
        except:
            journal.send(message='Plugin import failed: {}'.format(module_string)) #pylint: disable=no-member
            raise errors.CssefPluginInstantiationError(module_string)

    def import_from_list(self, module_list):
        for module_string in module_list:
            self.import_from_string(module_string)

class Plugin(object):
    """A base competition plugin class

    This class provides the basic functionality for registering new
    competition plugins. More methods will be made available in the future to
    improve utility provided to subclasses.
    """
    name = ""
    short_name = ""
    __version__ = ""
    endpoints = []

    @classmethod
    def endpoint_info(cls):
        tmp_dict = {}
        tmp_dict['name'] = cls.__name__
        tmp_dict['endpoints'] = []
        for endpoint in cls.endpoints:
            tmp_dict['endpoints'].append(endpoint.info_dict())
        return tmp_dict

    def as_dict(self):
        tmp_dict = {}
        tmp_dict['name'] = self.name
        tmp_dict['short_name'] = self.short_name
        tmp_dict['version'] = self.__version__
        return tmp_dict

#TODO: Write unit tests
class ModelWrapper(object):
    """ The base class for wrapping SQLAlchemy model objects

    This class provides utilities for interacting with SQLAlchemy models
    in a clean manner. This should be subclassed by any other objects that
    will need to wrap a SQLAlchemy model object.
    """
    __metaclass__ = abc.ABCMeta
    class ObjectDoesNotExist(CssefObjectDoesNotExist):
        def __init__(self, message):
            super(self.__class__, self).__init__(message)

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
