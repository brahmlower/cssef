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

	def testHttp405Response(self):
		url = '/organizations.json'
		utils.put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/organizations.json'
		utils.get(self, url)

	def testPost(self):
		url = '/organizations.json'
		utils.post(self, url, exampleData.team)

class OrganizationDetails(APITestCase):
	def setUp(self):
		utils.createOrganization(self)

	def testHttp405Response(self):
		url = '/organizations/1.json'
		utils.put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/organizations/1.json'
		utils.get(self, url)

	def testPatch(self):
		url = '/organizations/1.json'
		data = {"name": "This is a new name"}
		utils.patch(self, url, data)

	def testDelete(self):
		url = '/organizations/1.json'
		utils.delete(self, url)

	def testInvalid(self):
		url = '/organizations/9000.json'
		utils.get(self, url, status_code = status.HTTP_404_NOT_FOUND)