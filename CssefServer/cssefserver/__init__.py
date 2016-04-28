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
from cssefserver.utils import Configuration
from cssefserver.utils import create_database_connection
from cssefserver.account import tasks as account_tasks
from cssefserver import tasks as base_tasks

class CssefServer(object):
    def __init__(self):
        self.config = Configuration()
        # TODO: Idealy we would load configs from multiple source,
        # but we'll add that functionality later on...
        self.config.load_config_file(self.config.global_config_path)

        # THIS IS SUPER TEMPORARY!
        self.prepare_logging()

        # This is the database connection
        self.database_connection = None

        # Methods object to pass to the dispatcher when a request is handled
        self.rpc_methods = Methods()

        # The flask instance that handles incoming networking requests
        self.flask_app = None

    def load_plugins(self):
        for module_name in self.config.installed_plugins:
            try:
                __import__(module_name)
            except:
                print "Failed to load module: '%s'" % module_name


    def load_rpc_endpoints(self):
        endpoint_list = [
            (base_tasks.AvailableEndpoints, 'AvailableEndpoints'),
            (base_tasks.RenewToken, 'RenewToken'),
            (base_tasks.Login, 'Login'),
            (account_tasks.OrganizationAdd, 'organizationAdd'),
            (account_tasks.OrganizationDel, 'organizationDel'),
            (account_tasks.OrganizationSet, 'organizationSet'),
            (account_tasks.OrganizationGet, 'organizationGet'),
            (account_tasks.UserAdd, 'userAdd'),
            (account_tasks.UserDel, 'userDel'),
            (account_tasks.UserSet, 'userSet'),
            (account_tasks.UserGet, 'userGet')]
        for reference, name in endpoint_list:
            # I'm creating and storing an instance of every since endpoint...
            self.rpc_methods.add_method(reference(self.config, self.database_connection), name)

    def prepare_logging(self):
        pass
        # # I don't really know what's going on here. Making an issue to fix this later
        # # Make sure the files exist first
        # make_log_files(self.config)
        # # Set up the loggers (kinda... i suck at this)
        # logger = logging.getLogger("CssefDaemonLog")
        # logger.setLevel(logging.DEBUG)
        # formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # if self.config.cssef_stdout != '':
        # 	handler = logging.FileHandler(self.config.cssef_stdout)
        #   handler.setFormatter(formatter)
        # 	logger.addHandler(handler)

    def start(self):
        self.database_connection = create_database_connection(self.config)
        self.load_plugins()
        self.load_rpc_endpoints()
        self.flask_app = Flask(__name__)
        self.flask_app.add_url_rule('/', 'index', self.index, methods=['POST'])
        # This next line can throw a permissions error:
        # IOError: [Errno 13] Permission denied: '/var/log/cssef/error.log'
        # This should be caught and handleds, and possibly reported to the daemon?
        logging.basicConfig(filename='/var/log/cssef/error.log', level=logging.DEBUG)
        self.flask_app.run(debug=False)

    # This function shouldn't live here forever
    def index(self):
        rpc_resp = dispatch(self.rpc_methods, request.get_data().decode('utf-8'))
        return Response(str(rpc_resp), rpc_resp.http_status, mimetype='application/json')

# Dumpy old logging methods
def make_log_files(config):
    # Now create the log files within that directory
    files = [config.cssef_stderr, config.cssef_stdout]
    for i in files:
        if i == '':
            continue
        # Get the directory the file should be in
        log_directory = "/".join(i.split('/')[:-1])
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        # Now create the files in that directory
        if not os.path.isfile(i):
            open(i, 'a').close()

# Import plugins
def import_plugins(config):
    plugin_list = []
    if config.installed_plugins:
        for module_name in config.installed_plugins:
            plugin_list.append(__import__(module_name))
    return plugin_list
