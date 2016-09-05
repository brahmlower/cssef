import os
import re
import ast
import sys
import time
import yaml
from jsonrpcclient.http_server import HTTPServer
from cssefclient.tasks import RenewToken
from cssefclient.tasks import AvailableEndpoints
from cssefclient.utils import parse_time_notation
from cssefclient.utils import load_token_file

class CssefClient(object):
    def __init__(self):
        self.config = Configuration()
        self.endpoints = None

    def connect(self):
        """Establishes a connection to the celery server

        This sets the attribute `apiConn` to an open connection to the Celery
        server, based on the settings. This connection can be provided to a
        `CeleryEndpoint` to execute a task
        """
        self.config.server_connection = HTTPServer(self.config.server_url)

    def load_endpoints(self):
        endpoint_loader = EndpointsLoader(self.config)
        endpoint_loader.determine_source()
        self.endpoints = endpoint_loader.load()

    def load_token(self, auth):
        # If we're not supposed to do this, then dont do it
        if not self.config.token_auth_enabled:
            return False
        # Read the token from the file
        token = load_token_file(self.config.token_file)
        if token:
            self.config.token = token
        # Renew the token if it's enabled
        if self.config.token_renewal_enabled:
            return RenewToken(self.config).execute(auth=auth)

    def call_endpoint(self, command, args):
        return command.execute(**args)

class Configuration(object):
    """Contains and loads configuration values

    There is one attribute for each configuration that can be set.
    Configurations can be loaded from a file or dictionary. When loading
    configurations, any hyphens wihtin key values will be converted to
    underscores so that the attribute can be set.
    """
    def __init__(self):
        # Super global configs
        self.global_config_path = "/etc/cssef/cssef-client.yml"
        self.user_data_dir = os.path.expanduser("~/.cssef/")
        self.config_path = self.user_data_dir + "cssef-client.yml"
        self.server_connection = None
        # General configurations
        self.auth = {}
        self.verbose = False
        self.organization = None
        self.username = None
        self.password = None
        self.task_timeout = 5
        self.admin_token = None
        self.prompt_password = True
        # Default values for the client configuration
        self.rpc_hostname = "localhost"
        self.rpc_port = "5000"
        self.rpc_base_uri = "/"
        # Token configurations
        self.token_auth_enabled = True
        self.token = None
        self.token_file = self.user_data_dir + "token"
        self.token_renewal_enabled = True
        # Endpoint caching
        self.endpoint_cache_enabled = True
        self.force_endpoint_cache = False
        self.force_endpoint_server = False
        self.endpoint_cache_file = self.user_data_dir + "endpoint-cache"
        self.raw_endpoint_cache_time = '3600'

    @property
    def server_url(self):
        return "http://%s:%s%s" % (self.rpc_hostname, self.rpc_port, self.rpc_base_uri)

    @property
    def endpoint_cache_time(self):
        return self.raw_endpoint_cache_time

    @endpoint_cache_time.setter
    def endpoint_cache_time(self, value):
        try:
            self.raw_endpoint_cache_time = int(value)
        except ValueError:
            pass
        self.raw_endpoint_cache_time = parse_time_notation(value)


    def load_config_file(self, config_path):
        """Load configuration from a file

        This will read a yaml configuration file. The yaml file is converted
        to a dictionary object, which is just passed to `loadConfigDict`.

        Args:
            config_path (str): A filepath to the yaml config file

        Returns:
            None
        """
        try:
            config_dict = yaml.load(open(config_path, 'r'))
        except IOError:
            print "[WARNING] Failed to load config file at '%s'." % config_path
            return None
        if config_dict:
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
        # We want to make sure verbose is set first if it's provided
        if "verbose" in config_dict:
            setattr(self, "verbose", bool(config_dict.pop("verbose")))
            if self.verbose:
                print "[LOGGING] Configuration 'verbose' set to 'True'."
        for i in config_dict:
            if hasattr(self, i.replace('-', '_')):
                # Set the attribute
                setting = i.replace('-', '_')
                value = config_dict[i]
                # This is a hacky way of handling booleans: Check if the value is a string
                # and if the string is either 'true' or 'false'. If so, we're probably trying
                # to set a boolean, so we cast it to a boolean
                if isinstance(value, str) and value.lower() in ['true', 'false']:
                    value = value.lower() == 'true'
                setattr(self, setting, value)
                if self.verbose:
                    print "[LOGGING] Configuration '%s' set to '%s'." % (i, value)
            elif isinstance(config_dict[i], dict):
                # This is a dictionary and may contain additional values
                self.load_config_dict(config_dict[i])
            else:
                # We don't care about it. Just skip it!
                # if self.verbose:
                print "[WARNING] Ignoring invalid setting '%s'." % i

    def load_token(self):
        # If we're not supposed to do this, then dont do it
        if not self.token_auth_enabled:
            return None
        # Load the token. Failure to load will set self.token to None, which
        # is already the default value. Token absense is handled elsewhere. Errors
        # are logged by load_token_file
        self.token = load_token_file(self.token_file)

