from __future__ import absolute_import
import ast
import logging
from cssefserver.utils import get_empty_return_dict
from cssefserver.utils import CssefRPCEndpoint
from cssefserver.account.api import User
from cssefserver.taskutils import log_bad_user_search_results
from cssefserver.taskutils import client_failed_login_output

class AvailableEndpoints(CssefRPCEndpoint):
    name = "Available Endpoints"
    rpc_name = "availableendpoints"
    menu_path = None
    def on_request(self, *args):
        """Celery task to get all available celery endpoints.

        Returns:
            A return_dict dictionary containing the results of the API call. The
            content is a list of dictionaries containing information about the
            available endpoints.
        """
        return_dict = get_empty_return_dict()
        return_dict['content'] = self.config.endpoint_sources
        return return_dict

class AvailablePlugins(CssefRPCEndpoint):
    name = "Available Plugins"
    rpc_name = "availableplugins"
    menu_path = "availableplugins"
    def on_request(self, auth):
        """Celery task to get all available competition plugins.

        Returns:
            A return_dict dictionary containing the results of the API call. The
            content is a list of dictionaries containing information about the
            available endpoints.
        """
        return_dict = get_empty_return_dict()
        plugin_dict_list = []
        for i in self.config.installed_plugins:
            plugin_dict_list.append(i.as_dict())
        return_dict['content'] = plugin_dict_list
        return return_dict

class RenewToken(CssefRPCEndpoint):
    name = "Renew Token"
    rpc_name = "renewtoken"
    menu_path = "renewtoken"
    takesKwargs = False
    onRequestArgs = ['username', 'organization', 'token']
    def on_request(self, username, organization, token):
        """Celery task to get a new auth token
        """
        user_results = User.search(self.database_connection, username=username, \
            organization=organization)
        if len(user_results) != 1:
            return client_failed_login_output()
        user = user_results[0]
        if not user.authenticate_token(token):
            # If the token is already expired, then authentication has failed.
            return client_failed_login_output()
        return_dict = get_empty_return_dict()
        return_dict['content'] = [user.get_new_token()]
        return return_dict

class Login(CssefRPCEndpoint):
    name = "Login"
    rpc_name = "login"
    menu_path = "login"
    takesKwargs = False
    onRequestArgs = ['auth']
    def on_request(self, auth):
        """Celery task to login.

        Returns:
            A return_dict dictionary containing the results of the API call. The
            content keyword will be a list containing the key for the session if
            the credentials were correct. Content will be empty if the credentials
            were incorrect, and value will be non-zero.
        """
        username = auth.pop('username')
        password = auth.pop('password')
        organization = auth.pop('organization')
        user_results = User.search(self.database_connection, username=username, \
            organization=organization)
        if len(user_results) != 1:
            log_bad_user_search_results(user_results, username, organization)
            # Now return a genaric login failure message to the client.
            # TODO: Should I maybe describe the error a little more to the user, that way
            # they're aware that some actually bad has happened?
            return client_failed_login_output()
        user = user_results[0]
        # Try to verify the provided credentials
        if not user.authenticate_password(password):
            # Authentication has failed
            logging.info("Failed authentication attempt for '%s' with organization '%s'." % (username, organization))
            return client_failed_login_output()
        logging.info("Successful authentication for '%s' with organization '%s'." % (username, organization))
        # The user is authenticated. Generate a key for them
        return_dict = get_empty_return_dict()
        return_dict['content'] = [user.get_new_token()]
        return return_dict

def endpoint_source():
    source_dict = {}
    source_dict['name'] = 'base'
    endpoints = []
    # Now add the endpoints to the endpoint_list
    endpoints.append(AvailableEndpoints.info_dict())
    endpoints.append(AvailablePlugins.info_dict())
    endpoints.append(RenewToken.info_dict())
    endpoints.append(Login.info_dict())
    source_dict['endpoints'] = endpoints
    return source_dict
