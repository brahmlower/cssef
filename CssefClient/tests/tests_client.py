from unittest import TestCase
from datetime import datetime

from cssefclient.cssefclient import getConn
from cssefclient.cssefclient import Configuration

from cssefclient.cssefclient import OrganizationAdd as ApiOrganizationAdd
from cssefclient.cssefclient import OrganizationSet as ApiOrganizationSet
from cssefclient.cssefclient import OrganizationDel as ApiOrganizationDel
from cssefclient.cssefclient import OrganizationGet as ApiOrganizationGet

from cssefclient.cssefclient import CompetitionAdd as ApiCompetitionAdd
from cssefclient.cssefclient import CompetitionSet as ApiCompetitionSet
from cssefclient.cssefclient import CompetitionDel as ApiCompetitionDel
from cssefclient.cssefclient import CompetitionGet as ApiCompetitionGet

from cssefclient.cssefclient import CompetitionTeamAdd as ApiCompetitionTeamAdd
from cssefclient.cssefclient import CompetitionTeamSet as ApiCompetitionTeamSet
from cssefclient.cssefclient import CompetitionTeamDel as ApiCompetitionTeamDel
from cssefclient.cssefclient import CompetitionTeamGet as ApiCompetitionTeamGet

from cssefclient.cssefclient import CompetitionScoreAdd as ApiCompetitionScoreAdd
from cssefclient.cssefclient import CompetitionScoreSet as ApiCompetitionScoreSet
from cssefclient.cssefclient import CompetitionScoreDel as ApiCompetitionScoreDel
from cssefclient.cssefclient import CompetitionScoreGet as ApiCompetitionScoreGet

from cssefclient.cssefclient import CompetitionInjectAdd as ApiCompetitionInjectAdd
from cssefclient.cssefclient import CompetitionInjectSet as ApiCompetitionInjectSet
from cssefclient.cssefclient import CompetitionInjectDel as ApiCompetitionInjectDel
from cssefclient.cssefclient import CompetitionInjectGet as ApiCompetitionInjectGet

from cssefclient.cssefclient import CompetitionInjectResponseAdd as ApiCompetitionInjectResponseAdd
from cssefclient.cssefclient import CompetitionInjectResponseSet as ApiCompetitionInjectResponseSet
from cssefclient.cssefclient import CompetitionInjectResponseDel as ApiCompetitionInjectResponseDel
from cssefclient.cssefclient import CompetitionInjectResponseGet as ApiCompetitionInjectResponseGet

from cssefclient.cssefclient import CompetitionIncidentAdd as ApiCompetitionIncidentAdd
from cssefclient.cssefclient import CompetitionIncidentSet as ApiCompetitionIncidentSet
from cssefclient.cssefclient import CompetitionIncidentDel as ApiCompetitionIncidentDel
from cssefclient.cssefclient import CompetitionIncidentGet as ApiCompetitionIncidentGet

from cssefclient.cssefclient import CompetitionIncidentResponseAdd as ApiCompetitionIncidentResponseAdd
from cssefclient.cssefclient import CompetitionIncidentResponseSet as ApiCompetitionIncidentResponseSet
from cssefclient.cssefclient import CompetitionIncidentResponseDel as ApiCompetitionIncidentResponseDel
from cssefclient.cssefclient import CompetitionIncidentResponseGet as ApiCompetitionIncidentResponseGet

'''
Descriptions for the basic tests:
* testXXXXAdd
	Verify the correct object information is returned with status code 0
* testXXXXGet
	Create an object and retrieve it via its ID
* testXXXXSet
	Verify that an object attrribute is changed
* testXXXXDel
	Delete an object, and then verify nothing is returned when filtering that objects ID
'''

config = Configuration("cssefclient/cssef.conf")

defaultOrganizationDict = {
	'name': 'Test Name',
	'url': 'test_name',
	'maxMembers': 5,
	'maxCompetitions': 5
}

defaultCompetitionDict = {
	'name': 'Test Competition',
	'url': 'test_competition'
}

defaultTeamDict = {
	'name': 'Test Team',
	'username': 'testteam',
	'password': 'test'
}

