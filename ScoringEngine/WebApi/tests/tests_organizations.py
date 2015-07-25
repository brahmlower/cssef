from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.test import Client
import json
import exampleData
import utils

class OrganizationsList(APITestCase):
	def setUp(self):
		utils.createOrganization(self)
		self.url = '/organizations.json'

	def testHttp405Response(self):
		utils.put(self, self.url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.url)

	def testPost(self):
		utils.post(self, self.url, exampleData.organization)

class OrganizationDetails(APITestCase):
	def setUp(self):
		organization = utils.createOrganization(self)
		self.url = '/organizations/%s.json' % organization['organizationId']

	def testHttp405Response(self):
		utils.put(self, self.url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.url)

	def testPatch(self):
		data = {"name": "This is a new name"}
		utils.patch(self, self.url, data)

	def testDelete(self):
		utils.delete(self, self.url)

	def testInvalid(self):
		url = '/organizations/9000.json'
		utils.get(self, url, status_code = status.HTTP_404_NOT_FOUND)

class MembersList(APITestCase):
	def setUp(self):
		organization = utils.createOrganization(self)
		utils.createUser(self)
		self.url = '/organizations/%s/members.json' % organization['organizationId']

	def testHttp405Response(self):
		utils.put(self, self.url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.url)

	def testPost(self):
		utils.post(self, self.url, exampleData.user)

class MemberDetails(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		self.user = utils.createUser(self)
		self.url = '/organizations/%s/members/%s.json' % (self.organization['organizationId'], self.user['userId'])

	def testHttp405Response(self):
		utils.put(self, self.url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.url)

	def testPatch(self):
		data = {"name": "This is a new name"}
		utils.patch(self, self.url, data)

	def testDelete(self):
		utils.delete(self, self.url)

	def testInvalid(self):
		url = '/organizations/%s/members/9000.json' % self.organization['organizationId']
		utils.get(self, url, status_code = status.HTTP_404_NOT_FOUND)