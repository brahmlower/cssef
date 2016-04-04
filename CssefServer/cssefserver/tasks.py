from __future__ import absolute_import
#from celery import Task
from celery.app.task import Task
#from cssefserver import CssefCeleryApp
#from cssefserver import DatabaseConnection
#from cssefserver import plugins
from cssefserver.utils import getEmptyReturnDict
from cssefserver.account.api import User
from cssefserver.account.tasks import organizationEndpointsDict
from cssefserver.account.tasks import userEndpointsDict

from cssefserver.taskutils import logBadUserSearchResults
from cssefserver.taskutils import clientFailedLoginOutput

# class CssefTasks(object):
# 	def __init__(self, config, databaseConnection):
# 		self.config = config
# 		self.databaseConnection = databaseConnection

# #@CssefCeleryApp.task(name = 'availableEndpoints')
# @task(name = 'availableEndpoints', bind = True)
# def availableEndpoints(self):
# 	"""Celery task to get all available celery endpoints.

# 	Returns:
# 		A returnDict dictionary containing the results of the API call. The
# 		content is a list of dictionaries containing information about the
# 		available endpoints.
# 	"""
# 	returnDict = getEmptyReturnDict()
# 	returnDict['content'] = [
# 		endpointsDict,
# 		userEndpointsDict,
# 		organizationEndpointsDict
# 	]
# 	# Having this commented out will no present plugin endpoints to clients
# 	# for plugin in plugins:
# 	# 	returnDict['content'].append(plugin.tasks.endpointsDict)
# 	return returnDict

class AvailableEndpoints(Task):
	name = 'AvailableEndpoints'
	def run(self):
		"""Celery task to get all available celery endpoints.

		Returns:
			A returnDict dictionary containing the results of the API call. The
			content is a list of dictionaries containing information about the
			available endpoints.
		"""
		returnDict = getEmptyReturnDict()
		returnDict['content'] = [
			endpointsDict,
			userEndpointsDict,
			organizationEndpointsDict
		]
		# Having this commented out will not present plugin endpoints to clients
		# for plugin in plugins:
		# 	returnDict['content'].append(plugin.tasks.endpointsDict)
		return returnDict

# #@CssefCeleryApp.task(name = 'renewToken')
# @task(name = 'renewToken')
# def renewToken(self, username, organization, token):
# 	"""Celery task to get a new auth token
# 	"""
# 	#userResults = User.search(DatabaseConnection, username = username, organization = organization)
# 	userResults = User.search(self.databaseConnection, username = username, organization = organization)
# 	if len(userResults) != 1:
# 		return clientFailedLoginOutput()
# 	user = userResults[0]
# 	if not user.authenticateToken(token):
# 		# If the token is already expired, then authentication has failed.
# 		return clientFailedLoginOutput()
# 	returnDict = getEmptyReturnDict()
# 	returnDict['content'] = [user.getNewToken()]
# 	return returnDict

class RenewToken(Task):
	name = 'RenewToken'
	def run(self, username, organization, token):
		"""Celery task to get a new auth token
		"""
		#userResults = User.search(DatabaseConnection, username = username, organization = organization)
		userResults = User.search(self.databaseConnection, username = username, organization = organization)
		if len(userResults) != 1:
			return clientFailedLoginOutput()
		user = userResults[0]
		if not user.authenticateToken(token):
			# If the token is already expired, then authentication has failed.
			return clientFailedLoginOutput()
		returnDict = getEmptyReturnDict()
		returnDict['content'] = [user.getNewToken()]
		return returnDict

# #@CssefCeleryApp.task(name = 'login')
# @task(name = 'login')
# def login(self, username, password, organization, auth = None):
# 	"""Celery task to login.

# 	Returns:
# 		A returnDict dictionary containing the results of the API call. The
# 		content keyword will be a list containing the key for the session if
# 		the credentials were correct. Content will be empty if the credentials
# 		were incorrect, and value will be non-zero.
# 	"""
# 	#userResults = User.search(DatabaseConnection, username = username, organization = organization)
# 	userResults = User.search(self.databaseConnection, username = username, organization = organization)
# 	if len(userResults) != 1:
# 		logBadUserSearchResults(userResults, username, organization)
# 		# Now return a genaric login failure message to the client.
# 		# TODO: Should I maybe describe the error a little more to the user, that way
# 		# they're aware that some actually bad has happened?
# 		return clientFailedLoginOutput()
# 	# Try to verify the provided credentials
# 	user = userResults[0]
# 	if not user.authenticatePassword(password):
# 		# Authentication has failed
# 		return clientFailedLoginOutput()
# 	# The user is authenticated. Generate a key for them
# 	returnDict = getEmptyReturnDict()
# 	returnDict['content'] = [user.getNewToken()]
# 	return returnDict

class Login(Task):
	name = 'Login'
	def run(self, username, password, organization, auth = None):
		#userResults = User.search(DatabaseConnection, username = username, organization = organization)
		userResults = User.search(self.databaseConnection, username = username, organization = organization)
		if len(userResults) != 1:
			logBadUserSearchResults(userResults, username, organization)
			# Now return a genaric login failure message to the client.
			# TODO: Should I maybe describe the error a little more to the user, that way
			# they're aware that some actually bad has happened?
			return clientFailedLoginOutput()
		# Try to verify the provided credentials
		user = userResults[0]
		if not user.authenticatePassword(password):
			# Authentication has failed
			return clientFailedLoginOutput()
		# The user is authenticated. Generate a key for them
		returnDict = getEmptyReturnDict()
		returnDict['content'] = [user.getNewToken()]
		return returnDict

# def logBadUserSearchResults(numResults, username, organization):
# 	# This isn't how logging is done, but I'll get it fixed with I improve logging
# 	if numResults > 1:
# 		print "There were too many users returned"
# 	elif numResults < 1:
# 		print "There were fewer than 1 users returned."
# 	else:
# 		print "Num results was neither 1, >1, <1. You should NEVER see this message."
# 	print "Number of users: %d" % len(numResults)
# 	print "Provided username: %s" % username
# 	print "Provided organization: %s" % organization

# def clientFailedLoginOutput():
# 	returnDict = getEmptyReturnDict()
# 	returnDict['message'] = ["Incorrect username or password."]
# 	returnDict['value'] = 1
# 	return returnDict

endpointsDict = {
	"name": "Framework",
	"author": "",
	"menuName": "framework",
	"endpoints": []
}