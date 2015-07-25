#from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.test import Client
import json
import exampleData
import utils

class CompetitionsList(APITestCase):
	def testHttp405Response(self):
		url = '/competitions.json'
		data = {}
		response = self.client.put(url, data)
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions.json'
		utils.get(self, url)

	def testPost(self):
		url = '/competitions.json'
		utils.post(self, url, exampleData.competitionMin)

class CompetitionDetails(APITestCase):
	def setUp(self):
		utils.createCompetition(self)

	def testHttp405Response(self):
		url = '/competitions/1.json'
		utils.put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1.json'
		utils.get(self, url)

	def testPatch(self):
		url = '/competitions/1.json'
		# Request returns 400 without the description. With the description provided,
		# it will return the expected 202 status
		data = {"name": "This is a new name", "description":"new description"}
		utils.patch(self, url, data)

	def testDelete(self):
		url = '/competitions/1.json'
		utils.delete(self, url)

	def testInvalid(self):
		url = '/competitions/9000.json'
		utils.get(self, url, status_code = status.HTTP_404_NOT_FOUND)

class ServicesList(APITestCase):
	def setUp(self):
		utils.createCompetition(self)

	def testHttp405Response(self):
		url = '/competitions/1/services.json'
		utils.put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/services.json'
		utils.get(self, url)

	def testPost(self):
		url = '/competitions/1/services.json'
		utils.post(self, url, exampleData.service)

class ServiceDetails(APITestCase):
	def setUp(self):
		utils.createCompetition(self)
		utils.createPlugin(self)
		utils.createService(self)

	def testHttp405Response(self):
		url = '/competitions/1/services/1.json'
		utils.put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/services/1.json'
		utils.get(self, url)

	def testPatch(self):
		url = '/competitions/1/services/1.json'
		data = {"name": "This is a new name"}
		utils.patch(self, url, data)

	def testDelete(self):
		url = '/competitions/1/services/1.json'
		utils.delete(self, url)

	def testInvalid(self):
		url = '/competitions/1/services/9000.json'
		utils.get(self, url, status_code = status.HTTP_404_NOT_FOUND)

class TeamsList(APITestCase):
	def setUp(self):
		utils.createCompetition(self)

	def testHttp405Response(self):
		url = '/competitions/1/teams.json'
		utils.put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/teams.json'
		utils.get(self, url)

	def testPost(self):
		url = '/competitions/1/teams.json'
		utils.post(self, url, exampleData.team)

class TeamDetails(APITestCase):
	def setUp(self):
		utils.createCompetition(self)
		utils.createTeam(self)

	def testHttp405Response(self):
		url = '/competitions/1/teams/1.json'
		utils.put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/teams/1.json'
		utils.get(self, url)

	def testPatch(self):
		url = '/competitions/1/teams/1.json'
		data = {"name": "This is a new name"}
		utils.patch(self, url, data)

	def testDelete(self):
		url = '/competitions/1/teams/1.json'
		utils.delete(self, url)

	def testInvalid(self):
		url = '/competitions/1/teams/9000.json'
		utils.get(self, url, status_code = status.HTTP_404_NOT_FOUND)

class InjectsList(APITestCase):
	def setUp(self):
		utils.createCompetition(self)

	def testHttp405Response(self):
		url = '/competitions/1/injects.json'
		utils.put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/injects.json'
		utils.get(self, url)

	def testPost(self):
		url = '/competitions/1/injects.json'
		utils.post(self, url, exampleData.inject)

class InjectDetails(APITestCase):
	def setUp(self):
		utils.createCompetition(self)
		utils.createInject(self)

	def testHttp405Response(self):
		url = '/competitions/1/injects/1.json'
		utils.put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/injects/1.json'
		utils.get(self, url)

	def testPatch(self):
		url = '/competitions/1/injects/1.json'
		data = {"name": "This is a new name"}
		utils.patch(self, url, data)

	def testDelete(self):
		url = '/competitions/1/injects/1.json'
		utils.delete(self, url)

	def testInvalid(self):
		url = '/competitions/1/injects/9000.json'
		utils.get(self, url, status_code = status.HTTP_404_NOT_FOUND)

class IncidentResponsesList(APITestCase):
	def setUp(self):
		utils.createCompetition(self)

	def testHttp405Response(self):
		url = '/competitions/1/incidentresponses.json'
		utils.put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/incidentresponses.json'
		utils.get(self, url)

	def testPost(self):
		url = '/competitions/1/incidentresponses.json'
		utils.post(self, url, exampleData.incidentResponse)

class IncidentResponseDetails(APITestCase):
	def setUp(self):
		utils.createCompetition(self)
		utils.createIncidentResponse(self)

	def testHttp405Response(self):
		url = '/competitions/1/incidentresponses/1.json'
		utils.put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/incidentresponses/1.json'
		utils.get(self, url)

	def testPatch(self):
		url = '/competitions/1/incidentresponses/1.json'
		data = {"name": "This is a new name"}
		utils.patch(self, url, data)

	def testDelete(self):
		url = '/competitions/1/incidentresponses/1.json'
		utils.delete(self, url)

	def testInvalid(self):
		url = '/competitions/1/incidentresponses/9000.json'
		utils.get(self, url, status_code = status.HTTP_404_NOT_FOUND)

class ScoresList(APITestCase):
	def setUp(self):
		utils.createCompetition(self)

	def testHttp405Response(self):
		url = '/competitions/1/scores.json'
		utils.put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/scores.json'
		utils.get(self, url)

	def testPost(self):
		url = '/competitions/1/scores.json'
		utils.post(self, url, exampleData.score)

class ScoresDetails(APITestCase):
	def setUp(self):
		utils.createCompetition(self)
		utils.createScore(self)

	def testHttp405Response(self):
		url = '/competitions/1/scores/1.json'
		utils.put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/scores/1.json'
		utils.get(self, url)

	def testPatch(self):
		url = '/competitions/1/scores/1.json'
		data = {"name": "This is a new name"}
		utils.patch(self, url, data)

	def testDelete(self):
		url = '/competitions/1/scores/1.json'
		utils.delete(self, url)

	def testInvalid(self):
		url = '/competitions/1/scores/9000.json'
		utils.get(self, url, status_code = status.HTTP_404_NOT_FOUND)
