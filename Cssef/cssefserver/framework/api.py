from __future__ import absolute_import
from cssefserver.framework import CssefCeleryApp
from cssefserver.framework.utils import getEmptyReturnDict
from cssefserver.framework.utils import Configuration
from cssefserver.modules.account import User
from cssefserver.modules.account.api import organizationEndpointsDict as organizationEndpoints
from cssefserver.modules.account.api import userEndpointsDict as userEndpoints
from cssefserver.modules.competition.api import endpointsDict as competitionEndpoints

@CssefCeleryApp.task(name = 'availableEndpoints')
def availableEndpoints():
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
	config = Configuration()
	config.loadConfigFile(config.globalConfigPath)
	db = config.establishDatabaseConnection()
	user = User.search(db, username = username, organization = organization)
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