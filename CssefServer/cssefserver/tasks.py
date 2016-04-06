from __future__ import absolute_import
from .utils import getEmptyReturnDict
from .utils import CssefRPCEndpoint
from .account.api import User
from .account.tasks import organizationEndpointsDict
from .account.tasks import userEndpointsDict
from .taskutils import logBadUserSearchResults
from .taskutils import clientFailedLoginOutput
import logging

class AvailableEndpoints(CssefRPCEndpoint):
	def __call__(self, *args):
		"""Celery task to get all available celery endpoints.

		Returns:
			A returnDict dictionary containing the results of the API call. The
			content is a list of dictionaries containing information about the
			available endpoints.
		"""
		returnDict = getEmptyReturnDict()
		returnDict['content'] = [
			userEndpointsDict,
			organizationEndpointsDict
		]
		# Having this commented out will no present plugin endpoints to clients
		# for plugin in plugins:
		# 	returnDict['content'].append(plugin.tasks.endpointsDict)
		return returnDict

class RenewToken(CssefRPCEndpoint):
	takesKwargs = False
	onRequestArgs = ['username', 'organization', 'token']
	def onRequest(self, username, organization, token):
		"""Celery task to get a new auth token
		"""
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

class Login(CssefRPCEndpoint):
	takesKwargs = False
	onRequestArgs = ['username', 'organization', 'password']
	def onRequest(self, username, organization, password):
		"""Celery task to login.

		Returns:
			A returnDict dictionary containing the results of the API call. The
			content keyword will be a list containing the key for the session if
			the credentials were correct. Content will be empty if the credentials
			were incorrect, and value will be non-zero.
		"""
		logging.info('started login')
		userResults = User.search(self.databaseConnection, username = username, organization = organization)
		if len(userResults) != 1:
			logBadUserSearchResults(userResults, username, organization)
			# Now return a genaric login failure message to the client.
			# TODO: Should I maybe describe the error a little more to the user, that way
			# they're aware that some actually bad has happened?
			return clientFailedLoginOutput()
		user = userResults[0]
		# Try to verify the provided credentials
		logging.info('got user')
		if not user.authenticatePassword(password):
			# Authentication has failed
			logging.info('user authentication failed')
			return clientFailedLoginOutput()
		logging.info('user has been authenticated')
		# The user is authenticated. Generate a key for them
		returnDict = getEmptyReturnDict()
		returnDict['content'] = [user.getNewToken()]
		logging.info('got a new token')
		return returnDict