from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.test import Client
import exampleData
import utils

class OrganizationsList(APITestCase):
	def setUp(self):
		utils.createOrganization(self)
		self.uri = '/organizations.json'

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		utils.post(self, self.uri, exampleData.organization)

class OrganizationDetails(APITestCase):
	def setUp(self):
		organization = utils.createOrganization(self)
		self.uri = '/organizations/%s.json' % organization['organizationId']

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPatch(self):
		data = {"name": "This is a new name"}
		utils.patch(self, self.uri, data)

	def testDelete(self):
		utils.delete(self, self.uri)

	def testInvalid(self):
		uri = '/organizations/9000.json'
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)

class MembersList(APITestCase):
	def setUp(self):
		organization = utils.createOrganization(self)
		utils.createUser(self, organizationId = organization['organizationId'])
		self.uri = '/organizations/%s/members.json' % organization['organizationId']

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		utils.post(self, self.uri, exampleData.user)

class MemberDetails(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		self.user = utils.createUser(self, organizationId = self.organization['organizationId'])
		self.uri = '/organizations/%s/members/%s.json' % (self.organization['organizationId'], self.user['userId'])

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPatch(self):
		data = {"name": "This is a new name"}
		utils.patch(self, self.uri, data)

	def testDelete(self):
		utils.delete(self, self.uri)

	def testInvalid(self):
		uri = '/organizations/%s/members/9000.json' % self.organization['organizationId']
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)

class CompetitionsList(APITestCase):
	def setUp(self):
		organization = utils.createOrganization(self)
		competition = utils.createCompetition(self, organization = organization['organizationId'])
		self.uri = '/organizations/%s/competitions.json' % organization['organizationId']

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		utils.post(self, self.uri, exampleData.competitionMin)

class CompetitionsDetails(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		self.competition = utils.createCompetition(self, organization = self.organization['organizationId'])
		self.uri = '/organizations/%s/competitions/%s.json' % (self.organization['organizationId'], self.competition['competitionId'])

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPatch(self):
		# Request returns 400 without the description. With the description provided,
		# it will return the expected 202 status
		data = {"name": "This is a new name", "description":"new description"}
		utils.patch(self, self.uri, data)

	def testDelete(self):
		utils.delete(self, self.uri)

	def testInvalid(self):
		uri = '/organizations/%s/competitions/9000.json' % self.organization['organizationId']
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)

class CompetitionLimits(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)

	def testLessMax(self):
		testLimit = exampleData.organization['maxCompetitions'] - 1
		for i in range(testLimit):
			utils.createCompetition(self, organization = self.organization['organizationId'])

	def testEqualsMax(self):
		testLimit = exampleData.organization['maxCompetitions'] - 1
		for i in range(testLimit):
			utils.createCompetition(self, organization = self.organization['organizationId'])

	def testMoreMax(self):
		testLimit = exampleData.organization['maxCompetitions']
		for i in range(testLimit):
			utils.createCompetition(self, organization = self.organization['organizationId'])
		utils.createCompetition(self, status_code = status.HTTP_403_FORBIDDEN, organization = self.organization['organizationId'])

class MemberLimits(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)

	def testLessMax(self):
		testLimit = exampleData.organization['maxMembers'] - 1
		for i in range(testLimit):
			utils.createUser(self, organizationId = self.organization['organizationId'])

	def testEqualsMax(self):
		testLimit = exampleData.organization['maxCompetitions'] - 1
		for i in range(testLimit):
			utils.createUser(self, organizationId = self.organization['organizationId'])

	def testMoreMax(self):
		testLimit = exampleData.organization['maxCompetitions']
		for i in range(testLimit):
			utils.createUser(self, organizationId = self.organization['organizationId'])
		utils.createUser(self, status_code = status.HTTP_403_FORBIDDEN, organizationId = self.organization['organizationId'])