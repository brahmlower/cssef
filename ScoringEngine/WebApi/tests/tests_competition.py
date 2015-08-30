from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.test import Client
import exampleData
import utils
import json

class CompetitionsList(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		self.uri = '/competitions.json'

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

class CompetitionDetails(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		competition = utils.createCompetition(self, organization = self.organization['organizationId'])
		self.uri = '/competitions/%s.json' % competition['competitionId']

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	# Doesn't accept PATCH option at /competition/%s.json

	# def testPatch(self):
	# 	# Request returns 400 without the description. With the description provided,
	# 	# it will return the expected 202 status
	# 	data = {"name": "This is a new name", "description":"new description"}
	# 	utils.patch(self, self.uri, data)
	# 	response = utils.get(self, self.uri)
	# 	name = json.loads(response.content)['name']
	# 	self.assertEqual(name, data['name'])

	def testInvalid(self):
		uri = '/competitions/9000.json'
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)

class ServicesList(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		competition = utils.createCompetition(self, organization = self.organization['organizationId'])
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
		self.organization = utils.createOrganization(self)
		self.competition = utils.createCompetition(self, organization = self.organization['organizationId'])
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

class TeamsList(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		competition = utils.createCompetition(self, organization = self.organization['organizationId'])
		self.uri = '/competitions/%s/teams.json' % competition['competitionId']

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		utils.post(self, self.uri, exampleData.team)

class TeamDetails(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		self.competition = utils.createCompetition(self, organization = self.organization['organizationId'])
		team = utils.createTeam(self, competitionId = self.competition['competitionId'])
		self.uri = '/competitions/%s/teams/%s.json' % (self.competition['competitionId'], team['teamId'])

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
		uri = '/competitions/%s/teams/9000.json' % self.competition['competitionId']
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)

class InjectsList(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		competition = utils.createCompetition(self, organization = self.organization['organizationId'])
		self.uri = '/competitions/%s/injects.json' % competition['competitionId']

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		utils.post(self, self.uri, exampleData.inject)

class InjectDetails(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		self.competition = utils.createCompetition(self, organization = self.organization['organizationId'])
		inject = utils.createInject(self, competitionId = self.competition['competitionId'])
		self.uri = '/competitions/%s/injects/%s.json' % (self.competition['competitionId'], inject['injectId'])

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPatch(self):
		data = {"title": "This is a new title"}
		utils.patch(self, self.uri, data)
		response = utils.get(self, self.uri)
		title = json.loads(response.content)['title']
		self.assertEqual(title, data['title'])

	def testDelete(self):
		utils.delete(self, self.uri)

	def testInvalid(self):
		uri = '/competitions/%s/injects/9000.json' % self.competition['competitionId']
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)

class InjectResponsesList(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		competition = utils.createCompetition(self, organization = self.organization['organizationId'])
		self.uri = '/competitions/%s/injectresponses.json' % competition['competitionId']

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		utils.post(self, self.uri, exampleData.injectResponse)

class InjectResponseDetails(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		self.competition = utils.createCompetition(self, organization = self.organization['organizationId'])
		self.team = utils.createTeam(self, competitionId = self.competition['competitionId'])
		injectResponse = utils.createInjectResponse(self, competitionId = self.competition['competitionId'], teamId = self.team['teamId'])
		self.uri = '/competitions/%s/injectresponses/%s.json' % (self.competition['competitionId'], injectResponse['injectResponseId'])

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPatch(self):
		data = {"content": "This is some new content"}
		utils.patch(self, self.uri, data)
		response = utils.get(self, self.uri)
		content = json.loads(response.content)['content']
		self.assertEqual(content, data['content'])

	def testDelete(self):
		utils.delete(self, self.uri)

	def testInvalid(self):
		uri = '/competitions/%s/injectresponses/9000.json' % self.competition['competitionId']
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)

class IncidentaList(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		competition = utils.createCompetition(self, organization = self.organization['organizationId'])
		self.uri = '/competitions/%s/incidents.json' % competition['competitionId']

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		utils.post(self, self.uri, exampleData.inject)

class IncidentDetails(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		self.competition = utils.createCompetition(self, organization = self.organization['organizationId'])
		incident = utils.createIncident(self, competitionId = self.competition['competitionId'])
		self.uri = '/competitions/%s/incidents/%s.json' % (self.competition['competitionId'], incident['incidentId'])

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPatch(self):
		data = {"subject": "This is a new subject"}
		utils.patch(self, self.uri, data)
		response = utils.get(self, self.uri)
		subject = json.loads(response.content)['subject']
		self.assertEqual(subject, data['subject'])

	def testDelete(self):
		utils.delete(self, self.uri)

	def testInvalid(self):
		uri = '/competitions/%s/incidents/9000.json' % self.competition['competitionId']
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)

class IncidentResponsesList(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		competition = utils.createCompetition(self, organization = self.organization['organizationId'])
		self.uri = '/competitions/%s/incidentresponses.json' % competition['competitionId']

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		utils.post(self, self.uri, exampleData.incidentResponse)

class IncidentResponseDetails(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		self.competition = utils.createCompetition(self, organization = self.organization['organizationId'])
		self.team = utils.createTeam(self, competitionId = self.competition['competitionId'])
		incidentResponse = utils.createIncidentResponse(self, competitionId = self.competition['competitionId'], teamId = self.team['teamId'])
		self.uri = '/competitions/%s/incidentresponses/%s.json' % (self.competition['competitionId'], incidentResponse['incidentResponseId'])

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPatch(self):
		data = {"subject": "This is a new subject"}
		utils.patch(self, self.uri, data)
		response = utils.get(self, self.uri)
		subject = json.loads(response.content)['subject']
		self.assertEqual(subject, data['subject'])

	def testDelete(self):
		utils.delete(self, self.uri)

	def testInvalid(self):
		uri = '/competitions/%s/incidentresponses/9000.json' % self.competition['competitionId']
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)

class ScoresList(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		competition = utils.createCompetition(self, organization = self.organization['organizationId'])
		self.uri = '/competitions/%s/scores.json' % competition['competitionId']

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		utils.post(self, self.uri, exampleData.score)

class ScoresDetails(APITestCase):
	def setUp(self):
		self.organization = utils.createOrganization(self)
		self.competition = utils.createCompetition(self, organization = self.organization['organizationId'])
		self.team = utils.createTeam(self, competitionId = self.competition['competitionId'])
		score = utils.createScore(self, competitionId = self.competition['competitionId'], teamId = self.team['teamId'])
		self.uri = '/competitions/%s/scores/%s.json' % (self.competition['competitionId'], score['scoreId'])

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPatch(self):
		data = {"message": "This is a new message"}
		utils.patch(self, self.uri, data)
		response = utils.get(self, self.uri)
		message = json.loads(response.content)['message']
		self.assertEqual(message, data['message'])

	def testDelete(self):
		utils.delete(self, self.uri)

	def testInvalid(self):
		uri = '/competitions/%s/scores/9000.json' % self.competition['competitionId']
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)
