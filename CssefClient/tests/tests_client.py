from unittest import TestCase
from client import *
from client import OrganizationAdd as ApiOrganizationAdd
from client import OrganizationSet as ApiOrganizationSet
from client import OrganizationDel as ApiOrganizationDel
from client import OrganizationGet as ApiOrganizationGet

from client import CompetitionAdd as ApiCompetitionAdd
from client import CompetitionSet as ApiCompetitionSet
from client import CompetitionDel as ApiCompetitionDel
from client import CompetitionGet as ApiCompetitionGet

from client import CompetitionTeamAdd as ApiCompetitionTeamAdd
from client import CompetitionTeamSet as ApiCompetitionTeamSet
from client import CompetitionTeamDel as ApiCompetitionTeamDel
from client import CompetitionTeamGet as ApiCompetitionTeamGet

'''
Descriptions for the basic tests:
* testXXXXAdd
	Verify the correct object information is returned with status code 0
* testXXXXGet
	Verify the creation of a new object increases the list of objects by 1
* testXXXXSet
	Verify that an object attrribute is changed
* testXXXXDel
	Delete an object, and then verify an error is thrown when the object is retrieved
'''

organizationKeywordDict = {
	'name': 'Test Name',
	'url': 'test_name',
	'maxMembers': 5,
	'maxCompetitions': 5
}

competitionKeywordDict = {
	'name': 'Test Competition',
	'url': 'test_competition'
}

teamKeywordDict = {
	'name': 'Test Team',
	'username': 'testteam',
	'password': 'test'
}

class OrganizationEndpoints(TestCase):
	def testOrganizationAdd(self):
		conn = getConn()
		output = ApiOrganizationAdd(conn).execute(**organizationKeywordDict)
		self.assertEquals(output['value'], 0)

	def testOrganizationGet(self):
		conn = getConn()
		# Make sure there's no organizations listed
		output = ApiOrganizationGet(conn).execute()
		self.assertEquals(output['value'], 0)
		numOrganizations = len(output['content'])
		# Make sure the organization is successfully created
		output = ApiOrganizationAdd(conn).execute(**organizationKeywordDict)
		self.assertEquals(output['value'], 0)
		# Make sure the right number of organizations are listed
		output = ApiOrganizationGet(conn).execute()
		self.assertEquals(output['value'], 0)
		self.assertEquals(len(output['content']), numOrganizations + 1)

	def testOrganizationSet(self):
		conn = getConn()
		output = ApiOrganizationAdd(conn).execute(**organizationKeywordDict)
		pkid = output['content'][0]['id']
		output = ApiOrganizationSet(conn).execute(pkid = pkid, maxMembers = 4)
		output = ApiOrganizationGet(conn).execute(pkid = pkid)
		self.assertEquals(output['value'], 0)
		self.assertEquals(output['content'][0]['maxMembers'], 4)

	def testOrganizationDel(self):
		self.assertTrue(False)

class CompetitionEndpoints(TestCase):
	def testCompetitionAdd(self):
		conn = getConn()
		# Create an organization
		output = ApiOrganizationAdd(conn).execute(**organizationKeywordDict)
		kwDict = competitionKeywordDict
		kwDict['organization'] = output['content'][0]['id']
		# Create a competition
		output = ApiCompetitionAdd(conn).execute(**kwDict)
		self.assertEquals(output['value'], 0)

	def testCompetitionGet(self):
		conn = getConn()
		# Create an organization and competition
		output = ApiOrganizationAdd(conn).execute(**organizationKeywordDict)
		kwDict = competitionKeywordDict
		kwDict['organization'] = output['content'][0]['id']
		# Create a competition
		output = ApiCompetitionAdd(conn).execute(**kwDict)
		pkid = output['content'][0]['id']
		# Get that specific competition
		output = ApiCompetitionGet(conn).execute(pkid = pkid)
		self.assertEquals(output['value'], 0)

	def testCompetitionSet(self):
		conn = getConn()
		# Create an organization
		output = ApiOrganizationAdd(conn).execute(**organizationKeywordDict)
		kwDict = competitionKeywordDict
		kwDict['organization'] = output['content'][0]['id']
		# Create a competition
		output = ApiCompetitionAdd(conn).execute(**kwDict)
		pkid = output['content'][0]['id']
		# Change the name of the competition
		output = ApiCompetitionSet(conn).execute(pkid = pkid, name = 'New Name')
		self.assertEquals(output['value'], 0)
		# Verify the name was changed
		output = ApiCompetitionGet(conn).execute(pkid = pkid)
		self.assertEquals(output['content'][0]['name'], 'New Name')

	def testCompetitionDel(self):
		conn = getConn()
		# Create an organization
		output = ApiOrganizationAdd(conn).execute(**organizationKeywordDict)
		kwDict = competitionKeywordDict
		kwDict['organization'] = output['content'][0]['id']
		# Create a competition
		output = ApiCompetitionAdd(conn).execute(**kwDict)
		pkid = output['content'][0]['id']
		# Delete the competition we just created
		output = ApiCompetitionDel(conn).execute(pkid = pkid)
		self.assertEquals(output['value'], 0)
		# Check that the organization id gone
		output = ApiCompetitionGet(conn).execute(pkid = pkid)
		self.assertEquals(output['value'], 1)

