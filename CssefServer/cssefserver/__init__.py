import os
import os.path
import traceback
from systemd import journal
import yaml
# RPC Server related imports
from flask import Flask
from flask import request
from flask import Response
from jsonrpcserver import dispatch
from jsonrpcserver import Methods
# Local imports
from cssefserver import tasks as base_tasks
from cssefserver.utils import create_database_connection
from cssefserver.account import tasks as account_tasks

class CssefServer(object):
    """The CSSEF Server object

    The server coordinates the tracking of configurations, plugins,
    endpoints, database connection and socket connection (via flask) for
    incoming requests.
    """
    def __init__(self, config_dict=None):
        if not config_dict:
            config_dict = None
        self.config = Configuration()

        # The configuration loading process is tricky, since settings provided
        # at runtime may dictate how we load other configurations. Load the
        # runtime configurations, and then load the configurations from the
        # file. We load the runtime configurations again to reset any
        # configurations that may have been overwritten while loading from the
        # file.

        # 1: Load the runtime configurations
        # 2: Load the file configurations
        # 3: Load the runtime configurations again
        self.config.load_config_dict(config_dict)
        self.config.load_config_file(self.config.global_config_path)
        self.config.load_config_dict(config_dict)

        # This is the database connection
        self.database_connection = None

        # Methods object to pass to the dispatcher when a request is handled
        self.rpc_methods = Methods()

        # The list of plugins we will be running with
        self.plugins = []

    def import_plugins(self):
        """Instantiates CSSEF competition plugins

        Plugins that were specified within the ``installed-plugins``
        configuration are instantiated here. Successfully loaded plugins are
        listed in ``self.plugins``. If a plugin fails to load, it is
        effectively removed from ``self.config.installed_plugins``.

        Returns:
            None
        """
        journal.send(message='Starting plugin import') #pylint: disable=no-member
        # If the 'installed_plugins' line is provided, but no items are
        # included in the list, then the value of
        # self.config.installed_plugins will be None. Return if there are no
        # installed plugins.
        if not self.config.installed_plugins:
            return
        for module_string in self.config.installed_plugins:
            try:
                module_name = module_string.split(".")[0]
                module_class = module_string.split(".")[1]
            except ValueError:
                journal.send(message="Incorrectly formatted plugin entry: '%s'." % module_string) #pylint: disable=no-member
                continue
            try:
                module = __import__(module_name)
                plugin_class_ref = getattr(module, module_class)
                plugin_class_inst = plugin_class_ref(self.config)
                self.plugins.append(plugin_class_inst)
                journal.send(message="Successfully import plugin: '%s'" % module_name) #pylint: disable=no-member
            except:
                journal.send(message="Failed to import module: '%s'" % module_name) #pylint: disable=no-member
                for i in traceback.format_exc().splitlines():
                    journal.send(message="    " + i) #pylint: disable=no-member
                continue
        # This is just to finish implementing the Available Endpoints task
        # TODO: Maybe make a distinctions between 'configuration' and 'running
        # configuration'?
        self.config.installed_plugins = self.plugins

    def load_rpc_endpoints(self):
        """Instantiates RPC endpoints

        The RPC endpoing objects are all instantiated once, and then simply
        called any time a request is received for that endpoint. After the
        endpoint has been instantiated, it is added to the ``self.rpc_methods``
        object, which is provided to the flask app to define request routing.

        Returns:
            None
        """
        journal.send(message='Loading RCP endpoints...') #pylint: disable=no-member
        # Create the list of endpoints sources
        self.config.endpoint_sources = []
        self.config.endpoint_sources.append(account_tasks.endpoint_source())
        self.config.endpoint_sources.append(base_tasks.endpoint_source())
        for plugin in self.plugins:
            self.config.endpoint_sources.append(plugin.endpoint_info())

        # Now import add all of the endpoints as methods to watch for
        for source in self.config.endpoint_sources:
            for endpoint in source['endpoints']:
                # Add the endpoint to the method list for Flask
                instance = endpoint['reference'](self.config, self.database_connection)
                journal.send(message='Loading endpoint: %s' % endpoint['rpc_name']) #pylint: disable=no-member
                self.rpc_methods.add_method(instance, endpoint['rpc_name'])
                # Pop the reference key from the dict so we don't try to send
                # it to the client later when the client requests the
                # available enpoints
                endpoint.pop('reference')

    def start(self):
        """Starts running the service

        This will start the process of importing plugins, creating the
        database connection, loading the rpc endpoints, and then registering
        and starting the flask app.

        TODO: I may eventually change this so that this **only** starts the
        flask app, meaning the rest of the work can be done elsewhere, which
        would allow for better flexabiltiy and error handling.

        Returns:
            None
        """

        # Plugin imports *must* happen before making the database connection
        # otherwise tables won't be made for plugins
        self.import_plugins()
        # The database connection *must* be initialized before loading the rpc
        # endpoints, otherwise the endpoints will get the default value for
        # the database_connection, which is None (breaks everything)
        self.database_connection = create_database_connection(self.config.database_path)
        # Load the RCP Endpoints, instantiating each one and making it
        # available for Flask
        self.load_rpc_endpoints()
        # Start listening for rpc requests via Flask
        journal.send(message='Initializing flask instance') #pylint: disable=no-member
        flask_app = Flask(__name__)
        flask_app.add_url_rule('/', 'index', self.index, methods=['POST'])
        flask_app.run(debug=False)


    def index(self):
        """Function called by the flask app for new requests

        This function handles incoming requests to the '/' path for the RPC
        server. It matches the incoming request to the corresponding endpoint
        that's registered in self.rpc_methods.

        TODO: This function should probably not be here forever.
        TODO: Improve comments explaining what's happening here...
        """
        received_data = request.get_data().decode('utf-8')
        rpc_result = dispatch(self.rpc_methods, received_data)
        return Response(str(rpc_result), rpc_result.http_status, mimetype='application/json')

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
                journal.send(message="Configuration '%s' set to '%s'." % (i, value)) #pylint: disable=no-member
            elif isinstance(config_dict[i], dict):
                # This is a dictionary and may contain additional values
                self.load_config_dict(config_dict[i])
            else:
                # We don't care about it. Just skip it!
                journal.send(message="Ignoring invalid configuration '%s'." % i) #pylint: disable=no-member

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
    def __init__(self, config):
        self.config = config

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
