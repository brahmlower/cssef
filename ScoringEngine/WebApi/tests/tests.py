from django.test import TestCase
from django.test import Client

class Competitions(TestCase):
	def setUp(self):
		pass

	def testListCompetitions(self):
		client = Client()
		response = client.get('/api/v1/competitions.json')
		self.assertEqual(response.content, "[]")

	def testSpecificCompetition(self):
		client = Client()
		response = client.get('/api/v1/competitions/01.json')
		self.assertEqual(response.content, "[]")

	def testAbsentCompetition(self):
		client = Client()
		response = client.get('/api/v1/competitions/02.json')
		self.assertEqual(response.content, "")

class Teams(TestCase):
	def setUp(self):
		pass

	def testListTeams(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/teams.json')
		self.assertEqual(response.content, "[]")

	def testSpecificTeam(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/teams/01.json')
		self.assertEqual(response.content, "[]")

	def testAbsentTeam(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/teams/02.json')
		self.assertEqual(response.content, "")

class Services(TestCase):
	def setUp(self):
		pass

	def testListServices(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/services.json')
		self.assertEqual(response.content, "[]")

	def testSpecificService(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/services/01.json')
		self.assertEqual(response.content, "[]")

	def testAbsentService(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/services/02.json')
		self.assertEqual(response.content, "")

class Scores(TestCase):
	def setUp(self):
		pass

	def testListScores(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/scores.json')
		self.assertEqual(response.content, "[]")

	def testSpecificScore(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/scores/01.json')
		self.assertEqual(response.content, "[]")

	def testAbsentScore(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/scores/02.json')
		self.assertEqual(response.content, "")

class Injects(TestCase):
	def setUp(self):
		pass

	def testListInjects(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/injects.json')
		self.assertEqual(response.content, "[]")

	def testSpecificInject(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/injects/01.json')
		self.assertEqual(response.content, "[]")

	def testAbsentInject(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/injects/02.json')
		self.assertEqual(response.content, "")

class InjectResponses(TestCase):
	def setUp(self):
		pass

	def testListInjectResponses(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/injectresponses.json')
		self.assertEqual(response.content, "[]")

	def testSpecificInjectResponse(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/injectresponses/01.json')
		self.assertEqual(response.content, "[]")

	def testAbsentInjectResponse(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/injectresponses/02.json')
		self.assertEqual(response.content, "")

class IncidentResponses(TestCase):
	def setUp(self):
		pass

	def testListIncidentResponses(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/incidentresponses.json')
		self.assertEqual(response.content, "[]")

	def testSpecificIncidentResponse(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/incidentresponses/01.json')
		self.assertEqual(response.content, "[]")

	def testAbsentIncidentResponse(self):
		client = Client()
		response = client.get('/api/v1/competitions/01/incidentresponses/02.json')
		self.assertEqual(response.content, "")

class Plugins(TestCase):
	def setUp(self):
		pass

	def testListPlugins(self):
		client = Client()
		response = client.get('/api/v1/plugins.json')
		self.assertEqual(response.content, "[]")

	def testSpecificPlugins(self):
		client = Client()
		response = client.get('/api/v1/plugins/01.json')
		self.assertEqual(response.content, "[]")

	def testAbsentPlugins(self):
		client = Client()
		response = client.get('/api/v1/plugins/02.json')
		self.assertEqual(response.content, "")

class Users(TestCase):
	def setUp(self):
		pass

	def testListUsers(self):
		client = Client()
		response = client.get('/api/v1/users.json')
		self.assertEqual(response.content, "[]")

	def testSpecificUser(self):
		client = Client()
		response = client.get('/api/v1/users/01.json')
		self.assertEqual(response.content, "[]")

	def testAbsentUser(self):
		client = Client()
		response = client.get('/api/v1/users/02.json')
		self.assertEqual(response.content, "")

class Organizations(TestCase):
	def setUp(self):
		pass

	def testListOrganizations(self):
		client = Client()
		response = client.get('/api/v1/organizations.json')
		self.assertEqual(response.content, "[]")

	def testSpecificOrganization(self):
		client = Client()
		response = client.get('/api/v1/organizations/01.json')
		self.assertEqual(response.content, "[]")

	def testAbsentOrganization(self):
		client = Client()
		response = client.get('/api/v1/organizations/02.json')
		self.assertEqual(response.content, "")