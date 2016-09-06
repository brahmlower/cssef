import os
import os.path
from systemd import journal
# RPC Server related imports
from flask import Flask
from flask import request
from flask import Response
from jsonrpcserver import dispatch
from jsonrpcserver import Methods
# Local imports
from cssefserver import tasks as base_tasks
from cssefserver.utils import Configuration
from cssefserver.utils import create_database_connection
from cssefserver.account import tasks as account_tasks

class CssefServer(object):
    """The CSSEF Server object

    The server coordinates the tracking of configurations, plugins,
    endpoints, database connection and socket connection (via flask) for
    incoming requests.
    """
    def __init__(self, config_dict = {}):
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

        # The flask instance that handles incoming networking requests
        self.flask_app = Flask(__name__)

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
        journal.send(message = 'Starting plugin import')
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
                journal.send(message = "Incorrectly formatted plugin entry: '%s'." % module_string)
                continue
            try:
                module = __import__(module_name)
                plugin_class_ref = getattr(module, module_class)
            except:
                journal.send(message = "Failed to import module: '%s'" % module_name)
                continue
            plugin_class_inst = plugin_class_ref(self.config)
            self.plugins.append(plugin_class_inst)
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
        journal.send(message = 'Loading RCP endpoints...')
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
                journal.send(message = 'Loading endpoint: %s' % endpoint['rpc_name'])
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
        self.database_connection = create_database_connection(self.config)
        # Load the RCP Endpoints, instantiating each one and making it
        # available for Flask
        self.load_rpc_endpoints()
        # Start listening for rpc requests via Flask
        journal.send(message = 'Initializing flask instance')
        self.flask_app.add_url_rule('/', 'index', self.index, methods=['POST'])
        self.flask_app.run(debug=False)

    def index(self):
        """Function called by the flask app for new requests

        This function handles incoming requests to the '/' path for the RPC
        server. It matches the incoming request to the corresponding endpoint
        that's registered in self.rpc_methods.

        TODO: This function should probably not be here forever.
        TODO: Improve comments explaining what's happening here...
        """
        rpc_resp = dispatch(self.rpc_methods, request.get_data().decode('utf-8'))
        return Response(str(rpc_resp), rpc_resp.http_status, mimetype='application/json')

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

# Import plugins
def import_plugins(config):
    """Imports plugins listed in the provided configuration

    This just loops through the list of plugins and imports them. There is no
    real error checking here.

    Returns:
        list
    """
    plugin_list = []
    if config.installed_plugins:
        for module_name in config.installed_plugins:
            plugin_list.append(__import__(module_name))
    return plugin_list
