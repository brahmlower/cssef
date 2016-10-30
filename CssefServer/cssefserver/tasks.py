from __future__ import absolute_import
from cssefserver.api import Organization
from cssefserver.api import User
from cssefserver.utils import EndpointOutput
from cssefserver.utils import authorize_access
from cssefserver.taskutils import CssefRPCEndpoint
from cssefserver.taskutils import model_del
from cssefserver.taskutils import model_set
from cssefserver.taskutils import model_get

class OrganizationAdd(CssefRPCEndpoint):
    name = "Organization Add"
    rpc_name = "organizationadd"
    menu_path = "organization.add"
    on_request_args = ['auth']
    def on_request(self, auth, **kwargs):
        """RPC task to create a new organization.

        Args:
            **kwargs: Keyword arguments to be passed onto User.from_dict()

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        authorize_access(self.server.database_connection, auth, self.server.config)
        organization = Organization.from_dict(self.server.database_connection, kwargs)
        content = [organization.as_dict()]
        return EndpointOutput(content=content)

class OrganizationDel(CssefRPCEndpoint):
    name = "Organization Delete"
    rpc_name = "organizationdel"
    menu_path = "organization.del"
    takes_kwargs = False
    on_request_args = ['auth', 'pkid']
    def on_request(self, auth, pkid):
        """RPC task to delete an existing organization.

        Args:
            pkid (int): The ID of the organization to delete

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        authorize_access(self.server.database_connection, auth, self.server.config)
        return model_del(Organization, self.server.database_connection, pkid)

class OrganizationSet(CssefRPCEndpoint):
    name = "Organization Set"
    rpc_name = "organizationset"
    menu_path = "organization.set"
    on_request_args = ['auth', 'pkid']
    def on_request(self, auth, pkid, **kwargs):
        """RPC task to edit an existing organization.

        Args:
            pkid (int): The ID of the organization to edit
            **kwargs: Keyword arguments for values to change in the organization

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        authorize_access(self.server.database_connection, auth, self.server.config)
        return model_set(Organization, self.server.database_connection, pkid, **kwargs)

class OrganizationGet(CssefRPCEndpoint):
    name = "Organization Get"
    rpc_name = "organizationget"
    menu_path = "organization.get"
    on_request_args = ['auth']
    def on_request(self, auth, **kwargs):
        """RPC task to get one or more existing organization.

        Args:
            **kwargs: Keyword arguments to filter organization by

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        authorize_access(self.server.database_connection, auth, self.server.config)
        return model_get(Organization, self.server.database_connection, **kwargs)

class UserAdd(CssefRPCEndpoint):
    name = "User Add"
    rpc_name = "useradd"
    menu_path = "user.add"
    on_request_args = ['auth']
    def on_request(self, auth, **kwargs):
        """RPC task to create a new user.

        Args:
            organization (int): The ID of the organization the user belongs to
            **kwargs: Keyword arguments to be passed onto User.from_dict()

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        authorize_access(self.server.database_connection, auth, self.server.config)
        user = User.from_dict(self.server.database_connection, kwargs)
        content = [user.as_dict()]
        return EndpointOutput(content=content)

class UserDel(CssefRPCEndpoint):
    name = "User Delete"
    rpc_name = "userdel"
    menu_path = "user.del"
    takes_kwargs = False
    on_request_args = ['auth', 'pkid']
    def on_request(self, auth, pkid):
        """RPC task to delete an existing user.

        Args:
            pkid (int): The ID of the user to delete

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        authorize_access(self.server.database_connection, auth, self.server.config)
        return model_del(User, self.server.database_connection, pkid)

class UserSet(CssefRPCEndpoint):
    name = "User Set"
    rpc_name = "userset"
    menu_path = "user.set"
    on_request_args = ['auth', 'pkid']
    def on_request(self, auth, pkid, **kwargs):
        """RPC task to edit an existing user.

        Args:
            pkid (int): The ID of the user to edit
            **kwargs: Keyword arguments for values to change in the user

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        authorize_access(self.server.database_connection, auth, self.server.config)
        return model_set(User, self.server.database_connection, pkid, **kwargs)

class UserGet(CssefRPCEndpoint):
    name = "User Get"
    rpc_name = "userget"
    menu_path = "user.get"
    on_request_args = ['auth']
    def on_request(self, auth, **kwargs):
        """RPC task to get one or more existing users.

        Args:
            **kwargs: Keyword arguments to filter users by

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        authorize_access(self.server.database_connection, auth, self.server.config)
        return model_get(User, self.server.database_connection, **kwargs)

