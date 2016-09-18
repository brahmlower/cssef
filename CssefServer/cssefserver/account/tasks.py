#from cssefserver.utils import get_empty_return_dict
from cssefserver.utils import EndpointOutput
from cssefserver.utils import CssefRPCEndpoint
from cssefserver.taskutils import model_del
from cssefserver.taskutils import model_set
from cssefserver.taskutils import model_get
from cssefserver.errors import CssefException
from cssefserver.account.api import Organization
from cssefserver.account.api import User
from cssefserver.account.utils import authorize_access

class OrganizationAdd(CssefRPCEndpoint):
    name = "Organization Add"
    rpc_name = "organizationadd"
    menu_path = "organization.add"
    onRequestArgs = ['auth']
    def on_request(self, auth, **kwargs):
        """RPC task to create a new organization.

        Args:
            **kwargs: Keyword arguments to be passed onto User.from_dict()

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        authorize_access(self.database_connection, auth, self.config)
        organization = Organization.from_dict(self.database_connection, kwargs)
        content = [organization.as_dict()]
        return EndpointOutput(content = content)

class OrganizationDel(CssefRPCEndpoint):
    name = "Organization Delete"
    rpc_name = "organizationdel"
    menu_path = "organization.del"
    takesKwargs = False
    onRequestArgs = ['auth', 'pkid']
    def on_request(self, auth, pkid):
        """RPC task to delete an existing organization.

        Args:
            pkid (int): The ID of the organization to delete

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        authorize_access(self.database_connection, auth, self.config)
        return model_del(Organization, self.database_connection, pkid)

class OrganizationSet(CssefRPCEndpoint):
    name = "Organization Set"
    rpc_name = "organizationset"
    menu_path = "organization.set"
    onRequestArgs = ['auth', 'pkid']
    def on_request(self, auth, pkid, **kwargs):
        """RPC task to edit an existing organization.

        Args:
            pkid (int): The ID of the organization to edit
            **kwargs: Keyword arguments for values to change in the organization

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        authorize_access(self.database_connection, auth, self.config)
        return model_set(Organization, self.database_connection, pkid, **kwargs)

class OrganizationGet(CssefRPCEndpoint):
    name = "Organization Get"
    rpc_name = "organizationget"
    menu_path = "organization.get"
    onRequestArgs = ['auth']
    def on_request(self, auth, **kwargs):
        """RPC task to get one or more existing organization.

        Args:
            **kwargs: Keyword arguments to filter organization by

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        authorize_access(self.database_connection, auth, self.config)
        return model_get(Organization, self.database_connection, **kwargs)

class UserAdd(CssefRPCEndpoint):
    name = "User Add"
    rpc_name = "useradd"
    menu_path = "user.add"
    onRequestArgs = ['auth']
    def on_request(self, auth, **kwargs):
        """RPC task to create a new user.

        Args:
            organization (int): The ID of the organization the user belongs to
            **kwargs: Keyword arguments to be passed onto User.from_dict()

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        authorize_access(self.database_connection, auth, self.config)
        user = User.from_dict(self.database_connection, kwargs)
        content = [user.as_dict()]
        return EndpointOutput(content = content)

class UserDel(CssefRPCEndpoint):
    name = "User Delete"
    rpc_name = "userdel"
    menu_path = "user.del"
    takesKwargs = False
    onRequestArgs = ['auth', 'pkid']
    def on_request(self, auth, pkid):
        """RPC task to delete an existing user.

        Args:
            pkid (int): The ID of the user to delete

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        authorize_access(self.database_connection, auth, self.config)
        return model_del(User, self.database_connection, pkid)

class UserSet(CssefRPCEndpoint):
    name = "User Set"
    rpc_name = "userset"
    menu_path = "user.set"
    onRequestArgs = ['auth', 'pkid']
    def on_request(self, auth, pkid, **kwargs):
        """RPC task to edit an existing user.

        Args:
            pkid (int): The ID of the user to edit
            **kwargs: Keyword arguments for values to change in the user

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        authorize_access(self.database_connection, auth, self.config)
        return model_set(User, self.database_connection, pkid, **kwargs)

class UserGet(CssefRPCEndpoint):
    name = "User Get"
    rpc_name = "userget"
    menu_path = "user.get"
    onRequestArgs = ['auth']
    def on_request(self, auth, **kwargs):
        """RPC task to get one or more existing users.

        Args:
            **kwargs: Keyword arguments to filter users by

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        authorize_access(self.database_connection, auth, self.config)
        return model_get(User, self.database_connection, **kwargs)

class RenewToken(CssefRPCEndpoint):
    name = "Renew Token"
    rpc_name = "renewtoken"
    menu_path = "user.renewtoken"
    takesKwargs = False
    onRequestArgs = ['auth']
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
        user = authorize_access(self.database_connection, auth, self.config)
        content = [user.get_new_token()]
        return EndpointOutput(content = content)

class Login(CssefRPCEndpoint):
    name = "Login"
    rpc_name = "login"
    menu_path = "user.login"
    takesKwargs = False
    onRequestArgs = ['auth']
    def on_request(self, auth):
        """RPC task to login.

        Returns:
            A return_dict dictionary containing the results of the API call. The
            content keyword will be a list containing the key for the session if
            the credentials were correct. Content will be empty if the credentials
            were incorrect, and value will be non-zero.
        """
        user = authorize_access(self.database_connection, auth, self.config)
        # The user is authenticated. Generate a key for them
        content = [user.get_new_token()]
        return EndpointOutput(content = content)

def endpoint_source():
    source_dict = {}
    source_dict['name'] = 'account'
    endpoints = []
    # Now add the endpoints to the endpoint_list
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
