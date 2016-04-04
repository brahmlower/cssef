#from cssefserver import CssefCeleryApp
#from cssefserver import DatabaseConnection
#from cssefserver import config
#from celery.contrib.methods import task
#from celery import Task
from celery.app.task import Task
from cssefserver.utils import handleException
from cssefserver.utils import getEmptyReturnDict
from cssefserver.taskutils import modelDel
from cssefserver.taskutils import modelSet
from cssefserver.taskutils import modelGet
from cssefserver.account.api import Organization
from cssefserver.account.api import User
from cssefserver.account.utils import authorizeAccess

# class OrganizationTasks(object):
# 	def __init__(self, config, databaseConnection):
# 		self.config = config
# 		self.databaseConnection = databaseConnection

#@CssefCeleryApp.task(name = 'organizationAdd')
# @task(name = 'organizationAdd')
# def organizationAdd(auth, **kwargs):
# 	"""Celery task to create a new organization.

# 	Args:
# 		**kwargs: Keyword arguments to be passed onto User.fromDict()

# 	Returns:
# 		A returnDict dictionary containing the results of the API call. See
# 		getEmptyReturnDict for more information.
# 	"""
# 	try:
# 		authResult = authorizeAccess(self.databaseConnection, auth, config)
# 		if authResult is not None:
# 			return authResult
# 		organization = Organization.fromDict(self.databaseConnection, kwargs)
# 		returnDict = getEmptyReturnDict()
# 		returnDict['content'].append(organization.asDict())
# 		return returnDict
# 	except Exception as e:
# 		return handleException(e)

class OrganizationAdd(Task):
	name = 'OrganizationAdd'
	def run(self, auth, **kwargs):
		"""Celery task to create a new organization.

		Args:
			**kwargs: Keyword arguments to be passed onto User.fromDict()

		Returns:
			A returnDict dictionary containing the results of the API call. See
			getEmptyReturnDict for more information.
		"""
		try:
			authResult = authorizeAccess(self.databaseConnection, auth, config)
			if authResult is not None:
				return authResult
			organization = Organization.fromDict(self.databaseConnection, kwargs)
			returnDict = getEmptyReturnDict()
			returnDict['content'].append(organization.asDict())
			return returnDict
		except Exception as e:
			return handleException(e)

# #@CssefCeleryApp.task(name = 'organizationDel')
# @task(name = 'organizationDel')
# def organizationDel(auth, pkid = None):
# 	"""Celery task to delete an existing organization.

# 	Args:
# 		pkid (int): The ID of the organization to delete

# 	Returns:
# 		A returnDict dictionary containing the results of the API call. See
# 		getEmptyReturnDict for more information.
# 	"""
# 	try:
# 		authResult = authorizeAccess(self.databaseConnection, auth, config)
# 		if authResult is not None:
# 			return authResult
# 		if not pkid:
# 			raise Exception
# 		return modelDel(self.databaseConnection, Organization, pkid)
# 	except Exception as e:
# 		return handleException(e)

class OrganizationDel(Task):
	name = 'OrganizationDel'
	def run(self, auth, pkid = None):
		"""Celery task to delete an existing organization.

		Args:
			pkid (int): The ID of the organization to delete

		Returns:
			A returnDict dictionary containing the results of the API call. See
			getEmptyReturnDict for more information.
		"""
		try:
			authResult = authorizeAccess(self.databaseConnection, auth, config)
			if authResult is not None:
				return authResult
			if not pkid:
				raise Exception
			return modelDel(self.databaseConnection, Organization, pkid)
		except Exception as e:
			return handleException(e)

# #@CssefCeleryApp.task(name = 'organizationSet')
# @task(name = 'organizationSet')
# def organizationSet(auth, pkid = None, **kwargs):
# 	"""Celery task to edit an existing organization.

# 	Args:
# 		pkid (int): The ID of the organization to edit
# 		**kwargs: Keyword arguments for values to change in the organization

# 	Returns:
# 		A returnDict dictionary containing the results of the API call. See
# 		getEmptyReturnDict for more information.
# 	"""
# 	try:
# 		authResult = authorizeAccess(DatabaseConnection, auth, config)
# 		if authResult is not None:
# 			return authResult
# 		if not pkid:
# 			raise Exception
# 		return modelSet(self.databaseConnection, Organization, pkid, **kwargs)
# 	except Exception as e:
# 		return handleException(e)

