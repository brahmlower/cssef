from __future__ import absolute_import
from cssefserver.framework import CssefCeleryApp
from cssefserver.framework.utils import getEmptyReturnDict
from cssefserver.modules.user.api import endpointsDict as userEndpoints
from cssefserver.modules.competition.api import endpointsDict as competitionEndpoints
from cssefserver.modules.organization.api import endpointsDict as organizationEndpoints

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

endpointsDict = {
	"name": "Framework",
	"author": "",
	"menuName": "framework",
	"endpoints": []
}