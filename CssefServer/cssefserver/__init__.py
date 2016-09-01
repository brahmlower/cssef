import os
import os.path
import logging
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

        # Prepare the logger. This will run before start() is called, meaning
        # any logging errors should arise before daemonization happens. This
        # might cause problems if the daemonized process is started as a user
        # that has different permissions than the user that own the parent
        # process...
        # TODO: Test this hypothesis
        self.prepare_logging()

        # This is the database connection
        self.database_connection = None

        # Methods object to pass to the dispatcher when a request is handled
        self.rpc_methods = Methods()

        # The flask instance that handles incoming networking requests
        self.flask_app = Flask(__name__)

        # The list of plugins we will be running with
        self.plugins = []

    def import_plugins(self):
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
                logging.error("Incorrectly formatted plugin entry: '%s'." % module_string)
                continue
            try:
                module = __import__(module_name)
                plugin_class_ref = getattr(module, module_class)
            except:
                logging.error("Failed to import module: '%s'" % module_name)
                continue
            plugin_class_inst = plugin_class_ref(self.config)
            self.plugins.append(plugin_class_inst)
        # This is just to finish implementing the Available Endpoints task
        # TODO: Maybe make a distinctions between 'configuration' and 'running configuration'?
        self.config.installed_plugins = self.plugins

    def load_rpc_endpoints(self):
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
                logging.info('Adding plugin method: %s, %s' % (instance.__class__, endpoint['rpc_name']))
                self.rpc_methods.add_method(instance, endpoint['rpc_name'])
                # Pop the reference key from the dict so we don't try to send it
                # to the client later when the client requests the available enpoints
                endpoint.pop('reference')

    def prepare_logging(self):
        # This next line can throw a permissions error:
        # IOError: [Errno 13] Permission denied: '/var/log/cssef/error.log'
        # This should be caught and handled, and possibly reported to the daemon?
        logging.basicConfig(filename=self.config.cssef_stderr, level=logging.DEBUG)
        logging.info('Initialized logging')

    def start(self):
        # Plugin imports *must* happen before making the database connection
        # otherwise tables won't be made for plugins
        logging.debug('Starting plugin import')
        self.import_plugins()
        # The database connection *must* be initialized before loading the rpc
        # endpoints, otherwise the endpoints will get the default value for
        # the database_connection, which is None (breaks everything)
        logging.debug('Initializing database connection')
        self.database_connection = create_database_connection(self.config)
        # Load the RCP Endpoints, instantiating each one and making it available
        # for Flask
        logging.debug('Loading RCP endpoints')
        self.load_rpc_endpoints()
        # Start listening for rpc requests via Flask
        logging.debug('Initializing flask instance')
        self.flask_app.add_url_rule('/', 'index', self.index, methods=['POST'])
        self.flask_app.run(debug=False)

    # This function shouldn't live here forever
    def index(self):
        rpc_resp = dispatch(self.rpc_methods, request.get_data().decode('utf-8'))
        return Response(str(rpc_resp), rpc_resp.http_status, mimetype='application/json')

class Plugin(object):
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
    plugin_list = []
    if config.installed_plugins:
        for module_name in config.installed_plugins:
            plugin_list.append(__import__(module_name))
    return plugin_list
