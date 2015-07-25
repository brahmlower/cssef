#from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.test import Client
import json
import exampleData
import utils

class CompetitionsList(APITestCase):
	def setUp(self):
		self.uri = '/competitions.json'

	def testHttp405Response(self):
		response = self.client.put(self.uri, {})
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		utils.post(self, self.uri, exampleData.competitionMin)

class CompetitionDetails(APITestCase):
	def setUp(self):
		competition = utils.createCompetition(self)
		self.uri = '/competitions/%s.json' % competition['competitionId']

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
		uri = '/competitions/9000.json'
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)

class ServicesList(APITestCase):
	def setUp(self):
		competition = utils.createCompetition(self)
		self.uri = '/competitions/%s/services.json' % competition['competitionId']

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		utils.post(self, self.uri, exampleData.service)

class ServiceDetails(APITestCase):
	def setUp(self):
		self.competition = utils.createCompetition(self)
		plugin = utils.createPlugin(self)
		service = utils.createService(self)
		self.uri = '/competitions/%s/services/%s.json' % (self.competition['competitionId'], service['serviceId'])

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
		uri = '/competitions/%s/services/9000.json' % self.competition['competitionId']
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)

class TeamsList(APITestCase):
	def setUp(self):
		competition = utils.createCompetition(self)
		self.uri = '/competitions/%s/teams.json' % competition['competitionId']

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		utils.post(self, self.uri, exampleData.team)

class TeamDetails(APITestCase):
	def setUp(self):
		self.competition = utils.createCompetition(self)
		team = utils.createTeam(self)
		self.uri = '/competitions/%s/teams/%s.json' % (self.competition['competitionId'], team['teamId'])

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
		uri = '/competitions/%s/teams/9000.json' % self.competition['competitionId']
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)

class InjectsList(APITestCase):
	def setUp(self):
		competition = utils.createCompetition(self)
		self.uri = '/competitions/%s/injects.json' % competition['competitionId']

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		utils.post(self, self.uri, exampleData.inject)

class InjectDetails(APITestCase):
	def setUp(self):
		self.competition = utils.createCompetition(self)
		inject = utils.createInject(self)
		self.uri = '/competitions/%s/injects/%s.json' % (self.competition['competitionId'], inject['injectId'])

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
		uri = '/competitions/%s/injects/9000.json' % self.competition['competitionId']
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)

class IncidentResponsesList(APITestCase):
	def setUp(self):
		competition = utils.createCompetition(self)
		self.uri = '/competitions/%s/incidentresponses.json' % competition['competitionId']

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		utils.post(self, self.uri, exampleData.incidentResponse)

class IncidentResponseDetails(APITestCase):
	def setUp(self):
		self.competition = utils.createCompetition(self)
		incidentResponse = utils.createIncidentResponse(self)
		self.uri = '/competitions/%s/incidentresponses/%s.json' % (self.competition['competitionId'], incidentResponse['incidentResponseId'])

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
		uri = '/competitions/%s/incidentresponses/9000.json' % self.competition['competitionId']
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)

class ScoresList(APITestCase):
	def setUp(self):
		competition = utils.createCompetition(self)
		self.uri = '/competitions/%s/scores.json' % competition['competitionId']

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		utils.post(self, self.uri, exampleData.score)

class ScoresDetails(APITestCase):
	def setUp(self):
		self.competition = utils.createCompetition(self)
		scores = utils.createScore(self)
		self.uri = '/competitions/%s/scores/%s.json' % (self.competition['competitionId'], scores['scoreId'])

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
		uri = '/competitions/%s/scores/9000.json' % self.competition['competitionId']
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)
