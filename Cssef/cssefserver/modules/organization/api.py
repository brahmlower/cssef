from cssefserver.framework.utils import databaseConnection
from cssefserver.framework.utils import handleException
from cssefserver.framework.utils import getEmptyReturnDict
from cssefserver.framework.utils import modelDel
from cssefserver.framework.utils import modelSet
from cssefserver.framework.utils import modelGet
from cssefserver.framework import CssefCeleryApp
from cssefserver.framework import dbPath
from cssefserver.modules.organization import Organization

@CssefCeleryApp.task(name = 'organizationAdd')
def organizationAdd(**kwargs):
	"""Celery task to create a new organization.

	Args:
		**kwargs: Keyword arguments to be passed onto User.fromDict()

	Returns:
		A returnDict dictionary containing the results of the API call. See
		getEmptyReturnDict for more information.
	"""
	try:
		db = databaseConnection(dbPath)
		organization = Organization.fromDict(db, kwargs)
		returnDict = getEmptyReturnDict()
		returnDict['content'].append(organization.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'organizationDel')
def organizationDel(pkid = None):
	"""Celery task to delete an existing organization.

	Args:
		pkid (int): The ID of the organization to delete

	Returns:
		A returnDict dictionary containing the results of the API call. See
		getEmptyReturnDict for more information.
	"""
	try:
		if not pkid:
			raise Exception
		return modelDel(Organization, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'organizationSet')
def organizationSet(pkid = None, **kwargs):
	"""Celery task to edit an existing organization.

	Args:
		pkid (int): The ID of the organization to edit
		**kwargs: Keyword arguments for values to change in the organization

	Returns:
		A returnDict dictionary containing the results of the API call. See
		getEmptyReturnDict for more information.
	"""
	try:
		if not pkid:
			raise Exception
		return modelSet(Organization, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'organizationGet')
def organizationGet(**kwargs):
	"""Celery task to get one or more existing organization.

	Args:
		**kwargs: Keyword arguments to filter organization by

	Returns:
		A returnDict dictionary containing the results of the API call. See
		getEmptyReturnDict for more information.
	"""
	try:
		return modelGet(Organization, **kwargs)
	except Exception as e:
		return handleException(e)

endpointsDict = {
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