class OrganizationSet(Task):
	name = 'OrganizationSet'
	def run(self, auth, pkid = None, **kwargs):
		"""Celery task to edit an existing organization.

		Args:
			pkid (int): The ID of the organization to edit
			**kwargs: Keyword arguments for values to change in the organization

		Returns:
			A returnDict dictionary containing the results of the API call. See
			getEmptyReturnDict for more information.
		"""
		try:
			authResult = authorizeAccess(DatabaseConnection, auth, config)
			if authResult is not None:
				return authResult
			if not pkid:
				raise Exception
			return modelSet(self.databaseConnection, Organization, pkid, **kwargs)
		except Exception as e:
			return handleException(e)

# #@CssefCeleryApp.task(name = 'organizationGet')
# @task(name = 'organizationGet')
# def organizationGet(auth, **kwargs):
# 	"""Celery task to get one or more existing organization.

# 	Args:
# 		**kwargs: Keyword arguments to filter organization by

# 	Returns:
# 		A returnDict dictionary containing the results of the API call. See
# 		getEmptyReturnDict for more information.
# 	"""
# 	try:
# 		authResult = authorizeAccess(self.databaseConnection, auth, config)
# 		if authResult is not None:
# 			return authResult
# 		return modelGet(self.databaseConnection, Organization, **kwargs)
# 	except Exception as e:
# 		return handleException(e)

class OrganizationGet(Task):
	name = 'OrganizationGet'
	def run(self, auth, **kwargs):
		"""Celery task to get one or more existing organization.

		Args:
			**kwargs: Keyword arguments to filter organization by

		Returns:
			A returnDict dictionary containing the results of the API call. See
			getEmptyReturnDict for more information.
		"""
		try:
			authResult = authorizeAccess(self.databaseConnection, auth, config)
			if authResult is not None:
				return authResult
			return modelGet(self.databaseConnection, Organization, **kwargs)
		except Exception as e:
			return handleException(e)

# class UserTasks(object):
# 	def __init__(self, config, databaseConnection):
# 		self.config = config
# 		self.databaseConnection = databaseConnection

#@CssefCeleryApp.task(name = 'userAdd')
# @task(name = 'userAdd')
# def userAdd(auth, organization = None, **kwargs):
# 	"""Celery task to create a new user.

# 	Args:
# 		organization (int): The ID of the organization the user belongs to
# 		**kwargs: Keyword arguments to be passed onto User.fromDict()

# 	Returns:
# 		A returnDict dictionary containing the results of the API call. See
# 		getEmptyReturnDict for more information.
# 	"""
# 	try:
# 		authResult = authorizeAccess(self.databaseConnection, auth, config)
# 		if authResult is not None:
# 			return authResult
# 		kwargs['organization'] = organization
# 		user = User.fromDict(self.databaseConnection, kwargs)
# 		returnDict = getEmptyReturnDict()
# 		returnDict['content'].append(user.asDict())
# 		return returnDict
# 	except Exception as e:
# 		return handleException(e)

class UserAdd(Task):
	name = 'UserAdd'
	def run(self, auth, organization = None, **kwargs):
		"""Celery task to create a new user.

		Args:
			organization (int): The ID of the organization the user belongs to
			**kwargs: Keyword arguments to be passed onto User.fromDict()

		Returns:
			A returnDict dictionary containing the results of the API call. See
			getEmptyReturnDict for more information.
		"""
		try:
			authResult = authorizeAccess(self.databaseConnection, auth, config)
			if authResult is not None:
				return authResult
			kwargs['organization'] = organization
			user = User.fromDict(self.databaseConnection, kwargs)
			returnDict = getEmptyReturnDict()
			returnDict['content'].append(user.asDict())
			return returnDict
		except Exception as e:
			return handleException(e)

# #@CssefCeleryApp.task(name = 'userDel')
# @task(name = 'userDel')
# def userDel(auth, pkid = None):
# 	"""Celery task to delete an existing user.

