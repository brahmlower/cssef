from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.test import TestCase
from rest_framework.test import APITestCase
from django.test import Client
import json

URL_PREFIX = "/"

def prefixedUrl(url):
	return URL_PREFIX + url

def submitPostData(url, data, instance = None):
	client = Client()
	response = client.post(url, data)
	if instance:
		instance.assertEqual(response.status_code, status.HTTP_201_CREATED)
	return json.loads(response.content)

def createCompetition(instance):
	data = {
		'name': 'New Competition',
		'url': 'new_competition',
		'organization': 1
		}
	url = prefixedUrl('competitions.json')
	return submitPostData(url, data, instance)

def createTeam(instance, competitionId):
	data = {
		'competitionId': int(competitionId),
		'teamname': 'Testing Team',
		'username': 'testingteam',
		'password': 'Pa$$w0rd',
		'networkCidr': 'team1.tld'
		}
	url = prefixedUrl('competitions/%s/teams.json' % str(competitionId))
	return submitPostData(url, data, instance)

def createService(instance, competitionId, pluginId):
	data = { 
		'competitionId': int(competitionId),
		'plugin': int(pluginId),
		'name': 'Test SSH',
		'description': 'A test service.',
		'points': 100,
		'connectIp': True,
		'connectDisplay': "What's this?",
		'networkLocation': 'www',
		'defaultPort': 22}
	url = prefixedUrl('competitions/%s/services.json' % str(competitionId))
	return submitPostData(url, data, instance)

def createScore(instance, competitionId, teamId, serviceId):
	data = {
		'competitionId': int(competitionId),
		'teamId': int(teamId),
		'serviceId': int(serviceId),
		'value': 100,
		'message': 'Service is up.'}
	url = prefixedUrl('competitions/%s/scores.json' % str(competitionId))
	return submitPostData(url, data, instance)

def createInject(instance, competitionId):
	data = {
		'competitionId': int(competitionId),
		'manualDelivery': True,
		'requireResponse': True,
		'title': 'Title of Inject',
		'body': 'Body of new inject.'}
	url = prefixedUrl('competitions/%s/injects.json' % str(competitionId))
	return submitPostData(url, data, instance)

def createInjectResponse(instance, competitionId, teamId, injectId):
	data = {
		'competitionId': int(competitionId),
		'teamId': int(teamId),
		'injectId': int(injectId),
		'content': 'Testing inject response content'
	}
	url = prefixedUrl('competitions/%s/injectresponses.json' % str(competitionId))
	return submitPostData(url, data, instance)

def createIncidentResponse(instance, competitionId, teamId):
	data = {
		'competitionId': int(competitionId),
		'teamId': int(teamId),
		'replyTo': -1,
		'subject': 'Test Incident Response Subject',
		'content': 'Testing incident response content'}
	url = prefixedUrl('competitions/%s/incidentresponses.json' % str(competitionId))
	return submitPostData(url, data, instance)

def createPlugin(instance):
	data = {
		'name': 'Test Plugin',
		'description': 'This is a test plugin'}
	url = prefixedUrl('plugins.json')
	return submitPostData(url, data, instance)

def createUser(instance):
	data = {
		'username': 'TestUser',
		'password': 'testUserP@sSw0rd'}
	url = prefixedUrl('users.json')
	return submitPostData(url, data, instance)

def createOrganization(instance):
	data = {
		'name': 'Test Organization'}
	url = prefixedUrl('organizations.json')
	return submitPostData(url, data, instance)

class CompetitionsRoot(APITestCase):
	'''
	This set of tests covers the functionality of /competitions.json
	Methods tested: GET, POST
	Cases to check:
		Must respond to disallowed request methods

	'''
	def testHttp405Response(self):
		url = '/competitions.json'
		data = {}
		response = self.client.put(url, data)
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions.json'
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.content, "[]")

	def testPost(self):
		url = '/competitions.json'
		data = {
			'name': 'New Competition',
			'url': 'new_competition',
			'organization': 1
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class CompetitionsDetails(APITestCase):
	def setUp(self):
		createCompetition(self)

	def testHttp405Response(self):
		url = '/competitions/1.json'
		data = {}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1.json'
		data = {
			'name': 'New Competition',
			'url': 'new_competition',
			'organization': 1
		}
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.content, data)

	def testPut(self):
		url = '/competitions/1.json'
		data = {"name": "This is a new name"}
		response = self.client.patch(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def testDelete(self):
		url = '/competitions/1.json'
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def testInvalid(self):
		url = '/competitions/9000.json'
		response = self.client.get(url)
		self.assertEqual(response.content, '')
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class CompetitionsServices(TestCase):
	def setUp(self):
		createCompetition(self)

class CompetitionsTeams(TestCase):
	def setUp(self):
		createCompetition(self)

class CompetitionsInjects(TestCase):
	def setUp(self):
		createCompetition(self)

class CompetitionsIncidents(TestCase):
	def setUp(self):
		createCompetition(self)

class CompetitionsScores(TestCase):
	def setUp(self):
		createCompetition(self)
