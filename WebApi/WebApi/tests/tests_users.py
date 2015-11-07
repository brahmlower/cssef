from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.test import Client
import exampleData
import utils

class UsersList(APITestCase):
	def setUp(self):
		self.uri = '/users.json'

	def testHttp405Response(self):
		response = self.client.put(self.uri, {})
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		utils.createUser(self, uri = '/users.json', status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

class UserDetails(APITestCase):
	def setUp(self):
		# Have to create an organization, then create a user under that organization
		organization = utils.createOrganization(self)
		user = utils.createUser(self, organizationId = organization['organizationId'])
		self.uri = '/users/%s.json' % (user['userId'])

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPatch(self):
		data = {"name": "This is a new name"}
		utils.patch(self, self.uri, data)

	def testInvalid(self):
		uri = '/users/9000.json'
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)