# 	Args:
# 		pkid (int): The ID of the user to delete

# 	Returns:
# 		A returnDict dictionary containing the results of the API call. See
# 		getEmptyReturnDict for more information.
# 	"""
# 	try:
# 		authResult = authorizeAccess(self.databaseConnection, auth, config)
# 		if authResult is not None:
# 			return authResult
# 		if not pkid:
# 			raise Exception
# 		return modelDel(self.databaseConnection, User, pkid)
# 	except Exception as e:
# 		return handleException(e)

class UserDel(Task):
	name = 'UserDel'
	def run(self, auth, pkid = None):
		"""Celery task to delete an existing user.

		Args:
			pkid (int): The ID of the user to delete

		Returns:
			A returnDict dictionary containing the results of the API call. See
			getEmptyReturnDict for more information.
		"""
		try:
			authResult = authorizeAccess(self.databaseConnection, auth, config)
			if authResult is not None:
				return authResult
			if not pkid:
				raise Exception
			return modelDel(self.databaseConnection, User, pkid)
		except Exception as e:
			return handleException(e)

# #@CssefCeleryApp.task(name = 'userSet')
# @task(name = 'userSet')
# def userSet(auth, pkid = None, **kwargs):
# 	"""Celery task to edit an existing user.

# 	Args:
# 		pkid (int): The ID of the user to edit
# 		**kwargs: Keyword arguments for values to change in the user

# 	Returns:
# 		A returnDict dictionary containing the results of the API call. See
# 		getEmptyReturnDict for more information.
# 	"""
# 	try:
# 		authResult = authorizeAccess(self.databaseConnection, auth, config)
# 		if authResult is not None:
# 			return authResult
# 		if not pkid:
# 			raise Exception
# 		return modelSet(self.databaseConnection, User, pkid, **kwargs)
# 	except Exception as e:
# 		return handleException(e)

class UserSet(Task):
	name = 'UserSet'
	def run(self, auth, pkid = None, **kwargs):
		"""Celery task to edit an existing user.

		Args:
			pkid (int): The ID of the user to edit
			**kwargs: Keyword arguments for values to change in the user

		Returns:
			A returnDict dictionary containing the results of the API call. See
			getEmptyReturnDict for more information.
		"""
		try:
			authResult = authorizeAccess(self.databaseConnection, auth, config)
			if authResult is not None:
				return authResult
			if not pkid:
				raise Exception
			return modelSet(self.databaseConnection, User, pkid, **kwargs)
		except Exception as e:
			return handleException(e)

# #@CssefCeleryApp.task(name = 'userGet')
# @task(name = 'userGet')
# def userGet(auth, **kwargs):
# 	"""Celery task to get one or more existing users.

# 	Args:
# 		**kwargs: Keyword arguments to filter users by

# 	Returns:
# 		A returnDict dictionary containing the results of the API call. See
# 		getEmptyReturnDict for more information.
# 	"""
# 	try:
# 		authResult = authorizeAccess(self.databaseConnection, auth, config)
# 		if authResult is not None:
# 			return authResult
# 		return modelGet(self.databaseConnection, User, **kwargs)
# 	except Exception as e:
# 		return handleException(e)

class UserGet(Task):
	name = 'UserGet'
	def run(self, **kwargs):
		"""Celery task to get one or more existing users.

		Args:
			**kwargs: Keyword arguments to filter users by

		Returns:
			A returnDict dictionary containing the results of the API call. See
			getEmptyReturnDict for more information.
		"""
		try:
			authResult = authorizeAccess(self.databaseConnection, auth, config)
			if authResult is not None:
				return authResult
			return modelGet(self.databaseConnection, User, **kwargs)
		except Exception as e:
			return handleException(e)

organizationEndpointsDict = {
	"name": "Organizations",
	"author": "",
	"menuName": "organization",
	"endpoints": [
		{	"name": "Add Organization",
			"celeryName": "organizationAdd",
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
			"celeryName": "organizationDel",
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
			"celeryName": "organizationSet",
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
			"celeryName": "organizationGet",
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
			"celeryName": "userAdd",
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
			"celeryName": "userDel",
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
			"celeryName": "userSet",
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
			"celeryName": "userGet",
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