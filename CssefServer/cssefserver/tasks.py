from __future__ import absolute_import
from cssefserver import CssefCeleryApp
from cssefserver import DatabaseConnection
from cssefserver import plugins
from cssefserver.utils import getEmptyReturnDict
from cssefserver.account.api import User
from cssefserver.account.tasks import organizationEndpointsDict as organizationEndpoints
from cssefserver.account.tasks import userEndpointsDict as userEndpoints

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
		organizationEndpoints
	]
	for plugin in plugins:
		returnDict['content'].append(plugin.tasks.endpointsDict)
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
	user = User.search(DatabaseConnection, username = username, organization = organization)
	if len(user) != 1:
		if len(user) > 1:
			# This isn't how loggins is done, but I'll get it fixed with I improve logging
			print "There were too many users returned."
			print "Number of users: %d" % len(user)
			print "Provided username: %s" % username
			print "Provided organization: %s" % organization
		elif len(user) < 1:
			print "There were fewer than 1 users returned."
			print "Number of users: %d" % len(user)
			print "Provided username: %s" % username
			print "Provided organization: %s" % organization
		# Now return a genaric login failure message to the client.
		# TODO: Should I maybe describe the error a little more to the user, that way
		# they're aware that some actually bad has happened?
		return clientFailedLoginOutput()
	token = user[0].authenticatePassword(password)
	returnDict = getEmptyReturnDict()
	if not token:
		return clientFailedLoginOutput()
	else:
		returnDict['content'] = [token]
	return returnDict

def clientFailedLoginOutput():
	returnDict = getEmptyReturnDict()
	returnDict['message'] = ["Incorrect username or password."]
	returnDict['value'] = 1
	return returnDict

endpointsDict = {
	"name": "Framework",
	"author": "",
	"menuName": "framework",
	"endpoints": []
}