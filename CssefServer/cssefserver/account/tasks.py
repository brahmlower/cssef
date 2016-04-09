from cssefserver.utils import handleException
from cssefserver.utils import getEmptyReturnDict
from cssefserver.utils import CssefRPCEndpoint
from cssefserver.taskutils import modelDel
from cssefserver.taskutils import modelSet
from cssefserver.taskutils import modelGet
from cssefserver.errors import CssefException
from .api import Organization
from .api import User
from .utils import authorizeAccess
import logging

class OrganizationAdd(CssefRPCEndpoint):
	takesKwargs = True
	onRequestArgs = ['auth']
	def onRequest(self, auth, **kwargs):
		"""Celery task to create a new organization.

		Args:
			**kwargs: Keyword arguments to be passed onto User.fromDict()

		Returns:
			A returnDict dictionary containing the results of the API call. See
			getEmptyReturnDict for more information.
		"""
		authResult = authorizeAccess(self.databaseConnection, auth, self.config)
		if authResult is not None:
			return authResult
		organization = Organization.fromDict(self.databaseConnection, kwargs)
		returnDict = getEmptyReturnDict()
		returnDict['content'].append(organization.asDict())
		return returnDict

class OrganizationDel(CssefRPCEndpoint):
	takesKwargs = False
	onRequestArgs = ['auth', 'pkid']
	def onRequest(self, auth, pkid):
		"""Celery task to delete an existing organization.

		Args:
			pkid (int): The ID of the organization to delete

		Returns:
			A returnDict dictionary containing the results of the API call. See
			getEmptyReturnDict for more information.
		"""
		authResult = authorizeAccess(self.databaseConnection, auth, self.config)
		if authResult is not None:
			return authResult
		if not pkid:
			raise Exception
		return modelDel(Organization, self.databaseConnection, pkid)

class OrganizationSet(CssefRPCEndpoint):
	takesKwargs = True
	onRequestArgs = ['auth', 'pkid']
	def onRequest(self, auth, pkid, **kwargs):
		"""Celery task to edit an existing organization.

		Args:
			pkid (int): The ID of the organization to edit
			**kwargs: Keyword arguments for values to change in the organization

		Returns:
			A returnDict dictionary containing the results of the API call. See
			getEmptyReturnDict for more information.
		"""
		authResult = authorizeAccess(DatabaseConnection, auth, self.config)
		if authResult is not None:
			return authResult
		if not pkid:
			raise Exception
		return modelSet(Organization, self.databaseConnection, pkid, **kwargs)

class OrganizationGet(CssefRPCEndpoint):
	takesKwargs = True
	onRequestArgs = ['auth']
	def onRequest(self, auth, **kwargs):
		"""Celery task to get one or more existing organization.

		Args:
			**kwargs: Keyword arguments to filter organization by

		Returns:
			A returnDict dictionary containing the results of the API call. See
			getEmptyReturnDict for more information.
		"""
		authResult = authorizeAccess(self.databaseConnection, auth, self.config)
		if authResult is not None:
			return authResult
		return modelGet(Organization, self.databaseConnection, **kwargs)

class UserAdd(CssefRPCEndpoint):
	takesKwargs = True
	onRequestArgs = ['auth']
	def __call__(self, auth, **kwargs):
		"""Celery task to create a new user.

		Args:
			organization (int): The ID of the organization the user belongs to
			**kwargs: Keyword arguments to be passed onto User.fromDict()

		Returns:
			A returnDict dictionary containing the results of the API call. See
			getEmptyReturnDict for more information.
		"""
		authResult = authorizeAccess(self.databaseConnection, auth, self.config)
		if authResult is not None:
			return authResult
		#kwargs['organization'] = organization
		user = User.fromDict(self.databaseConnection, kwargs)
		returnDict = getEmptyReturnDict()
		returnDict['content'].append(user.asDict())
		return returnDict

class UserDel(CssefRPCEndpoint):
	takesKwargs = False
	onRequestArgs = ['auth', 'pkid']
	def onRequest(self, auth, pkid):
		"""Celery task to delete an existing user.

		Args:
			pkid (int): The ID of the user to delete

		Returns:
			A returnDict dictionary containing the results of the API call. See
			getEmptyReturnDict for more information.
		"""
		authResult = authorizeAccess(self.databaseConnection, auth, self.config)
		if authResult is not None:
			return authResult
		if not pkid:
			raise Exception
		return modelDel(User, self.databaseConnection, pkid)

class UserSet(CssefRPCEndpoint):
	takesKwargs = True
	onRequestArgs = ['auth', 'pkid']
	def onRequest(self, auth, pkid, **kwargs):
		"""Celery task to edit an existing user.

		Args:
			pkid (int): The ID of the user to edit
			**kwargs: Keyword arguments for values to change in the user

		Returns:
			A returnDict dictionary containing the results of the API call. See
			getEmptyReturnDict for more information.
		"""
		authResult = authorizeAccess(self.databaseConnection, auth, self.config)
		if authResult is not None:
			return authResult
		if not pkid:
			raise Exception
		return modelSet(User, self.databaseConnection, pkid, **kwargs)

