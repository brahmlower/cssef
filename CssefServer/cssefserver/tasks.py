from __future__ import absolute_import
import ast
import logging
from cssefserver.utils import get_empty_return_dict
from cssefserver.utils import CssefRPCEndpoint
from cssefserver.account.api import User
from cssefserver.taskutils import log_bad_user_search_results
from cssefserver.taskutils import client_failed_login_output

class AvailableEndpoints(CssefRPCEndpoint):
    def on_request(self, *args):
        """Celery task to get all available celery endpoints.

        Returns:
            A return_dict dictionary containing the results of the API call. The
            content is a list of dictionaries containing information about the
            available endpoints.
        """
        # This is another temporary solution to an awful problem
        user_endpoint_file_content = open('/etc/cssef/userEndpointsDict.json', 'r').read()
        org_endpoint_file_content = open('/etc/cssef/organizationEndpointsDict.json', 'r').read()
        user_endpoints_dict = ast.literal_eval(user_endpoint_file_content)
        organization_endpoints_dict = ast.literal_eval(org_endpoint_file_content)


        return_dict = get_empty_return_dict()
        return_dict['content'] = [
            user_endpoints_dict,
            organization_endpoints_dict
        ]
        # Having this commented out will not present plugin endpoints to clients
        # for plugin in plugins:
        #   return_dict['content'].append(plugin.tasks.endpointsDict)
        return return_dict

class RenewToken(CssefRPCEndpoint):
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
    takesKwargs = False
    onRequestArgs = ['username', 'organization', 'password']
    def on_request(self, username, organization, password):
        """Celery task to login.

        Returns:
            A return_dict dictionary containing the results of the API call. The
            content keyword will be a list containing the key for the session if
            the credentials were correct. Content will be empty if the credentials
            were incorrect, and value will be non-zero.
        """
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