class TeamEndpoints(TestCase):
	def testTeamAdd(self):
		conn = getConn()
		# Create an organization
		output = ApiOrganizationAdd(conn).execute(**organizationKeywordDict)
		kwDict = competitionKeywordDict
		kwDict['organization'] = output['content'][0]['id']
		# Create a competition
		output = ApiCompetitionAdd(conn).execute(**kwDict)
		self.assertEquals(output['value'], 0)
		# Create a team for that competition
		kwDict = teamKeywordDict
		kwDict['competition'] = output['content'][0]['id']
		output = ApiCompetitionTeamAdd(conn).execute(**kwDict)
		self.assertEquals(output['value'], 0)

	def testTeamGet(self):
		conn = getConn()
		# Create an organization
		output = ApiOrganizationAdd(conn).execute(**organizationKeywordDict)
		kwDict = competitionKeywordDict
		kwDict['organization'] = output['content'][0]['id']
		# Create a competition
		output = ApiCompetitionAdd(conn).execute(**kwDict)
		self.assertEquals(output['value'], 0)
		# Create a team for that competition
		kwDict = teamKeywordDict
		kwDict['competition'] = output['content'][0]['id']
		output = ApiCompetitionTeamAdd(conn).execute(**kwDict)
		self.assertEquals(output['value'], 0)

	def testTeamSet(self):
		conn = getConn()
		# Create an organization
		output = ApiOrganizationAdd(conn).execute(**organizationKeywordDict)
		kwDict = competitionKeywordDict
		kwDict['organization'] = output['content'][0]['id']
		# Create a competition
		output = ApiCompetitionAdd(conn).execute(**kwDict)
		self.assertEquals(output['value'], 0)
		# Create a team for that competition
		kwDict = teamKeywordDict
		kwDict['competition'] = output['content'][0]['id']
		output = ApiCompetitionTeamAdd(conn).execute(**kwDict)
		pkid = output['content'][0]['id']
		# Change the name of the team
		output = ApiCompetitionTeamSet(conn).execute(pkid = pkid, name = 'Test Name')
		self.assertEquals(output['value'], 0)
		# Make sure the name was properly changed
		output = ApiCompetitionTeamGet(conn).execute(pkid = pkid)
		self.assertEquals(output['value'], 0)
		self.assertEquals(output['content'][0]['name'], 'Test Name')

	def testTeamDel(self):
		conn = getConn()
		# Create an organization
		output = ApiOrganizationAdd(conn).execute(**organizationKeywordDict)
		kwDict = competitionKeywordDict
		kwDict['organization'] = output['content'][0]['id']
		# Create a competition
		output = ApiCompetitionAdd(conn).execute(**kwDict)
		self.assertEquals(output['value'], 0)
		# Create a team for that competition
		kwDict = teamKeywordDict
		kwDict['competition'] = output['content'][0]['id']
		output = ApiCompetitionTeamAdd(conn).execute(**kwDict)
		pkid = output['content'][0]['id']
		# Delete the team
		output = ApiCompetitionTeamDel(conn).execute(pkid = pkid)
		self.assertEquals(output['value'], 0)
		# Try to get the team (it should fail)
		output = ApiCompetitionTeamGet(conn).execute(pkid = pkid)
		self.assertEquals(output['value'], 1)

class ScoreEndpoints(TestCase):
	def testScoreAdd(self):
		self.assertTrue(False)

	def testScoreGet(self):
		self.assertTrue(False)

	def testScoreSet(self):
		self.assertTrue(False)

	def testScoreDel(self):
		self.assertTrue(False)

class InjectEndpoints(TestCase):
	def testInjectAdd(self):
		self.assertTrue(False)

	def testInjectGet(self):
		self.assertTrue(False)

	def testInjectSet(self):
		self.assertTrue(False)

	def testInjectDel(self):
		self.assertTrue(False)

class InjectResponseEndpoints(TestCase):
	def testInjectResponseAdd(self):
		self.assertTrue(False)

	def testInjectResponseGet(self):
		self.assertTrue(False)

	def testInjectResponseSet(self):
		self.assertTrue(False)

	def testInjectResponseDel(self):
		self.assertTrue(False)

class IncidentEndpoints(TestCase):
	def testIncidentAdd(self):
		self.assertTrue(False)

	def testIncidentGet(self):
		self.assertTrue(False)

	def testIncidentSet(self):
		self.assertTrue(False)

	def testIncidentDel(self):
		self.assertTrue(False)

class IncidentResponseEndpoints(TestCase):
	def testIncidentResponseAdd(self):
		self.assertTrue(False)

	def testIncidentResponseGet(self):
		self.assertTrue(False)

	def testIncidentResponseSet(self):
		self.assertTrue(False)

	def testIncidentResponseDel(self):
		self.assertTrue(False)
