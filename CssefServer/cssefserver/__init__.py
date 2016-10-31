import os
import os.path
import sys
import abc
import logging
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
from cssefserver.errors import CssefPluginInstantiationError

class CssefServer(object):
    """The CSSEF Server object

    The server coordinates the tracking of configurations, plugins,
    endpoints, database connection and socket connection (via jsonrpcserver) for
    incoming requests.
    """
    def __init__(self, config=None):
        self.config = config
        if not self.config:
            self.config = Configuration()

        # This is the database connection
        self.database_connection = None

        # Methods object to pass to the dispatcher when a request is handled
        self.rpc_methods = Methods()

        # List of endpoint sources
        self.endpoint_sources = []

        # The list of plugins we will be running with
        self.plugin_manager = PluginManager(module_list=self.config.installed_plugins)

    def load_endpoint_sources(self):
        from cssefserver import tasks as base_tasks
        temp_list = []
        temp_list.append(base_tasks.endpoint_source())
        for plugin in self.plugin_manager.available_plugins:
            temp_list.append(plugin.endpoint_info())
        self.endpoint_sources = temp_list

    def load_endpoints(self):
        """Instantiates RPC endpoints

        The RPC endpoing objects are all instantiated once, and then simply
        called any time a request is received for that endpoint. After the
        endpoint has been instantiated, it is added to the ``self.rpc_methods``
        object, which is provided to the jsonrpcserver to define request routing.

        Returns:
            None
        """
        logging.info("Loading endpoints from {} sources.".format(len(self.endpoint_sources)))
        for source in self.endpoint_sources:
            logging.info("Loading endpoints from source '{}'.".format(source['name']))
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
        # Load the RCP Endpoints, instantiating each one and making it
        # available for the web server
        self.load_endpoint_sources()
        self.load_endpoints()
        # Start listening for rpc requests
        logging.info('Starting httpserver')
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
                logging.info("Configuration '{}' set to '{}'.".format(i, settings_dict[i]))
            except ValueError:
                logging.warning("Ignoring invalid configuration '{}'.".format(i))

class PluginManager(object):
    def __init__(self, module_list=None):
        self.available_plugins = []
        if module_list != None:
            self.import_from_list(module_list)

    def import_from_string(self, module_string):
        if len(module_string.split(".")) != 2:
            raise CssefPluginMalformedName(module_string)
        module_name = module_string.split(".")[0]
        class_name = module_string.split(".")[1]
        try:
            module = __import__(module_name)
            plugin_class_ref = getattr(module, class_name)
            self.available_plugins.append(plugin_class_ref())
            logging.info('Plugin import success: {}'.format(module_string))
        except:
            logging.warning('Plugin import failed: {}'.format(module_string))
            raise CssefPluginInstantiationError(module_string)

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

    def __init__(self, server, model):
        self.server = server
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
            self.server.database_connection.commit()
        return default_set

    def get_id(self):
        return self.model.pkid

    def edit(self, **kwargs):
        for i in kwargs:
            if i in self.fields:
                setattr(self, i, kwargs[i])

    def delete(self):
        self.server.database_connection.delete(self.model)
        self.server.database_connection.commit()

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
    def count(cls, server, **kwargs):
        return server.database_connection.query(cls.model_object).filter_by(**kwargs).count()

    @classmethod
    def search(cls, server, **kwargs):
        model_object_list = server.database_connection.query(cls.model_object).filter_by(**kwargs)
        cls_list = []
        for i in model_object_list:
            cls_list.append(cls(server, i))
        return cls_list

    @classmethod
    def from_database(cls, server, pkid):
        try:
            return cls.search(server, pkid=pkid)[0]
        except IndexError:
            return None

    @classmethod
    def from_dict(cls, server, kw_dict):
        model_object_inst = cls.model_object() #pylint: disable=not-callable
        cls_inst = cls(server, model_object_inst)
        for i in kw_dict:
            if i in cls_inst.fields:
                setattr(cls_inst, i, kw_dict[i])
        server.database_connection.add(cls_inst.model)
        server.database_connection.commit()
        return cls_inst

class ParseInput(object):
    def __init__(self, input_list):
        self.remaining_args = input_list
        self.options = {}
        self.command = []
        self.command_args = {}
        self.parse_input()

    def parse_input(self):
        self.parse_command()
        self.parse_command_args()

    def parse_options(self):
        index = 0
        while index < len(self.remaining_args) and self.remaining_args[index][0] == '-':
            argument = self.remaining_args[index]
            argument = argument.strip('-')
            if len(argument.split("=")) > 1:
                # The value is in the same argument
                keyword = argument.split('=')[0]
                value = argument.split('=')[1]
            else:
                # The value is in the next argument
                keyword = argument
                value = self.remaining_args[index + 1]
                index += 1
            self.options[keyword] = value
            index += 1
        self.remaining_args = self.remaining_args[index:]

    def parse_command(self):
        index = 0
        while index < len(self.remaining_args) and self.remaining_args[index][0] != '-':
            self.command.append(self.remaining_args[index])
            index += 1
        self.remaining_args = self.remaining_args[index:]

    def parse_command_args(self):
        index = 0
        while index < len(self.remaining_args) and self.remaining_args[index][0] == '-':
            argument = self.remaining_args[index]
            argument = argument.strip('-')
            if len(argument.split("=")) > 1:
                # The value is in the same argument
                keyword = argument.split('=')[0].replace('-', '_')
                value = argument.split('=')[1]
            else:
                # The value is in the next argument
                keyword = argument.replace('-', '_')
                try:
                    value = self.remaining_args[index + 1]
                except IndexError:
                    # There is no next error. Complain and quit
                    sys.exit("Expected value in for argument, but got none.")
                index += 1
            self.command_args[keyword] = value
            index += 1

def main(raw_input_list):
    # Parse the user input. Make sure a command was provided and that it is
    # one of the available commands
    logging.basicConfig(level=logging.DEBUG)
    user_input = ParseInput(raw_input_list)
    if len(user_input.command) < 0:
        sys.exit("Usage: cssef-server [options]")

    # The configuration loading process is tricky, since settings provided at
    # runtime may dictate how we load other configurations. Load the runtime
    # configurations, and then load the configurations from the file. We load
    # the runtime configurations again to reset any configurations that may have
    # been overwritten while loading from the file.

    # 1: Load the runtime configurations
    # 2: Load the file configurations
    # 3: Load the runtime configurations again
    config = Configuration()
    config.from_dict(user_input.command_args)
    config.from_file("/etc/cssef/cssef-server.yml")
    config.from_dict(user_input.command_args)

    # Create the server object based on the configuration we built, and then
    # start it.
    server = CssefServer(config=config)
    # The database connection *must* be initialized before loading the rpc
    # endpoints, otherwise the endpoints will get the default value for
    # the database_connection, which is None (breaks everything)
    server.database_connection = create_database_connection(server.config.database_path)
    server.start()
