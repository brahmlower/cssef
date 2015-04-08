from rest_framework.status import HTTP_201_CREATED
from django.test import TestCase
from django.test import Client
import json

URL_PREFIX = "/"

def prefixedUrl(url):
	return URL_PREFIX + url

class Competitions(TestCase):
	def setUp(self):
		pass

	def testListCompetitions(self):
		client = Client()
		response = client.get('%scompetitions.json' % URL_PREFIX)
		self.assertEqual(response.content, "[]")

	def testExistingCompetition(self):
		client = Client()
		postData = {'name': 'New Competition', 'url': 'new_competition'}
		response = client.post(prefixedUrl('competitions.json'), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		content = json.loads(response.content)
		competitionId = content['competitionId']
		response = client.get(prefixedUrl('competitions/%s.json' % competitionId))
		content = json.loads(response.content)
		self.assertEqual(content['competitionId'], competitionId)

	def testAbsentCompetition(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/02.json'))
		self.assertEqual(response.content, "")

	def testCreateCompetition(self):
		client = Client()
		postData = {'name': 'New Competition', 'url': 'new_competition'}
		response = client.post(prefixedUrl('competitions.json'), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)

class Teams(TestCase):
	def setUp(self):
		client = Client()
		postData = {'name': 'New Competition', 'url': 'new_competition'}
		response = client.post(prefixedUrl('competitions.json'), postData)
		content = json.loads(response.content)
		self.competitionId = content['competitionId']

	def testListTeams(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/teams.json' % self.competitionId))
		self.assertEqual(response.content, "[]")

	def testExistingTeam(self):
		client = Client()
		postData = {\
			'competitionId': int(self.competitionId), \
			'teamname': 'Testing Team', \
			'username': 'testingteam', \
			'password': 'Pa$$w0rd', \
			'networkCidr': 'team1.tld'}
		response = client.post(prefixedUrl('competitions/%s/teams.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		content = json.loads(response.content)
		teamId = content['teamId']
		response = client.get(prefixedUrl('competitions/%s/teams/%s.json' % (self.competitionId, teamId)))
		content = json.loads(response.content)
		self.assertEqual(content['teamId'], teamId)

	def testAbsentTeam(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/01/teams/02.json'))
		self.assertEqual(response.content, '')

	def testCreateTeam(self):
		client = Client()
		postData = { \
			'competitionId': int(self.competitionId), \
			'teamname': 'Testing Team', \
			'username': 'testingteam', \
			'password': 'Pa$$w0rd', \
			'networkCidr': 'team1.tld'}
		response = client.post(prefixedUrl('competitions/%s/teams.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)

class Services(TestCase):
	def setUp(self):
		client = Client()
		postData = {'name': 'New Competition', 'url': 'new_competition'}
		response = client.post(prefixedUrl('competitions.json'), postData)
		content = json.loads(response.content)
		self.competitionId = content['competitionId']

	def testListServices(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/services.json' % self.competitionId))
		self.assertEqual(response.content, "[]")

	def testExistingService(self):
		client = Client()
		# Create a plugin for the service
		postData = { \
			'name': 'Test Plugin', \
			'description': 'This is a test plugin' \
			}
		response = client.post(prefixedUrl('plugins.json'), postData)
		content = json.loads(response.content)
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		# Now create the service
		postData = { \
			'competitionId': int(self.competitionId), \
			'plugin': content['pluginId'], \
			'name': 'Test SSH', \
			'description': 'A test service.', \
			'points': 100, \
			'connectIp': True, \
			'connectDisplay': "What's this?", \
			'networkLocation': 'www', \
			'defaultPort': 22}
		response = client.post(prefixedUrl('competitions/%s/services.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		content = json.loads(response.content)
		serviceId = content['serviceId']
		response = client.get(prefixedUrl('competitions/%s/services/%s.json' % (self.competitionId, serviceId)))
		content = json.loads(response.content)
		self.assertEqual(content['serviceId'], serviceId)

	def testAbsentService(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/services/2.json' % self.competitionId))
		self.assertEqual(response.content, '')

	def testCreateService(self):
		client = Client()
		# Create a plugin for the service
		postData = { \
			'name': 'Test Plugin', \
			'description': 'This is a test plugin' \
			}
		response = client.post(prefixedUrl('plugins.json'), postData)
		content = json.loads(response.content)
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		# Now create the service
		postData = { \
			'competitionId': int(self.competitionId), \
			'plugin': content['pluginId'], \
			'name': 'Test SSH', \
			'description': 'A test service.', \
			'points': 100, \
			'connectIp': True, \
			'connectDisplay': "What's this?", \
			'networkLocation': 'www', \
			'defaultPort': 22}
		response = client.post(prefixedUrl('competitions/%s/services.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)

class Scores(TestCase):
	def setUp(self):
		client = Client()
		postData = {'name': 'New Competition', 'url': 'new_competition'}
		response = client.post(prefixedUrl('competitions.json'), postData)
		content = json.loads(response.content)
		self.competitionId = content['competitionId']

	def testListScores(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/scores.json' % self.competitionId))
		self.assertEqual(response.content, "[]")

	def testExistingScore(self):
		client = Client()
		postData = { \
			'competitionId': int(self.competitionId),
			'teamId': 1, \
			'serviceId': 1, \
			'value': 100, \
			'message': 'Service is up.'}
		response = client.post(prefixedUrl('competitions/%s/scores.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		content = json.loads(response.content)
		scoreId = content['scoreId']
		response = client.get(prefixedUrl('competitions/%s/scores/%s.json' % (self.competitionId, scoreId)))
		content = json.loads(response.content)
		self.assertEqual(content['scoreId'], scoreId)

	def testAbsentScore(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/scores/2.json' % self.competitionId))
		self.assertEqual(response.content, '')

	def testCreateScore(self):
		client = Client()
		postData = { \
			'competitionId': int(self.competitionId),
			'teamId': 1, \
			'serviceId': 1, \
			'value': 100, \
			'message': 'Service is up.'}
		response = client.post(prefixedUrl('competitions/%s/scores.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)

class Injects(TestCase):
	def setUp(self):
		client = Client()
		postData = {'name': 'New Competition', 'url': 'new_competition'}
		response = client.post(prefixedUrl('competitions.json'), postData)
		content = json.loads(response.content)
		self.competitionId = content['competitionId']

	def testListInjects(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/injects.json' % self.competitionId))
		self.assertEqual(response.content, "[]")

	def testExistingInject(self):
		client = Client()
		postData = { \
			'competitionId': int(self.competitionId), \
			'manualDelivery': True, \
			'requireResponse': True, \
			'title': 'Title of Inject', \
			'body': 'Body of new inject.'}
		response = client.post(prefixedUrl('competitions/%s/injects.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		content = json.loads(response.content)
		injectId = content['injectId']
		response = client.get(prefixedUrl('competitions/%s/injects/%s.json' % (self.competitionId, injectId)))
		content = json.loads(response.content)
		self.assertEqual(content['injectId'], injectId)

	def testAbsentInject(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/injects/2.json' % self.competitionId))
		self.assertEqual(response.content, "")

	def testCreateInject(self):
		client = Client()
		postData = { \
			'competitionId': int(self.competitionId), \
			'manualDelivery': True, \
			'requireResponse': True, \
			'title': 'Title of Inject', \
			'body': 'Body of new inject.'}
		response = client.post(prefixedUrl('competitions/%s/injects.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)


class InjectResponses(TestCase):
	def setUp(self):
		client = Client()
		postData = {'name': 'New Competition', 'url': 'new_competition'}
		response = client.post(prefixedUrl('competitions.json'), postData)
		content = json.loads(response.content)
		self.competitionId = content['competitionId']

	def testListInjectResponses(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/01/injectresponses.json'))
		self.assertEqual(response.content, "[]")

	def testExistingInjectResponse(self):
		client = Client()
		# create inject
		postData = { \
			'competitionId': int(self.competitionId), \
			'manualDelivery': True, \
			'requireResponse': True, \
			'title': 'Title of Inject', \
			'body': 'Body of new inject.'}
		response = client.post(prefixedUrl('competitions/%s/injects.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		injectId = json.loads(response.content)['injectId']
		# create team
		postData = { \
			'competitionId': int(self.competitionId), \
			'teamname': 'Testing Team', \
			'username': 'testingteam', \
			'password': 'Pa$$w0rd', \
			'networkCidr': 'team1.tld'}
		response = client.post(prefixedUrl('competitions/%s/teams.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		teamId = json.loads(response.content)['teamId']
		# create inject response
		postData = { \
			'competitionId': int(self.competitionId), \
			'teamId': int(teamId), \
			'injectId': int(injectId), \
			'content': 'Testing inject response content'}
		response = client.post(prefixedUrl('competitions/%s/injectresponses.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		content = json.loads(response.content)
		injectResponseId = content['injectResponseId']
		response = client.get(prefixedUrl('competitions/%s/injectresponses/%s.json' % (self.competitionId, injectResponseId)))
		content = json.loads(response.content)
		self.assertEqual(content['injectResponseId'], injectResponseId)

	def testAbsentInjectResponse(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/injectresponses/2.json' % self.competitionId))
		self.assertEqual(response.content, '')

	def testCreateInjectResponse(self):
		client = Client()
		# create inject
		postData = { \
			'competitionId': int(self.competitionId), \
			'manualDelivery': True, \
			'requireResponse': True, \
			'title': 'Title of Inject', \
			'body': 'Body of new inject.'}
		response = client.post(prefixedUrl('competitions/%s/injects.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		injectId = json.loads(response.content)['injectId']
		# create team
		postData = { \
			'competitionId': int(self.competitionId), \
			'teamname': 'Testing Team', \
			'username': 'testingteam', \
			'password': 'Pa$$w0rd', \
			'networkCidr': 'team1.tld'}
		response = client.post(prefixedUrl('competitions/%s/teams.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		teamId = json.loads(response.content)['teamId']
		# create inject response
		postData = { \
			'competitionId': int(self.competitionId), \
			'teamId': int(teamId), \
			'injectId': int(injectId), \
			'content': 'Testing inject response content'}
		response = client.post(prefixedUrl('competitions/%s/injectresponses.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)


class IncidentResponses(TestCase):
	def setUp(self):
		client = Client()
		postData = {'name': 'New Competition', 'url': 'new_competition'}
		response = client.post(prefixedUrl('competitions.json'), postData)
		content = json.loads(response.content)
		self.competitionId = content['competitionId']

	def testListIncidentResponses(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/%s/incidentresponses.json' % self.competitionId))
		self.assertEqual(response.content, "[]")

	def testExistingIncidentResponse(self):
		client = Client()
		# create team
		postData = { \
			'competitionId': int(self.competitionId), \
			'teamname': 'Testing Team', \
			'username': 'testingteam', \
			'password': 'Pa$$w0rd', \
			'networkCidr': 'team1.tld'}
		response = client.post(prefixedUrl('competitions/%s/teams.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		teamId = json.loads(response.content)['teamId']
		# create incident response
		postData = { \
			'competitionId': int(self.competitionId), \
			'teamId': int(teamId), \
			'replyTo': -1, \
			'subject': 'Test Incident Response Subject', \
			'content': 'Testing incident response content'}
		response = client.post(prefixedUrl('competitions/%s/incidentresponses.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		content = json.loads(response.content)
		incidentResponseId = content['incidentResponseId']
		response = client.get(prefixedUrl('competitions/%s/incidentresponses/%s.json' % (self.competitionId, incidentResponseId)))
		content = json.loads(response.content)
		self.assertEqual(content['incidentResponseId'], incidentResponseId)

	def testAbsentIncidentResponse(self):
		client = Client()
		response = client.get(prefixedUrl('competitions/01/incidentresponses/02.json'))
		self.assertEqual(response.content, "")

	def testCreateIncidentResponse(self):
		client = Client()
		# create team
		postData = { \
			'competitionId': int(self.competitionId), \
			'teamname': 'Testing Team', \
			'username': 'testingteam', \
			'password': 'Pa$$w0rd', \
			'networkCidr': 'team1.tld'}
		response = client.post(prefixedUrl('competitions/%s/teams.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		teamId = json.loads(response.content)['teamId']
		# create incident response
		postData = { \
			'competitionId': int(self.competitionId), \
			'teamId': int(teamId), \
			'replyTo': -1, \
			'subject': 'Test Incident Response Subject', \
			'content': 'Testing incident response content'}
		response = client.post(prefixedUrl('competitions/%s/incidentresponses.json' % self.competitionId), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)

class Plugins(TestCase):
	def setUp(self):
		pass

	def testListPlugins(self):
		client = Client()
		response = client.get(prefixedUrl('plugins.json'))
		self.assertEqual(response.content, "[]")

	def testExistingPlugin(self):
		client = Client()
		postData = { \
			'name': 'Test Plugin', \
			'description': 'This is a test plugin' \
			}
		response = client.post(prefixedUrl('plugins.json'), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)
		content = json.loads(response.content)
		pluginId = content['pluginId']
		response = client.get(prefixedUrl('plugins/%s.json' % pluginId))
		content = json.loads(response.content)
		self.assertEqual(content['pluginId'], pluginId)

	def testAbsentPlugin(self):
		client = Client()
		response = client.get(prefixedUrl('plugins/2.json'))
		self.assertEqual(response.content, '')

	def testCreatePlugin(self):
		client = Client()
		postData = { \
			'name': 'Test Plugin', \
			'description': 'This is a test plugin' \
			}
		response = client.post(prefixedUrl('plugins.json'), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)

class Users(TestCase):
	def setUp(self):
		pass

	def testListUsers(self):
		client = Client()
		response = client.get(prefixedUrl('users.json'))
		self.assertEqual(response.content, "[]")

	def testExistingUser(self):
		client = Client()
		postData = {'username': 'TestUser', 'password': 'testUserP@sSw0rd'}
		response = client.post(prefixedUrl('users.json'), postData)
		userId = json.loads(response.content)['userId']
		response = client.get(prefixedUrl('users/%s.json' % userId))
		content = json.loads(response.content)
		self.assertEqual(content['userId'], userId)

	def testAbsentUser(self):
		client = Client()
		response = client.get(prefixedUrl('users/02.json'))
		self.assertEqual(response.content, "")

	def testCreateUser(self):
		client = Client()
		postData = {'username': 'TestUser', 'password': 'testUserP@sSw0rd'}
		response = client.post(prefixedUrl('users.json'), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)

class Organizations(TestCase):
	def setUp(self):
		pass

	def testListOrganizations(self):
		client = Client()
		response = client.get(prefixedUrl('organizations.json'))
		self.assertEqual(response.content, "[]")

	def testExistingOrganization(self):
		client = Client()
		postData = {'name': 'Test Organization'}
		response = client.post(prefixedUrl('organizations.json'), postData)
		organizationId = json.loads(response.content)['organizationId']
		response = client.get(prefixedUrl('organizations/%s.json' % organizationId))
		content = json.loads(response.content)
		self.assertEqual(content['organizationId'], organizationId)

	def testAbsentOrganization(self):
		client = Client()
		response = client.get(prefixedUrl('organizations/2.json'))
		self.assertEqual(response.content, '')

	def testCreateOrganization(self):
		client = Client()
		postData = {'name': 'Test Organization'}
		response = client.post(prefixedUrl('organizations.json'), postData)
		self.assertEqual(response.status_code, HTTP_201_CREATED)