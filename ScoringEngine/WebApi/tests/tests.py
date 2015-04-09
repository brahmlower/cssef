from rest_framework.status import HTTP_201_CREATED
from django.test import TestCase
from django.test import Client
import json

URL_PREFIX = "/"

def prefixedUrl(url):
	return URL_PREFIX + url

def submitPostData(url, data, instance = None):
	client = Client()
	response = client.post(url, data)
	if instance:
		instance.assertEqual(response.status_code, HTTP_201_CREATED)
	return json.loads(response.content)

def createCompetition(instance):
	data = {'name': 'New Competition', 'url': 'new_competition'}
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


class Competitions(TestCase):
	def setUp(self):
		pass

	def testListCompetitions(self):
		client = Client()
		response = client.get('%scompetitions.json' % URL_PREFIX)
		self.assertEqual(response.content, "[]")

	def testExistingCompetition(self):
		client = Client()
		competitionId = createCompetition(self)['competitionId']
		response = client.get(prefixedUrl('competitions/%s.json' % competitionId))
		content = json.loads(response.content)
		self.assertEqual(content['competitionId'], competitionId)

	def testAbsentCompetition(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/2.json'))
		self.assertEqual(response.content, '')

	def testCreateCompetition(self):
		createCompetition(self)

class Teams(TestCase):
	def setUp(self):
		client = Client()
		self.competitionId = createCompetition(self)['competitionId']

	def testListTeams(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/teams.json' % self.competitionId))
		self.assertEqual(response.content, "[]")

	def testExistingTeam(self):
		client = Client()
		teamId = createTeam(self, self.competitionId)['teamId']
		response = client.get(prefixedUrl('competitions/%s/teams/%s.json' % (self.competitionId, teamId)))
		content = json.loads(response.content)
		self.assertEqual(content['teamId'], teamId)

	def testAbsentTeam(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/teams/2.json' % self.competitionId))
		self.assertEqual(response.content, '')

	def testCreateTeam(self):
		createTeam(self, self.competitionId)

class Services(TestCase):
	def setUp(self):
		self.competitionId = createCompetition(self)['competitionId']
		self.pluginId = createPlugin(self)['pluginId']

	def testListServices(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/services.json' % self.competitionId))
		self.assertEqual(response.content, "[]")

	def testExistingService(self):
		client = Client()
		serviceId = createService(self, self.competitionId, self.pluginId)['serviceId']
		response = client.get(prefixedUrl('competitions/%s/services/%s.json' % (self.competitionId, serviceId)))
		content = json.loads(response.content)
		self.assertEqual(content['serviceId'], serviceId)

	def testAbsentService(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/services/2.json' % self.competitionId))
		self.assertEqual(response.content, '')

	def testCreateService(self):
		createService(self, self.competitionId, self.pluginId)

class Scores(TestCase):
	def setUp(self):
		self.competitionId = createCompetition(self)['competitionId']
		self.pluginId = createPlugin(self)['pluginId']
		self.serviceId = createService(self, self.competitionId, self.pluginId)['serviceId']
		self.teamId = createTeam(self, self.competitionId)['teamId']

	def testListScores(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/scores.json' % self.competitionId))
		self.assertEqual(response.content, "[]")

	def testExistingScore(self):
		client = Client()
		scoreId = createScore(self, self.competitionId, self.teamId, self.serviceId)['scoreId']
		response = client.get(prefixedUrl('competitions/%s/scores/%s.json' % (self.competitionId, scoreId)))
		content = json.loads(response.content)
		self.assertEqual(content['scoreId'], scoreId)

	def testAbsentScore(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/scores/2.json' % self.competitionId))
		self.assertEqual(response.content, '')

	def testCreateScore(self):
		createScore(self, self.competitionId, self.teamId, self.serviceId)

class Injects(TestCase):
	def setUp(self):
		self.competitionId = createCompetition(self)['competitionId']

	def testListInjects(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/injects.json' % self.competitionId))
		self.assertEqual(response.content, "[]")

	def testExistingInject(self):
		client = Client()
		injectId = createInject(self, self.competitionId)['injectId']
		response = client.get(prefixedUrl('competitions/%s/injects/%s.json' % (self.competitionId, injectId)))
		content = json.loads(response.content)
		self.assertEqual(content['injectId'], injectId)

	def testAbsentInject(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/injects/2.json' % self.competitionId))
		self.assertEqual(response.content, "")

	def testCreateInject(self):
		createInject(self, self.competitionId)

class InjectResponses(TestCase):
	def setUp(self):
		self.competitionId = createCompetition(self)['competitionId']
		self.teamId = createTeam(self, self.competitionId)['teamId']
		self.injectId = createInject(self, self.competitionId)['injectId']

	def testListInjectResponses(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/injectresponses.json' % self.competitionId))
		self.assertEqual(response.content, "[]")

	def testExistingInjectResponse(self):
		client = Client()
		injectResponseId = createInjectResponse(self, self.competitionId, self.teamId, self.injectId)['injectResponseId']
		response = client.get(prefixedUrl('competitions/%s/injectresponses/%s.json' % (self.competitionId, injectResponseId)))
		content = json.loads(response.content)
		self.assertEqual(content['injectResponseId'], injectResponseId)

	def testAbsentInjectResponse(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/injectresponses/2.json' % self.competitionId))
		self.assertEqual(response.content, '')

	def testCreateInjectResponse(self):
		createInjectResponse(self, self.competitionId, self.teamId, self.injectId)

class IncidentResponses(TestCase):
	def setUp(self):
		self.competitionId = createCompetition(self)['competitionId']
		self.teamId = createTeam(self, self.competitionId)['teamId']

	def testListIncidentResponses(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/incidentresponses.json' % self.competitionId))
		self.assertEqual(response.content, "[]")

	def testExistingIncidentResponse(self):
		client = Client()
		incidentResponseId = createIncidentResponse(self, self.competitionId, self.teamId)['incidentResponseId']
		response = client.get(prefixedUrl('competitions/%s/incidentresponses/%s.json' % (self.competitionId, incidentResponseId)))
		content = json.loads(response.content)
		self.assertEqual(content['incidentResponseId'], incidentResponseId)

	def testAbsentIncidentResponse(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/incidentresponses/2.json' % self.competitionId))
		self.assertEqual(response.content, '')

	def testCreateIncidentResponse(self):
		createIncidentResponse(self, self.competitionId, self.teamId)

class Plugins(TestCase):
	def setUp(self):
		pass

	def testListPlugins(self):
		client = Client()
		response = client.get(prefixedUrl('plugins.json'))
		self.assertEqual(response.content, "[]")

	def testExistingPlugin(self):
		client = Client()
		pluginId = createPlugin(self)['pluginId']
		response = client.get(prefixedUrl('plugins/%s.json' % pluginId))
		content = json.loads(response.content)
		self.assertEqual(content['pluginId'], pluginId)

	def testAbsentPlugin(self):
		client = Client()
		response = client.get(prefixedUrl('plugins/2.json'))
		self.assertEqual(response.content, '')

	def testCreatePlugin(self):
		createPlugin(self)

class Users(TestCase):
	def setUp(self):
		pass

	def testListUsers(self):
		client = Client()
		response = client.get(prefixedUrl('users.json'))
		self.assertEqual(response.content, "[]")

	def testExistingUser(self):
		client = Client()
		userId = createUser(self)['userId']
		response = client.get(prefixedUrl('users/%s.json' % userId))
		content = json.loads(response.content)
		self.assertEqual(content['userId'], userId)

	def testAbsentUser(self):
		client = Client()
		response = client.get(prefixedUrl('users/2.json'))
		self.assertEqual(response.content, '')

	def testCreateUser(self):
		createUser(self)

class Organizations(TestCase):
	def setUp(self):
		pass

	def testListOrganizations(self):
		client = Client()
		response = client.get(prefixedUrl('organizations.json'))
		self.assertEqual(response.content, "[]")

	def testExistingOrganization(self):
		client = Client()
		organizationId = createOrganization(self)['organizationId']
		response = client.get(prefixedUrl('organizations/%s.json' % organizationId))
		content = json.loads(response.content)
		self.assertEqual(content['organizationId'], organizationId)

	def testAbsentOrganization(self):
		client = Client()
		response = client.get(prefixedUrl('organizations/2.json'))
		self.assertEqual(response.content, '')

	def testCreateOrganization(self):
		createOrganization(self)