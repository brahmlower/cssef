from cssefserver.framework.utils import databaseConnection
from cssefserver.framework.utils import handleException
from cssefserver.framework.utils import getEmptyReturnDict
from cssefserver.framework.utils import modelDel
from cssefserver.framework.utils import modelSet
from cssefserver.framework.utils import modelGet
from cssefserver.framework import CssefCeleryApp
from cssefserver.framework import dbPath
from cssefserver.modules.user import User

@CssefCeleryApp.task(name = 'userAdd')
def userAdd(organization = None, **kwargs):
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
	try:
		if not pkid:
			raise Exception
		return modelDel(User, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'userSet')
def userSet(pkid = None, **kwargs):
	try:
		if not pkid:
			raise Exception
		return modelSet(User, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'userGet')
def userGet(**kwargs):
	try:
		return modelGet(User, **kwargs)
	except Exception as e:
		return handleException(e)

endpointsDict = {
	"name": "Users",
	"author": "",
	"menuName": ["user"],
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