import os
import re
import ast
import sys
import time
import yaml
from getpass import getpass
from jsonrpcclient.http_server import HTTPServer
from cssefclient.tasks import RenewToken
from cssefclient.utils import RPCEndpoint
from cssefclient.utils import parse_time_notation
from cssefclient.utils import load_token_file

class CssefClient(object):
    def __init__(self):
        self.config = Configuration()
        self.auth = AuthBuilder()
        self.endpoint_sources = []
        self.server_connection = None

    def connect(self):
        """Establishes a connection to the celery server
        """
        self.server_connection = HTTPServer(self.config.server_url)

    def load_endpoints(self):
        endpoint_loader = EndpointsLoader(self.config, self.server_connection)
        self.endpoint_sources = endpoint_loader.load()

    def load_auth(self):
        self.auth.load_from_config(self.config)
        return self.auth.is_valid()

class Configuration(object):
    """Contains and loads configuration values

    There is one attribute for each configuration that can be set.
    Configurations can be loaded from a file or dictionary. When loading
    configurations, any hyphens wihtin key values will be converted to
    underscores so that the attribute can be set.
    """
    filepath_configs = [
    'token_file',
    'endpoint_cache_file'
    ]

    def __init__(self):
        # Super global configs
        self.global_config_path = "/etc/cssef/cssef-client.yml"
        self.user_config_path = os.path.expanduser("~/.cssef/cssef-client.yml")
        self.user_data_dir = os.path.expanduser("~/.cssef/")
        # General configurations
        self.verbose = False
        self.task_timeout = 5
        # Server connection
        self.rpc_hostname = ''
        self.rpc_port = ''
        # Authentication
        self.admin_token = None
        self.organization = None
        self.username = None
        self.password = None
        self.prompt_password = True
        # Token configurations
        self.token_auth_enabled = True
        self.token = None
        self.token_file = ''
        self.token_renewal_enabled = True
        # Endpoint caching
        self.endpoint_cache_enabled = True
        self.force_endpoint_cache = False
        self.force_endpoint_server = False
        self.endpoint_cache_file = ''
        self.raw_endpoint_cache_time = '3600'

    @property
    def server_url(self):
        return "http://%s:%s/" % (self.rpc_hostname, self.rpc_port)

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
                # Some values point to files. If the path is relative or uses
                # a '~' for the home directory, we will need to expand it.
                if setting in self.filepath_configs:
                    value = os.path.expanduser(value)
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
    def __init__(self):
        # Values that can be used for the auth dict
        self.admin_token = None
        self.username = None
        self.organization = None
        self.password = None
        self.token = None
        # Whether we can prompt for a password or not
        self.allow_prompt_password = False
        # This is just to track what type of authentication we're doing
        # available options are "password", "token", "admin-token", "invalid"
        self.auth_strategy = {
            "invalid": self.auth_invalid,
            "admin-token": self.auth_admin_token,
            "token": self.auth_token,
            "password": self.auth_password
        }

    def load_from_config(self, config):
        self.admin_token = config.admin_token
        self.username = config.username
        self.organization = config.organization
        self.password = config.password
        self.token = config.token
        self.allow_prompt_password = config.prompt_password

    def prompt_for_password(self):
        self.password = getpass()

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
        if self.allow_prompt_password:
            # If we're allowed to ask for a password, then do so, thus
            # fufilling the requirements for password authentication
            # TODO: This will need to be refactored, since 'get_auth_strategy'
            # should be entirely read-only, so it shoudln't be adding/changing
            # any data. The prompt for a password should be a reaction to the
            # the auth strategy being put in an invalid state
            self.prompt_for_password()
            return "password"
        # Since no other authentication type has matched yet, if the
        # requirements for password authentication are fufilled, then we have
        # incomplete authentication information
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
    def __init__(self, config, server_connection):
        self.config = config
        self.endpoints = None
        self.server_connection = server_connection

    def load(self):
        if self.from_cache():
            output = self.load_from_file()
            self.endpoints = output
            # TODO: We should eventually return an output object from
            # loadFromFile. Then make sure that if it failed, we failover to
            # loading from the server (maybe?)
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

    def from_cache(self):
        # Are we even caching?
        if not self.config.endpoint_cache_enabled:
            return False
        # consider forced sources first
        if self.config.force_endpoint_cache:
            return True
        if self.config.force_endpoint_server:
            return False
        # Endpoint caching is enabled, but the source hasn't been forced
        # so we need to figure out if we should pull from the cache or not
        try:
            cache_last_mod_time = os.stat(self.config.endpoint_cache_file).st_mtime
        except OSError:
            # Failed to read from the file, load from server
            print "Failed to read endpoint cache file: %s" % self.config.endpoint_cache_file
            # TODO: Libraries shouldn't print! (I thought this was a library,
            # not a printing press! :P)
            return False
        time_delta = time.time() - cache_last_mod_time
        # If it has been longer since the cache was updated than is
        # configured, then we need to load from server
        if time_delta >= self.config.raw_endpoint_cache_time:
            return False
        return True

    def load_from_server(self):
        """Retrieves the available endpoints from the server.

        Here we're manually creating an RPCEndpoint with the hardcoded name
        'availableendpoints'. We can get away with this because this will
        always exist on the server.
        """
        return RPCEndpoint(self.config, 'availableendpoints').execute(self.server_connection)

    def load_from_file(self):
        """Retrieves the available endpoints from the cache
        """
        # This will throw an error if the content of file cannot be literally
        # evaluated. This is good for here, but should be caught in the
        # cli tool
        file_content = open(self.config.endpoint_cache_file, 'r').read()
        return ast.literal_eval(file_content)

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