defaultScoreDict = {
	'datetime': datetime.now(),
	'message': 'Test message',
	'value': 100
}

defaultInjectDict = {
	'requireResponse': False,
	'manualDelivery': False,
	'datetimeDelivery': datetime.now(),
	'datetimeResponseDue': datetime.now(),
	'datetimeResponseClose': datetime.now(),
	'title': 'Test Inject',
	'body': 'test inject body'
}

defaultInjectResponseDict = {
	'datetime': datetime.now(),
	'content': "test content"
}

defaultIncidentDict = {
	'datetime': datetime.now(),
	'subject': "Test Subject",
	'content': "test content"
}

defaultIncidentResponseDict = {
	'datetime': datetime.now(),
	'subject': "Test Subject",
	'content': "test content"
}

def addOrganization(inst, conn, organizationDict = {}):
	kwDict = defaultOrganizationDict.copy()
	kwDict.update(organizationDict)
	output = ApiOrganizationAdd(conn).execute(**kwDict)
	inst.assertEquals(output['value'], 0)
	return output['content']

def addCompetition(inst, conn, competitionDict = {}):
	kwDict = defaultCompetitionDict.copy()
	kwDict.update(competitionDict)
	output = ApiCompetitionAdd(conn).execute(**kwDict)
	inst.assertEquals(output['value'], 0)
	return output['content']

def addTeam(inst, conn, teamDict = {}):
	kwDict = defaultTeamDict.copy()
	kwDict.update(teamDict)
	output = ApiCompetitionTeamAdd(conn).execute(**kwDict)
	inst.assertEquals(output['value'], 0)
	return output['content']

def addScore(inst, conn, scoreDict = {}):
	kwDict = defaultScoreDict.copy()
	kwDict.update(scoreDict)
	output = ApiCompetitionScoreAdd(conn).execute(**kwDict)
	inst.assertEquals(output['value'], 0)
	return output['content']

def addInject(inst, conn, injectDict ={}):
	kwDict = defaultInjectDict.copy()
	kwDict.update(injectDict)
	output = ApiCompetitionInjectAdd(conn).execute(**kwDict)
	inst.assertEquals(output['value'], 0)
	return output['content']

def addInjectResponse(inst, conn, injectResponseDict = {}):
	kwDict = defaultInjectResponseDict.copy()
	kwDict.update(injectResponseDict)
	output = ApiCompetitionInjectResponseAdd(conn).execute(**kwDict)
	inst.assertEquals(output['value'], 0)
	return output['content']

def addIncident(inst, conn, incidentDict = {}):
	kwDict = defaultIncidentDict.copy()
	kwDict.update(incidentDict)
	output = ApiCompetitionIncidentAdd(conn).execute(**kwDict)
	inst.assertEquals(output['value'], 0)
	return output['content']

def addIncidentResponse(inst, conn, incidentResponseDict = {}):
	kwDict = defaultIncidentResponseDict.copy()
	kwDict.update(incidentResponseDict)
	output = ApiCompetitionIncidentResponseAdd(conn).execute(**kwDict)
	inst.assertEquals(output['value'], 0)
	return output['content']

