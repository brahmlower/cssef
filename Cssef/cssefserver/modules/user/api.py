from cssefserver.framework.utils import databaseConnection
from cssefserver.framework.utils import handleException
from cssefserver.framework.utils import getEmptyReturnDict
from cssefserver.framework.utils import modelDel
from cssefserver.framework.utils import modelSet
from cssefserver.framework.utils import modelGet
from cssefserver.framework import CssefCeleryApp
from cssefserver.framework import dbPath
from cssefserver.modules.organization import Organization
from cssefserver.modules.user import User

@CssefCeleryApp.task(name = 'userAdd')
def userAdd(organization = None, **kwargs):
	"""Celery task to create a new user.

	Args:
		organization (int): The ID of the organization the user belongs to
		**kwargs: Keyword arguments to be passed onto User.fromDict()

	Returns:
		A returnDict dictionary containing the results of the API call. See
		getEmptyReturnDict for more information.
	"""
	try:
		db = databaseConnection(dbPath)
		organization = Organization.fromDatabase(db, organization)
		user = organization.createMember(kwargs)
		returnDict = getEmptyReturnDict()
		returnDict['content'].append(user.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'userDel')
def userDel(pkid = None):
	"""Celery task to delete an existing user.

	Args:
		pkid (int): The ID of the user to delete

	Returns:
		A returnDict dictionary containing the results of the API call. See
		getEmptyReturnDict for more information.
	"""
	try:
		if not pkid:
			raise Exception
		return modelDel(User, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'userSet')
def userSet(pkid = None, **kwargs):
	"""Celery task to edit an existing user.

	Args:
		pkid (int): The ID of the user to edit
		**kwargs: Keyword arguments for values to change in the user

	Returns:
		A returnDict dictionary containing the results of the API call. See
		getEmptyReturnDict for more information.
	"""
	try:
		if not pkid:
			raise Exception
		return modelSet(User, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'userGet')
def userGet(**kwargs):
	"""Celery task to get one or more existing users.

	Args:
		**kwargs: Keyword arguments to filter users by

	Returns:
		A returnDict dictionary containing the results of the API call. See
		getEmptyReturnDict for more information.
	"""
	try:
		return modelGet(User, **kwargs)
	except Exception as e:
		return handleException(e)

endpointsDict = {
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