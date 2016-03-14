from __future__ import absolute_import
from cssefserver.framework import CssefCeleryApp
from cssefserver.framework import DatabaseConnection
from cssefserver.framework.utils import getEmptyReturnDict
from cssefserver.framework.utils import Configuration
from cssefserver.modules.account import User
from cssefserver.modules.account.api import organizationEndpointsDict as organizationEndpoints
from cssefserver.modules.account.api import userEndpointsDict as userEndpoints
from cssefserver.modules.competition.api import endpointsDict as competitionEndpoints

@CssefCeleryApp.task(name = 'availableEndpoints')
def availableEndpoints():
	"""Celery task to get all available celery endpoints.

	Returns:
		A returnDict dictionary containing the results of the API call. The
		content is a list of dictionaries containing information about the
		available endpoints.
	"""
	returnDict = getEmptyReturnDict()
	returnDict['content'] = [
		endpointsDict,
		userEndpoints,
		organizationEndpoints,
		competitionEndpoints
	]
	return returnDict

@CssefCeleryApp.task(name = 'login')
def login(username, password, organization, auth = None):
	"""Celery task to login.

	Returns:
		A returnDict dictionary containing the results of the API call. The
		content keyword will be a list containing the key for the session if
		the credentials were correct. Content will be empty if the credentials
		were incorrect, and value will be non-zero.
		"""
	# config = Configuration()
	# config.loadConfigFile(config.globalConfigPath)
	# db = config.establishDatabaseConnection()
	user = User.search(DatabaseConnection, username = username, organization = organization)
	token = user[0].authenticatePassword(password)
	returnDict = getEmptyReturnDict()
	if not token:
		returnDict['message'] = ["Incorrect username or password."]
		returnDict['value'] = 1
	else:
		returnDict['content'] = [token]
	return returnDict

endpointsDict = {
	"name": "Framework",
	"author": "",
	"menuName": "framework",
	"endpoints": []
}