class OrganizationEndpoints(TestCase):
	def testOrganizationAdd(self):
		conn = getConn(config)
		content = addOrganization(self, conn)

	def testOrganizationGet(self):
		conn = getConn(config)
		# Create an organization
		content = addOrganization(self, conn)
		# Make sure the right number of organizations are listed
		output = ApiOrganizationGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		self.assertEquals(len(output['content']), 1)

	def testOrganizationSet(self):
		conn = getConn(config)
		# Create an organization
		content = addOrganization(self, conn)
		# Change the maxMembers for the organization
		output = ApiOrganizationSet(conn).execute(pkid = content[0]['id'], maxMembers = 9001)
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		# Get the organization again and verify the value of maxMembers
		output = ApiOrganizationGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		self.assertEquals(output['content'][0]['maxMembers'], 9001)

	def testOrganizationDel(self):
		conn = getConn(config)
		# Create an organization
		content = addOrganization(self, conn)
		# Delete the competition we just created
		output = ApiOrganizationDel(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		# Check that the organization id gone
		output = ApiOrganizationGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(len(output['content']), 0)

class CompetitionEndpoints(TestCase):
	def testCompetitionAdd(self):
		conn = getConn(config)
		# Create an organization and competition
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})

	def testCompetitionGet(self):
		conn = getConn(config)
		# Create an organization and competition
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		# Get that specific competition
		output = ApiCompetitionGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		self.assertEquals(len(output['content']), 1)

	def testCompetitionSet(self):
		conn = getConn(config)
		# Create an organization and competition
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		# Change the name of the competition
		output = ApiCompetitionSet(conn).execute(pkid = content[0]['id'], name = 'New Name')
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		# Verify the name was changed
		output = ApiCompetitionGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['content'][0]['name'], 'New Name', "\n".join(output['message']))

	def testCompetitionDel(self):
		conn = getConn(config)
		# Create an organization and competition
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		# Delete the competition we just created
		output = ApiCompetitionDel(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		# Check that the organization id gone
		output = ApiCompetitionGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(len(output['content']), 0)

class TeamEndpoints(TestCase):
	def testTeamAdd(self):
		conn = getConn(config)
		# Create an organization, competition and team
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		content = addTeam(self, conn, {'competition': content[0]['id']})

	def testTeamGet(self):
		conn = getConn(config)
		# Create an organization, competition, and team
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		content = addTeam(self, conn, {'competition': content[0]['id']})
		# Get teams by that ID. Verify the return status is OK, and only 1 item was returned
		output = ApiCompetitionTeamGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		self.assertEquals(len(output['content']), 1)

	def testTeamSet(self):
		conn = getConn(config)
		# Create an organization, competition and team
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		content = addTeam(self, conn, {'competition': content[0]['id']})
		# Change the name of the team
		output = ApiCompetitionTeamSet(conn).execute(pkid = content[0]['id'], name = 'Test Name')
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		# Make sure the name was properly changed
		output = ApiCompetitionTeamGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		self.assertEquals(output['content'][0]['name'], 'Test Name')

	def testTeamDel(self):
		conn = getConn(config)
		# Create an organization, competition and team
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		content = addTeam(self, conn, {'competition': content[0]['id']})
		# Delete the team
		output = ApiCompetitionTeamDel(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		# Try to get the team, it should return no items
		output = ApiCompetitionTeamGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(len(output['content']), 0)

class ScoreEndpoints(TestCase):
	def testScoreAdd(self):
		conn = getConn(config)
		# Create an organization, competition and team
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		competitionId = content[0]['id']
		content = addTeam(self, conn, {'competition': competitionId})
		teamId = content[0]['id']
		content = addScore(self, conn, {'competition': competitionId, 'team': teamId})

	def testScoreGet(self):
		conn = getConn(config)
		# Create an organization, competition and team
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		competitionId = content[0]['id']
		content = addTeam(self, conn, {'competition': competitionId})
		teamId = content[0]['id']
		content = addScore(self, conn, {'competition': competitionId, 'team': teamId})
		# Get score by that ID. Verify the return status is OK, and only 1 item was returned
		output = ApiCompetitionScoreGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		self.assertEquals(len(output['content']), 1)

	def testScoreSet(self):
		conn = getConn(config)
		# Create an organization, competition and team
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		competitionId = content[0]['id']
		content = addTeam(self, conn, {'competition': competitionId})
		teamId = content[0]['id']
		content = addScore(self, conn, {'competition': competitionId, 'team': teamId})
		# Change the message of the score
		output = ApiCompetitionScoreSet(conn).execute(pkid = content[0]['id'], message = "new message")
		print output
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		# Make sure the message was properly changed
		output = ApiCompetitionScoreGet(conn).execute(pkid = content[0]['id'])
		print output
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		self.assertEquals(output['content'][0]['message'], "new message")

	def testScoreDel(self):
		conn = getConn(config)
		# Create an organization, competition and team
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		competitionId = content[0]['id']
		content = addTeam(self, conn, {'competition': competitionId})
		teamId = content[0]['id']
		content = addScore(self, conn, {'competition': competitionId, 'team': teamId})
		# Delete the score
		output = ApiCompetitionScoreDel(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		# Try to get the score, it should return no items
		output = ApiCompetitionScoreGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(len(output['content']), 0)

class InjectEndpoints(TestCase):
	def testInjectAdd(self):
		conn = getConn(config)
		# Create an organization, competition, and inject
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		content = addInject(self, conn, {'competition': content[0]['id']})

	def testInjectGet(self):
		conn = getConn(config)
		# Create an organization, competition, and inject
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		content = addInject(self, conn, {'competition': content[0]['id']})
		# Get inject
		output = ApiCompetitionInjectGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		self.assertEquals(len(output['content']), 1)

	def testInjectSet(self):
		conn = getConn(config)
		# Create an organization, competition, and inject
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		content = addInject(self, conn, {'competition': content[0]['id']})
		# Change the title of the inject
		output = ApiCompetitionInjectSet(conn).execute(pkid = content[0]['id'], title = 'New Test Title')
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		# Verify the title was properly changed
		output = ApiCompetitionInjectGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		self.assertEquals(output['content'][0]['title'], 'New Test Title')

	def testInjectDel(self):
		conn = getConn(config)
		# Create an organization, competition, and inject
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		content = addInject(self, conn, {'competition': content[0]['id']})
		# Delete the inject
		output = ApiCompetitionInjectDel(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		# Try to get the inject, it should return no items
		output = ApiCompetitionInjectGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(len(output['content']), 0)

class InjectResponseEndpoints(TestCase):
	def testInjectResponseAdd(self):
		conn = getConn(config)
		# Create an organization, competition, team, inject and inject response
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		competitionId = content[0]['id']
		content = addTeam(self, conn, {'competition': competitionId})
		teamId = content[0]['id']
		content = addInject(self, conn, {'competition': content[0]['id']})
		injectId = content[0]['id']
		content = addInjectResponse(self, conn, {'competition': competitionId, 'team': teamId, 'inject': injectId})

	def testInjectResponseGet(self):
		conn = getConn(config)
		# Create an organization, competition, team, inject and inject response
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		competitionId = content[0]['id']
		content = addTeam(self, conn, {'competition': competitionId})
		teamId = content[0]['id']
		content = addInject(self, conn, {'competition': content[0]['id']})
		injectId = content[0]['id']
		content = addInjectResponse(self, conn, {'competition': competitionId, 'team': teamId, 'inject': injectId})
		# Get the new inject response
		output = ApiCompetitionInjectResponseGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		self.assertEquals(len(output['content']), 1)

	def testInjectResponseSet(self):
		conn = getConn(config)
		# Create an organization, competition, team, inject and inject response
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		competitionId = content[0]['id']
		content = addTeam(self, conn, {'competition': competitionId})
		teamId = content[0]['id']
		content = addInject(self, conn, {'competition': content[0]['id']})
		injectId = content[0]['id']
		content = addInjectResponse(self, conn, {'competition': competitionId, 'team': teamId, 'inject': injectId})
		# Change the content of the inject
		output = ApiCompetitionInjectResponseSet(conn).execute(pkid = content[0]['id'], content = 'new content')
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		# Verify the content was properly changed
		output = ApiCompetitionInjectResponseGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		self.assertEquals(output['content'][0]['content'], 'new content')

	def testInjectResponseDel(self):
		conn = getConn(config)
		# Create an organization, competition, team, inject and inject response
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		competitionId = content[0]['id']
		content = addTeam(self, conn, {'competition': competitionId})
		teamId = content[0]['id']
		content = addInject(self, conn, {'competition': content[0]['id']})
		injectId = content[0]['id']
		content = addInjectResponse(self, conn, {'competition': competitionId, 'team': teamId, 'inject': injectId})
		# Delete the inject response
		output = ApiCompetitionInjectResponseDel(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		# Try to get the inject response, it should return no items
		output = ApiCompetitionInjectResponseGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(len(output['content']), 0)

class IncidentEndpoints(TestCase):
	def testIncidentAdd(self):
		conn = getConn(config)
		# Create an organization, competition, team and incident
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		competitionId = content[0]['id']
		content = addTeam(self, conn, {'competition': competitionId})
		teamId = content[0]['id']
		content = addIncident(self, conn, {'competition': competitionId, 'team': teamId})

	def testIncidentGet(self):
		conn = getConn(config)
		# Create an organization, competition, team and incident
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		competitionId = content[0]['id']
		content = addTeam(self, conn, {'competition': competitionId})
		teamId = content[0]['id']
		content = addIncident(self, conn, {'competition': competitionId, 'team': teamId})
		# Get the new inject response
		output = ApiCompetitionIncidentGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		self.assertEquals(len(output['content']), 1)

	def testIncidentSet(self):
		conn = getConn(config)
		# Create an organization, competition, team and incident
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		competitionId = content[0]['id']
		content = addTeam(self, conn, {'competition': competitionId})
		teamId = content[0]['id']
		content = addIncident(self, conn, {'competition': competitionId, 'team': teamId})
		# Change the content of the incident
		output = ApiCompetitionIncidentSet(conn).execute(pkid = content[0]['id'], subject = 'new subject')
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		# Verify the content was properly changed
		output = ApiCompetitionIncidentGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		self.assertEquals(output['content'][0]['subject'], 'new subject')

	def testIncidentDel(self):
		conn = getConn(config)
		# Create an organization, competition, team and incident
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		competitionId = content[0]['id']
		content = addTeam(self, conn, {'competition': competitionId})
		teamId = content[0]['id']
		content = addIncident(self, conn, {'competition': competitionId, 'team': teamId})
		# Delete the incident response
		output = ApiCompetitionIncidentDel(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		# Try to get the incident response, it should return no items
		output = ApiCompetitionIncidentGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(len(output['content']), 0)

class IncidentResponseEndpoints(TestCase):
	def testIncidentResponseAdd(self):
		conn = getConn(config)
		# Create an organization, competition, team and incident
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		competitionId = content[0]['id']
		content = addTeam(self, conn, {'competition': competitionId})
		teamId = content[0]['id']
		content = addIncidentResponse(self, conn, {'competition': competitionId, 'team': teamId})

	def testIncidentResponseGet(self):
		conn = getConn(config)
		# Create an organization, competition, team and incident
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		competitionId = content[0]['id']
		content = addTeam(self, conn, {'competition': competitionId})
		teamId = content[0]['id']
		content = addIncidentResponse(self, conn, {'competition': competitionId, 'team': teamId})
		# Get the new inject response
		output = ApiCompetitionIncidentResponseGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		self.assertEquals(len(output['content']), 1)

	def testIncidentResponseSet(self):
		conn = getConn(config)
		# Create an organization, competition, team and incident
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		competitionId = content[0]['id']
		content = addTeam(self, conn, {'competition': competitionId})
		teamId = content[0]['id']
		content = addIncidentResponse(self, conn, {'competition': competitionId, 'team': teamId})
		# Change the content of the incident
		output = ApiCompetitionIncidentResponseSet(conn).execute(pkid = content[0]['id'], subject = 'new subject')
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		# Verify the content was properly changed
		output = ApiCompetitionIncidentResponseGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		self.assertEquals(output['content'][0]['subject'], 'new subject')

	def testIncidentResponseDel(self):
		conn = getConn(config)
		# Create an organization, competition, team and incident
		content = addOrganization(self, conn)
		content = addCompetition(self, conn, {'organization': content[0]['id']})
		competitionId = content[0]['id']
		content = addTeam(self, conn, {'competition': competitionId})
		teamId = content[0]['id']
		content = addIncidentResponse(self, conn, {'competition': competitionId, 'team': teamId})
		# Delete the incident response
		output = ApiCompetitionIncidentResponseDel(conn).execute(pkid = content[0]['id'])
		self.assertEquals(output['value'], 0, "\n".join(output['message']))
		# Try to get the incident response, it should return no items
		output = ApiCompetitionIncidentResponseGet(conn).execute(pkid = content[0]['id'])
		self.assertEquals(len(output['content']), 0)