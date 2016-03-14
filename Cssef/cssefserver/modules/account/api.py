from cssefserver.framework import CssefCeleryApp
from cssefserver.framework.utils import Configuration
from cssefserver.framework.utils import handleException
from cssefserver.framework.utils import getEmptyReturnDict
from cssefserver.framework.utils import modelDel
from cssefserver.framework.utils import modelSet
from cssefserver.framework.utils import modelGet
from cssefserver.modules.account import Organization
from cssefserver.modules.account import User
from cssefserver.modules.account.utils import authorizeAccess

@CssefCeleryApp.task(name = 'organizationAdd')
def organizationAdd(auth, **kwargs):
	"""Celery task to create a new organization.

	Args:
		**kwargs: Keyword arguments to be passed onto User.fromDict()

	Returns:
		A returnDict dictionary containing the results of the API call. See
		getEmptyReturnDict for more information.
	"""
	config = Configuration()
	config.loadConfigFile(config.globalConfigPath)
	db = config.establishDatabaseConnection()
	authResult = authorizeAccess(auth, config)
	if authResult is not None:
		return authResult
	try:
		organization = Organization.fromDict(db, kwargs)
		returnDict = getEmptyReturnDict()
		returnDict['content'].append(organization.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'organizationDel')
def organizationDel(auth, pkid = None):
	"""Celery task to delete an existing organization.

	Args:
		pkid (int): The ID of the organization to delete

	Returns:
		A returnDict dictionary containing the results of the API call. See
		getEmptyReturnDict for more information.
	"""
	config = Configuration()
	config.loadConfigFile(config.globalConfigPath)
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelDel(Organization, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'organizationSet')
def organizationSet(auth, pkid = None, **kwargs):
	"""Celery task to edit an existing organization.

	Args:
		pkid (int): The ID of the organization to edit
		**kwargs: Keyword arguments for values to change in the organization

	Returns:
		A returnDict dictionary containing the results of the API call. See
		getEmptyReturnDict for more information.
	"""
	config = Configuration()
	config.loadConfigFile(config.globalConfigPath)
	authResult = authorizeAccess(auth, config)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelSet(Organization, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'organizationGet')
def organizationGet(auth, **kwargs):
	"""Celery task to get one or more existing organization.

	Args:
		**kwargs: Keyword arguments to filter organization by

	Returns:
		A returnDict dictionary containing the results of the API call. See
		getEmptyReturnDict for more information.
	"""
	config = Configuration()
	config.loadConfigFile(config.globalConfigPath)
	authResult = authorizeAccess(auth, config)
	if authResult is not None:
		return authResult
	try:
		return modelGet(Organization, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'userAdd')
def userAdd(auth, organization = None, **kwargs):
	"""Celery task to create a new user.

	Args:
		organization (int): The ID of the organization the user belongs to
		**kwargs: Keyword arguments to be passed onto User.fromDict()

	Returns:
		A returnDict dictionary containing the results of the API call. See
		getEmptyReturnDict for more information.
	"""
	config = Configuration()
	config.loadConfigFile(config.globalConfigPath)
	db = config.establishDatabaseConnection()
	authResult = authorizeAccess(auth, config)
	if authResult is not None:
		return authResult
	try:
		kwargs['organization'] = organization
		user = User.fromDict(db, kwargs)
		returnDict = getEmptyReturnDict()
		returnDict['content'].append(user.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'userDel')
def userDel(auth, pkid = None):
	"""Celery task to delete an existing user.

	Args:
		pkid (int): The ID of the user to delete

	Returns:
		A returnDict dictionary containing the results of the API call. See
		getEmptyReturnDict for more information.
	"""
	config = Configuration()
	config.loadConfigFile(config.globalConfigPath)
	authResult = authorizeAccess(auth, config)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelDel(User, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'userSet')
def userSet(auth, pkid = None, **kwargs):
	"""Celery task to edit an existing user.

	Args:
		pkid (int): The ID of the user to edit
		**kwargs: Keyword arguments for values to change in the user

	Returns:
		A returnDict dictionary containing the results of the API call. See
		getEmptyReturnDict for more information.
	"""
	config = Configuration()
	config.loadConfigFile(config.globalConfigPath)
	authResult = authorizeAccess(auth, config)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelSet(User, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'userGet')
def userGet(auth, **kwargs):
	"""Celery task to get one or more existing users.

	Args:
		**kwargs: Keyword arguments to filter users by

	Returns:
		A returnDict dictionary containing the results of the API call. See
		getEmptyReturnDict for more information.
	"""
	config = Configuration()
	config.loadConfigFile(config.globalConfigPath)
	authResult = authorizeAccess(auth, config)
	if authResult is not None:
		return authResult
	try:
		return modelGet(User, **kwargs)
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