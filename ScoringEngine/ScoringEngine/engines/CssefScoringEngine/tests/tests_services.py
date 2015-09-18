from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.test import Client
from WebApi.tests import utils as webapiUtils
import utils
import exampleData
import json

class ServicesList(APITestCase):
	def setUp(self):
		self.organization = webapiUtils.createOrganization(self)
		competition = webapiUtils.createCompetition(self, organization = self.organization['organizationId'])
		self.uri = '/competitions/%s/services.json' % competition['competitionId']

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		plugin = utils.createPlugin(self)
		utils.post(self, self.uri, exampleData.service)

class ServiceDetails(APITestCase):
	def setUp(self):
		self.organization = webapiUtils.createOrganization(self)
		self.competition = webapiUtils.createCompetition(self, organization = self.organization['organizationId'])
		plugin = utils.createPlugin(self)
		service = utils.createService(self, competitionId = self.competition['competitionId'])
		self.uri = '/competitions/%s/services/%s.json' % (self.competition['competitionId'], service['serviceId'])

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPatch(self):
		data = {"name": "This is a new name"}
		utils.patch(self, self.uri, data)
		response = utils.get(self, self.uri)
		name = json.loads(response.content)['name']
		self.assertEqual(name, data['name'])

	def testDelete(self):
		utils.delete(self, self.uri)

	def testInvalid(self):
		uri = '/competitions/%s/services/9000.json' % self.competition['competitionId']
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)