class AuthBuilder(object):
    def __init__(self, config):
        self.admin_token = config.admin_token
        self.username = config.username
        self.organization = config.organization
        self.password = config.password
        self.token = config.token
        # This is just to track what type of authentication we're doing
        # available options are "password", "token", "admin-token", "invalid"
        self.auth_strategy = {
            "invalid": self.auth_invalid,
            "admin-token": self.auth_admin_token,
            "token": self.auth_token,
            "password": self.auth_password
        }

    def get_auth_strategy(self):
        # If the admin token is set, we use that and ignore any other options
        if self.admin_token:
            return "admin-token"
        # For other types of of authentication, we need a username/organization
        if not self.username or not self.organization:
            return "invalid"
        if self.token:
            return "token"
        if self.password:
            return "password"
        # Since no other authentication type has matched yet, if the requirements
        # for password authentication are fufilled, then we have incomplete
        # authentication information
        return "invalid"

    def auth_invalid(self):
        return None

    def auth_admin_token(self):
        auth_dict = {}
        auth_dict["admin-token"] = self.admin_token
        return auth_dict

    def auth_token(self):
        auth_dict = {}
        auth_dict["username"] = self.username
        auth_dict["organization"] = self.organization
        auth_dict["token"] = self.token
        return auth_dict

    def auth_password(self):
        auth_dict = {}
        auth_dict["username"] = self.username
        auth_dict["organization"] = self.organization
        auth_dict["password"] = self.password
        return auth_dict

    def as_dict(self):
        strategy = self.get_auth_strategy()
        return self.auth_strategy[strategy]()

    def is_valid(self):
        return not "invalid" == self.get_auth_strategy()

class EndpointsLoader(object):
    def __init__(self, config):
        self.config = config
        self.endpoints = None
        self.from_cache = False

    def load(self):
        if self.from_cache:
            output = self.load_from_file()
            # TODO: We should eventually return an output object from
            # loadFromFile. Then make sure that if it failed, we failover to
            # loading from the server (maybe?)
            #self.endpoints = output.content
        else:
            output = self.load_from_server()
            if not output:
                # Raise an error since we failed to load the endpoints
                print output.value
                print output.message
                raise Exception
            self.endpoints = output.content
            self.update_cache()
        return self.endpoints

    def determine_source(self):
        # Are we even caching?
        if not self.config.endpoint_cache_enabled:
            self.from_cache = False
            return
        # consider forced sources first
        if self.config.force_endpoint_cache:
            self.from_cache = True
            return
        if self.config.force_endpoint_server:
            self.from_cache = False
            return
        # Endpoint caching is enabled, but the source hasn't been forced
        # so we need to figure out if we should pull from the cache or not
        try:
            cache_last_mod_time = os.stat(self.config.endpoint_cache_file).st_mtime
        except OSError:
            # Failed to read from the file, load from server
            print "Failed to read cache file: %s" % self.config.endpoint_cache_file
            # TODO: Libraries shouldn't print! (I thought this was a library,
            # not a printing press! :P)
            self.from_cache = False
            return
        time_delta = time.time() - cache_last_mod_time
        # If it has been longer since the cache was updated than is
        # configured, then we need to load from server
        if time_delta >= self.config.raw_endpoint_cache_time:
            self.from_cache = False
        self.from_cache = True

    def load_from_server(self):
        """Retrieves the available endpoints from the server.
        """
        output = AvailableEndpoints(self.config).execute()
        return output

    def load_from_file(self):
        """Retrieves the available endpoints from the cache
        """
        file_content = open(self.config.endpoint_cache_file, 'r').read()
        # This will throw an error if the content of file cannot be literally
        # evaluated. This is good for here, but should be caught in the
        # cli tool
        self.endpoints = ast.literal_eval(file_content)

    def update_cache(self):
        """Writes the received endpoints to the cache file
        """
        if not self.endpoints:
            # The endpoints are not actually endpoints. Don't write over
            # possibly valid endpoints already in the cache
            return
        wfile = open(self.config.endpoint_cache_file, 'w')
        wfile.write(str(self.endpoints))
        wfile.close()