class RenewToken(CssefRPCEndpoint):
    name = "Renew Token"
    rpc_name = "renewtoken"
    menu_path = "user.renewtoken"
    takes_kwargs = False
    on_request_args = ['auth']
    def on_request(self, auth):
        """RPC task to get a more up to date authentication token.

        Args:
            username: The username of the account the token belongs to
            organization: The organization id of the account the token belongs to
            token: The current token proving authentication

        Returns:
            A return_dict dictionary containing the results of the API call. The
            content field contains the new token if authentication was successful
        """
        user = authorize_access(self.server.database_connection, auth, self.server.config)
        content = [user.get_new_token()]
        return EndpointOutput(content=content)

class Login(CssefRPCEndpoint):
    name = "Login"
    rpc_name = "login"
    menu_path = "user.login"
    takes_kwargs = False
    on_request_args = ['auth']
    def on_request(self, auth):
        """RPC task to login.

        Returns:
            A return_dict dictionary containing the results of the API call. The
            content keyword will be a list containing the key for the session if
            the credentials were correct. Content will be empty if the credentials
            were incorrect, and value will be non-zero.
        """
        user = authorize_access(self.server.database_connection, auth, self.server.config)
        # The user is authenticated. Generate a key for them
        content = [user.get_new_token()]
        return EndpointOutput(content=content)

class AvailableEndpoints(CssefRPCEndpoint):
    """Provides a list of endpoint sources

    This will provide the list of raw enpoint source data, that being a list
    of dictionaries, where each dictionary is a single endpoint source
    containing information about the endpoints it provides.
    """
    name = "Available Endpoints"
    rpc_name = "availableendpoints"
    menu_path = None
    def on_request(self, *args):
        """RPC task to get all available celery endpoints.

        Returns:
            ReturnMessage: A return message where the content is a list of
            dictionaries containing information about the available endpoints.
        """
        return EndpointOutput(content=self.server.endpoint_sources)

class AvailablePlugins(CssefRPCEndpoint):
    """Provides a list of registered plugins

    This returns a list of the plugins that the server is using.
    """
    name = "Available Plugins"
    rpc_name = "availableplugins"
    menu_path = "availableplugins"
    def on_request(self, auth):
        """Get the list of plugins when the endpoint is requested

        Returns:
            ReturnMessage: A list of the plugins, where each entry is a result
            of calling ``plugin_instance.as_dict()``.
        """
        output = EndpointOutput()
        for plugin in self.server.config.installed_plugins:
            output.content.append(plugin.as_dict())
        return output

def endpoint_source():
    """Builds a dictionary defining the endpoints

    This builds an "endpoint dictionary" that defines information about the
    endpoints in this module and where their source, relative to the overall
    project.

    Returns:
        dict: Dictionary with the keys 'name' and 'endpoints'.
    """
    source_dict = {}
    source_dict['name'] = 'base'
    endpoints = []
    # Now add the endpoints to the endpoint_list
    endpoints.append(AvailableEndpoints.info_dict())
    endpoints.append(AvailablePlugins.info_dict())
    endpoints.append(OrganizationAdd.info_dict())
    endpoints.append(OrganizationDel.info_dict())
    endpoints.append(OrganizationSet.info_dict())
    endpoints.append(OrganizationGet.info_dict())
    endpoints.append(UserAdd.info_dict())
    endpoints.append(UserDel.info_dict())
    endpoints.append(UserSet.info_dict())
    endpoints.append(UserGet.info_dict())
    endpoints.append(RenewToken.info_dict())
    endpoints.append(Login.info_dict())
    source_dict['endpoints'] = endpoints
    return source_dict
