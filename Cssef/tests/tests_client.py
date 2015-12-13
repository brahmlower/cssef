from unittest import TestCase
from client import *

class OrganizationEndpoints(TestCase):
	def organizationAdd(self, conn):
		kwDict = {
			'name': 'Test Name',
			'url': 'test_name',
		}
		command = CssefClient.organizationAdd
		command.conn = conn
		return command(**kwDict)

	def organizationSet(self, conn, **kwargs):
		kwDict = kwargs
		command = CssefClient.organizationSet
		command.conn = conn
		return command(**kwDict)

	def organizationGet(self, conn, **kwargs):
		kwDict = kwargs
		command = CssefClient.organizationGet
		command.conn = conn
		return command(**kwDict)

	def testOrganizationAdd(self):
		conn = getConn()
		output = self.organizationAdd(conn)
		self.assertEquals(output['value'], 0)

	def testOrganizationGet(self):
		conn = getConn()
		# Make sure there's no organizations listed
		output = self.organizationGet(conn)
		self.assertEquals(output['value'], 0)
		numOrganizations = len(output['content'])
		# Make sure the organization is successfully created
		output = self.organizationAdd(conn)
		self.assertEquals(output['value'], 0)
		# Make sure the right number of organizations are listed
		output = self.organizationGet(conn)
		self.assertEquals(output['value'], 0)
		self.assertEquals(len(output['content']), numOrganizations + 1)

	def testOrganizationSet(self):
		conn = getConn()
		output = self.organizationAdd(conn)
		pkid = output['content'][0]['id']
		output = self.organizationSet(conn, pkid = pkid, maxMembers = 4)
		output = self.organizationGet(conn, pkid = pkid)
		self.assertEquals(output['value'], 0)
		print output['content'][0]
		self.assertEquals(output['content'][0]['maxMembers'], 4)

class CompetitionEndpoints(TestCase):
	def organizationAdd(self, conn):
		kwDict = {
			'name': 'Test Name',
			'url': 'test_name'}
		command = CssefClient.organizationAdd
		command.conn = conn
		return command(**kwDict)

	def competitionAdd(self, conn, **kwargs):
		kwDict = kwargs
		kwDict['name'] = 'Test Name'
		kwDict['url'] = 'test_name'
		command = CssefClient.competitionAdd
		command.conn = conn
		return command(**kwDict)

	def testCompetitionAdd(self):
		conn = getConn()
		output = self.organizationAdd(conn)
		self.assertEquals(output['value'], 0)
		organizationId = output['content'][0]['id']
		output = self.competitionAdd(conn, organization = organizationId)
		print output['content']
		self.assertEquals(output['value'], 0)

class TeamEndpoints(TestCase):
	def teamAdd():
		pass

class ScoreEndpoints(TestCase):
	def scoreAdd():
		pass

class InjectEndpoints(TestCase):
	def injectAdd():
		pass

class InjectResponseEndpoints(TestCase):
	def injectResponseAdd():
		pass

class IncidentEndpoints(TestCase):
	def incidentAdd():
		pass

class IncidentResponseEndpoints(TestCase):
	def incidentResponseAdd():
		pass