class UserGet(CssefRPCEndpoint):
	takesKwargs = True
	onRequestArgs = ['auth']
	def onRequest(self, auth, **kwargs):
		"""Celery task to get one or more existing users.

		Args:
			**kwargs: Keyword arguments to filter users by

		Returns:
			A returnDict dictionary containing the results of the API call. See
			getEmptyReturnDict for more information.
		"""
		authResult = authorizeAccess(self.databaseConnection, auth, self.config)
		if authResult is not None:
			return authResult
		return modelGet(User, self.databaseConnection, **kwargs)

organizationEndpointsDict = {
	"name": "Organizations",
	"author": "",
	"menuName": "organization",
	"endpoints": [
		{	"name": "Add Organization",
			"endpointName": "organizationAdd",
			"menu": ["add"],
			"arguments": [
				{	"name": "Name",
					"argument": "name",
					"keyword": True,
					"optional": False
				},
				{	"name": "URL",
					"argument": "url",
					"keyword": True,
					"optional": False
				},
				{	"name": "Description",
					"argument": "description",
					"keyword": True,
					"optional": True
				},
				{	"name": "Max Members",
					"argument": "maxMembers",
					"keyword": True,
					"optional": True
				},
				{	"name": "Max Competitions",
					"argument": "maxCompetitions",
					"keyword": True,
					"optional": True
				}
			]
		},
		{	"name": "Delete Organization",
			"endpointName": "organizationDel",
			"menu": ["del"],
			"arguments": [
				{	"name": "Organization",
					"argument": "organization",
					"keyword": True,
					"optional": False
				}
			]
		},
		{	"name": "Set Organization",
			"endpointName": "organizationSet",
			"menu": ["set"],
			"arguments": [
				{	"name": "Name",
					"argument": "name",
					"keyword": True,
					"optional": True
				},
				{	"name": "URL",
					"argument": "url",
					"keyword": True,
					"optional": True
				},
				{	"name": "Description",
					"argument": "description",
					"keyword": True,
					"optional": True
				},
				{	"name": "Max Members",
					"argument": "maxMembers",
					"keyword": True,
					"optional": True
				},
				{	"name": "Max Competitions",
					"argument": "maxCompetitions",
					"keyword": True,
					"optional": True
				}
			]
		},
		{	"name": "Get Organization",
			"endpointName": "organizationGet",
			"menu": ["get"],
			"arguments": [
				{	"name": "Name",
					"argument": "name",
					"keyword": True,
					"optional": True
				},
				{	"name": "URL",
					"argument": "url",
					"keyword": True,
					"optional": True
				},
				{	"name": "Description",
					"argument": "description",
					"keyword": True,
					"optional": True
				},
				{	"name": "Max Members",
					"argument": "maxMembers",
					"keyword": True,
					"optional": True
				},
				{	"name": "Max Competitions",
					"argument": "maxCompetitions",
					"keyword": True,
					"optional": True
				}
			]
		}
	]
}

userEndpointsDict = {
	"name": "Users",
	"author": "",
	"menuName": "user",
	"endpoints": [
		{	"name": "Add User",
			"endpointName": "userAdd",
			"menu": ["add"],
			"arguments": [
				{	"name": "Organization",
					"argument": "organization",
					"keyword": True,
					"optional": False
				},
				{	"name": "Name",
					"argument": "name",
					"keyword": True,
					"optional": False
				},
				{	"name": "Username",
					"argument": "username",
					"keyword": True,
					"optional": False
				},
				{	"name": "Password",
					"argument": "password",
					"keyword": True,
					"optional": False
				},
				{	"name": "Description",
					"argument": "description",
					"keyword": True,
					"optional": True
				}
			]
		},
		{	"name": "Delete User",
			"endpointName": "userDel",
			"menu": ["del"],
			"arguments": [
				{	"name": "User",
					"argument": "user",
					"keyword": True,
					"optional": False
				}
			]
		},
		{	"name": "Set User",
			"endpointName": "userSet",
			"menu": ["set"],
			"arguments": [
				{	"name": "Organization",
					"argument": "organization",
					"keyword": True,
					"optional": False
				},
				{	"name": "Name",
					"argument": "name",
					"keyword": True,
					"optional": False
				},
				{	"name": "Username",
					"argument": "username",
					"keyword": True,
					"optional": False
				},
				{	"name": "Password",
					"argument": "password",
					"keyword": True,
					"optional": False
				},
				{	"name": "Description",
					"argument": "description",
					"keyword": True,
					"optional": True
				}
			]
		},
		{	"name": "Get User",
			"endpointName": "userGet",
			"menu": ["get"],
			"arguments": [
				{	"name": "Organization",
					"argument": "organization",
					"keyword": True,
					"optional": False
				},
				{	"name": "Name",
					"argument": "name",
					"keyword": True,
					"optional": False
				},
				{	"name": "Username",
					"argument": "username",
					"keyword": True,
					"optional": False
				},
				{	"name": "Password",
					"argument": "password",
					"keyword": True,
					"optional": False
				},
				{	"name": "Description",
					"argument": "description",
					"keyword": True,
					"optional": True
				}
			]
		}
	]
}