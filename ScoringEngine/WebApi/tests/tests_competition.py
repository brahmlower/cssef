#from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.test import Client
import json
import exampleData

def prefixedUrl(url):
	return "/" + url

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

def get(instance, url, status_code = status.HTTP_200_OK, content = None):
	response = instance.client.get(url)
	instance.assertEqual(response.status_code, status_code)
	if content:
		instance.assertEqual(response.content, content)
	return response

def put(instance, url, data, status_code = status.HTTP_200_OK, content = None):
	response = instance.client.put(url, data)
	instance.assertEqual(response.status_code, status_code)
	if content:
		print content
		instance.assertEqual(response.content, content)
	return response

def post(instance, url, data, status_code = status.HTTP_201_CREATED, content = None):
	response = instance.client.post(url, data, format='json')
	instance.assertEqual(response.status_code, status_code)
	if content:
		instance.assertEqual(response.content, content)
	return response

def patch(instance, url, data, status_code = status.HTTP_200_OK, content = None):
	response = instance.client.patch(url, data, format='json')
	instance.assertEqual(response.status_code, status.HTTP_200_OK)
	if content:
		instance.assertEqual(responses.content, content)
	return response

def delete(instance, url, status_code = status.HTTP_204_NO_CONTENT):
	response = instance.client.delete(url)
	instance.assertEqual(response.status_code, status_code)
	return response

def getInvalid(instance, url, status_code = status.HTTP_404_NOT_FOUND):
	response = instance.client.get(url)
	instance.assertEqual(response.content, '')
	instance.assertEqual(response.status_code, status_code)
	return response

class CompetitionsList(APITestCase):
	def testHttp405Response(self):
		url = '/competitions.json'
		data = {}
		response = self.client.put(url, data)
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions.json'
		get(self, url)

	def testPost(self):
		url = '/competitions.json'
		post(self, url, exampleData.competitionMin)

class CompetitionDetails(APITestCase):
	def setUp(self):
		createCompetition(self)

	def testHttp405Response(self):
		url = '/competitions/1.json'
		put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1.json'
		get(self, url, content = exampleData.competitionMax)

	def testPatch(self):
		url = '/competitions/1.json'
		data = {"name": "This is a new name"}
		patch(self, url, data)

	def testDelete(self):
		url = '/competitions/1.json'
		delete(self, url)

	def testInvalid(self):
		url = '/competitions/9000.json'
		getInvalid(self, url)

class ServicesList(APITestCase):
	def setUp(self):
		createCompetition(self)

	def testHttp405Response(self):
		url = '/competitions/1/services.json'
		put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/services.json'
		get(self, url)

	def testPost(self):
		url = '/competitions/1/services.json'
		post(self, url, exampleData.service)

class ServiceDetails(APITestCase):
	def setUp(self):
		createCompetition(self)
		#TODO: Create a service here

	def testHttp405Response(self):
		url = '/competitions/1/services/1.json'
		put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/services/1.json'
		get(self, url, content = exampleData.competitionMax)

	def testPatch(self):
		url = '/competitions/1/services/1.json'
		data = {"name": "This is a new name"}
		patch(self, url, data)

	def testDelete(self):
		url = '/competitions/1/services/1.json'
		delete(self, url)

	def testInvalid(self):
		url = '/competitions/1/services/9000.json'
		getInvalid(self, url)

class TeamsList(APITestCase):
	def setUp(self):
		createCompetition(self)

	def testHttp405Response(self):
		url = '/competitions/1/teams.json'
		put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/teams.json'
		get(self, url)

	def testPost(self):
		url = '/competitions/1/teams.json'
		post(self, url, exampleData.team)

class TeamDetails(APITestCase):
	def setUp(self):
		createCompetition(self)
		#TODO: Create a team here

	def testHttp405Response(self):
		url = '/competitions/1/teams/1.json'
		put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/teams/1.json'
		get(self, url, content = exampleData.competitionMax)

	def testPatch(self):
		url = '/competitions/1/teams/1.json'
		data = {"name": "This is a new name"}
		patch(self, url, data)

	def testDelete(self):
		url = '/competitions/1/teams/1.json'
		delete(self, url)

	def testInvalid(self):
		url = '/competitions/1/teams/9000.json'
		getInvalid(self, url)

class InjectsList(APITestCase):
	def setUp(self):
		createCompetition(self)

	def testHttp405Response(self):
		url = '/competitions/1/injects.json'
		put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/injects.json'
		get(self, url)

	def testPost(self):
		url = '/competitions/1/injects.json'
		post(self, url, exampleData.inject)

class InjectDetails(APITestCase):
	def setUp(self):
		createCompetition(self)
		#TODO: Create an inject here

	def testHttp405Response(self):
		url = '/competitions/1/injects/1.json'
		put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/injects/1.json'
		get(self, url, content = exampleData.competitionMax)

	def testPatch(self):
		url = '/competitions/1/injects/1.json'
		data = {"name": "This is a new name"}
		patch(self, url, data)

	def testDelete(self):
		url = '/competitions/1/injects/1.json'
		delete(self, url)

	def testInvalid(self):
		url = '/competitions/1/injects/9000.json'
		getInvalid(self, url)

class IncidentResponsesList(APITestCase):
	def setUp(self):
		createCompetition(self)

	def testHttp405Response(self):
		url = '/competitions/1/incidentresponses.json'
		put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/incidentresponses.json'
		get(self, url)

	def testPost(self):
		url = '/competitions/1/incidentresponses.json'
		post(self, url, exampleData.incidentResponse)

class IncidentResponseDetails(APITestCase):
	def setUp(self):
		createCompetition(self)
		#TODO: Create an incident response here

	def testHttp405Response(self):
		url = '/competitions/1/incidentresponses/1.json'
		put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/incidentresponses/1.json'
		get(self, url, content = exampleData.competitionMax)

	def testPatch(self):
		url = '/competitions/1/incidentresponses/1.json'
		data = {"name": "This is a new name"}
		patch(self, url, data)

	def testDelete(self):
		url = '/competitions/1/incidentresponses/1.json'
		delete(self, url)

	def testInvalid(self):
		url = '/competitions/1/incidentresponses/9000.json'
		getInvalid(self, url)

class ScoresList(APITestCase):
	def setUp(self):
		createCompetition(self)

	def testHttp405Response(self):
		url = '/competitions/1/scores.json'
		put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/scores.json'
		get(self, url)

	def testPost(self):
		url = '/competitions/1/scores.json'
		post(self, url, exampleData.score)

class ScoresDetails(APITestCase):
	def setUp(self):
		createCompetition(self)
		#TODO: Create a score here

	def testHttp405Response(self):
		url = '/competitions/1/scores/1.json'
		put(self, url, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		url = '/competitions/1/scores/1.json'
		get(self, url, content = exampleData.competitionMax)

	def testPatch(self):
		url = '/competitions/1/scores/1.json'
		data = {"name": "This is a new name"}
		patch(self, url, data)

	def testDelete(self):
		url = '/competitions/1/scores/1.json'
		delete(self, url)

	def testInvalid(self):
		url = '/competitions/1/scores/9000.json'
		getInvalid(self, url)