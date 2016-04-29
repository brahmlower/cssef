from cssefserver.utils import get_empty_return_dict
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
        """Celery task to create a new organization.

        Args:
            **kwargs: Keyword arguments to be passed onto User.from_dict()

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        try:
            authorize_access(self.database_connection, auth, self.config)
        except CssefException as err:
            return err.as_return_dict()
        organization = Organization.from_dict(self.database_connection, kwargs)
        return_dict = get_empty_return_dict()
        return_dict['content'].append(organization.as_dict())
        return return_dict

class OrganizationDel(CssefRPCEndpoint):
    name = "Organization Delete"
    rpc_name = "organizationdel"
    menu_path = "organization.del"
    takesKwargs = False
    onRequestArgs = ['auth', 'pkid']
    def on_request(self, auth, pkid):
        """Celery task to delete an existing organization.

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
        """Celery task to edit an existing organization.

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
        """Celery task to get one or more existing organization.

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
        """Celery task to create a new user.

        Args:
            organization (int): The ID of the organization the user belongs to
            **kwargs: Keyword arguments to be passed onto User.from_dict()

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        try:
            authorize_access(self.database_connection, auth, self.config)
        except CssefException as err:
            return err.as_return_dict()
        #kwargs['organization'] = organization
        user = User.from_dict(self.database_connection, kwargs)
        return_dict = get_empty_return_dict()
        return_dict['content'].append(user.as_dict())
        return return_dict

class UserDel(CssefRPCEndpoint):
    name = "User Delete"
    rpc_name = "userdel"
    menu_path = "user.del"
    takesKwargs = False
    onRequestArgs = ['auth', 'pkid']
    def on_request(self, auth, pkid):
        """Celery task to delete an existing user.

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
        """Celery task to edit an existing user.

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
        """Celery task to get one or more existing users.

        Args:
            **kwargs: Keyword arguments to filter users by

        Returns:
            A return_dict dictionary containing the results of the API call. See
            get_empty_return_dict for more information.
        """
        authorize_access(self.database_connection, auth, self.config)
        return model_get(User, self.database_connection, **kwargs)

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
    source_dict['endpoints'] = endpoints
    return source_dict
