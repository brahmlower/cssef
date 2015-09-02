from django.test import TestCase
from ScoringEngine.endpoints import *

class GeneralEndpoints(TestCase):
	def testGetCompetition(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
		org = createOrganization(creationDict)
		org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		comp = getCompetition(name = 'Super Comp')
		self.assertEquals(org.__class__.__name__, 'Organization')

	def testGetCompetitions(self):
		orgDict1 = {'name': 'First Org', 'url': 'first_org', 'maxCompetitions': 5}
		orgDict2 = {'name': 'Second Org', 'url': 'second_org', 'maxCompetitions': 5}
		org1 = createOrganization(orgDict1)
		org2 = createOrganization(orgDict2)
		org1.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		org2.createCompetition({'name': 'Mega Comp', 'url': 'mega_comp'})
		users = getCompetitions()
		self.assertEquals(len(users), 2)
		for i in users:
			self.assertEquals(i.__class__.__name__, 'Competition')

	def testGetOrganization(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		createOrganization(creationDict)
		org = getOrganization(name = 'New Org')
		self.assertEquals(org.__class__.__name__, 'Organization')

	def testGetOrganizations(self):
		orgDict1 = {'name': 'First Org', 'url': 'first_org'}
		orgDict2 = {'name': 'Second Org', 'url': 'second_org'}
		createOrganization(orgDict1)
		createOrganization(orgDict2)
		orgs = getOrganizations()
		self.assertEquals(len(orgs), 2)
		for i in orgs:
			self.assertEquals(i.__class__.__name__, 'Organization')

	def testCreateOrganization(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		self.assertEquals(org.__class__.__name__, 'Organization')

	def testCreateOrganizationNoUrl(self):
		# Ultimately though, an error should be thrown rather than returning a dict/returndict
		creationDict = {'name': 'New Org'}
		org = createOrganization(creationDict)
		self.assertEquals(org.__class__.__name__, 'Organization')

	def testCreateOrganizationDefaults(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		self.assertEquals(org.getMaxMembers(), 0)
		self.assertEquals(org.getMaxCompetitions(), 0)

	def testEditOrganization(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
		org = createOrganization(creationDict)
		editOrganization(organizationId = org.getId(), maxMembers = 10, maxCompetitions = 5)
		self.assertEquals(org.getMaxMembers(), 10)
		self.assertEquals(org.getMaxCompetitions(), 5)

	def testGetUser(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
		org = createOrganization(creationDict)
		member = org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
		user = getUser(name = 'Bob')
		self.assertEquals(user.__class__.__name__, 'User')

	def testGetUsers(self):
		orgDict1 = {'name': 'First Org', 'url': 'first_org', 'maxMembers': 5}
		orgDict2 = {'name': 'Second Org', 'url': 'second_org', 'maxMembers': 5}
		org1 = createOrganization(orgDict1)
		org2 = createOrganization(orgDict2)
		org1.createMember({'name': 'Bob', 'password': 'B0bs!password'})
		org2.createMember({'name': 'Jill', 'password': 'J1lls!password'})
		users = getUsers()
		self.assertEquals(len(users), 2)
		for i in users:
			self.assertEquals(i.__class__.__name__, 'User')

	def testEditUser(self):
		pass

class DocumentEndpoints(TestCase):
	pass

class OrganizationEndpoints(TestCase):
	def testCantModifyDeletionAtCreation(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'deleteable': False}
		org = createOrganization(creationDict)
		self.assertEquals(org.getDeleteable(), True)

	def testCantModifyDeletionAtEdit(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		org.edit(deleteable = False)
		self.assertEquals(org.getDeleteable(), True)

	def testGetName(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		self.assertEquals(org.getName(), creationDict['name'])

	def testSetName(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		org.edit(name = 'New Name')
		self.assertEquals(org.getName(), 'New Name')

	def testGetUrl(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		self.assertEquals(org.getUrl(), creationDict['url'])

	def testSetUrl(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		org.edit(url = 'new_url')
		self.assertEquals(org.getUrl(), 'new_url')

	def testGetDescription(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'description': 'New description!'}
		org = createOrganization(creationDict)
		self.assertEquals(org.getDescription(), creationDict['description'])

	def testSetDescription(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		description = 'New different description!'
		org.edit(description = description)
		self.assertEquals(org.getDescription(), description)

	def testGetMaxMembers(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 10}
		org = createOrganization(creationDict)
		self.assertEquals(org.getMaxMembers(), creationDict['maxMembers'])

	def testSetMaxMembers(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		org.edit(maxMembers = 15)
		self.assertEquals(org.getMaxMembers(), 15)

	def testGetMaxCompetitions(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 10}
		org = createOrganization(creationDict)
		self.assertEquals(org.getMaxCompetitions(), creationDict['maxCompetitions'])

	def testSetMaxCompetitions(self):
		creationDict = {'name': 'New Org', 'url': 'new_org'}
		org = createOrganization(creationDict)
		org.edit(maxCompetitions = 15)
		self.assertEquals(org.getMaxCompetitions(), 15)

	def testGetNumMembers(self):
		pass

	def testSetNumMembers(self):
		pass

	def testGetNumCompetitions(self):
		pass

	def testSetNumCompetitions(self):
		pass

	def testGetCompetitions(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
		org = createOrganization(creationDict)
		self.assertEquals(len(org.getCompetitions()), 0)
		org.createCompetition({'name': 'New Comp', 'url': 'new_comp'})
		self.assertEquals(len(org.getCompetitions()), 1)

	def testGetMembers(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
		org = createOrganization(creationDict)
		self.assertEquals(len(org.getMembers()), 0)
		org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
		self.assertEquals(len(org.getMembers()), 1)

	def testGetCompetition(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
		org = createOrganization(creationDict)
		org.createCompetition({'name': 'New Comp', 'url': 'new_comp'})
		competition = org.getCompetition(name = 'New Comp')
		self.assertEquals(competition.__class__.__name__, 'Competition')

	def testGetMember(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
		org = createOrganization(creationDict)
		org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
		member = org.getMember(name = 'Bob')
		self.assertEquals(member.__class__.__name__, 'User')

	def testCreateCompetition(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
		org = createOrganization(creationDict)
		competition = org.createCompetition({'name': 'New Comp', 'url': 'new_comp'})
		self.assertEquals(competition.__class__.__name__, 'Competition')

	def testCreateMember(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
		org = createOrganization(creationDict)
		member = org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
		self.assertEquals(member.__class__.__name__, 'User')

	def testDeleteCompetition(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
		org = createOrganization(creationDict)
		competition = org.createCompetition({'name': 'New Comp', 'url': 'new_comp'})
		org.deleteCompetition(competitionId = competition.getId())

	def testDeleteMember(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
		org = createOrganization(creationDict)
		member = org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
		org.deleteMember(userId = member.getId())

	def testEditCompetition(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5}
		org = createOrganization(creationDict)
		competition = org.createCompetition({'name': 'New Comp', 'url': 'new_comp'})
		org.editCompetition(competitionId = competition.getId(), description = 'New description')
		self.assertEquals(competition.getDescription(), 'New description')

	def testEditMember(self):
		creationDict = {'name': 'New Org', 'url': 'new_org', 'maxMembers': 5}
		org = createOrganization(creationDict)
		member = org.createMember({'name': 'Bob', 'password': 'Bobs!password'})
		org.editMember(userId = member.getId(), name = 'Jill')
		self.assertEquals(member.getName(), 'Jill')

class UserEndpoints(TestCase):
	def testGetId(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		self.assertEquals(user.getId(), 1)

	def testGetName(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		self.assertEquals(user.getName(), 'Bob')

	def testSetName(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		user.setUsername('Billy')
		self.assertEquals(user.getName(), 'Billy')

	def testGetUsername(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		self.assertEquals(user.getUsername(), 'b')

	def testSetUsername(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		user.setUsername('bb')
		self.assertEquals(user.getUsername(), 'bb')

	def testGetPassword(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		self.assertEquals(user.getPassword(), 'Bobs!password')

	def testSetPassword(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		user.setPassword('b0bsBurg3rz')
		self.assertEquals(user.getPassword(), 'b0bsBurg3rz')

	def testGetDescription(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b', 'description': "Super security expert!"})
		self.assertEquals(user.getDescription(), "Super security expert!")

	def testSetDescription(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b', 'description': "Super security expert!"})
		user.setDescription("He actually sucks at security...")
		self.assertEquals(user.getDescription(), "He actually sucks at security...")

	def testGetOrganizationId(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxMembers': 1})
		user = org.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		self.assertEquals(user.getOrganizationId(), org.getId())

	def testSetOrganizationId(self):
		org1 = createOrganization({'name': 'First Org', 'url': 'first_org', 'maxMembers': 1})
		org2 = createOrganization({'name': 'Second Org', 'url': 'second_org', 'maxMembers': 1})
		user = org1.createMember({'name': 'Bob', 'password': 'Bobs!password', 'username': 'b'})
		user.setOrganizationId(org2.getId())
		self.assertEquals(user.getOrganizationId(), org2.getId())

class CompetitionEndpoints(TestCase):
	def testCount(self):
		pass

	def testGetName(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		self.assertEquals(comp.getName(), 'Super Comp')

	def testCheck(self):
		pass
		
	def testCreateTeam(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		team = comp.createTeam(teamData)
		self.assertEquals(team.__class__.__name__, 'Team')

	def testEditTeam(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		team = comp.createTeam(teamData)
		comp.editTeam(team.getId(), password = 'Its so cold up here...')
		self.assertEquals(team.getPassword(), 'Its so cold up here...')

	def testGetTeam(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		comp.createTeam(teamData)
		team = comp.getTeam(name = 'UAF Team')
		self.assertEquals(team.__class__.__name__, 'Team')

	def testGetTeams(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		teamData1 = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		teamData2 = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		comp.createTeam(teamData1)
		comp.createTeam(teamData2)
		teams = comp.getTeams()
		self.assertEquals(len(teams), 2)
		for i in teams:
			self.assertEquals(i.__class__.__name__, 'Team')

	def testDeleteTeam(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		comp.createTeam(teamData)
		team = comp.getTeam(name = 'UAF Team')
		comp.deleteTeam(team.getId())

	def testCreateIncident(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		team = comp.createTeam(teamData)
		incidentData = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
		incident = comp.createIncident(incidentData)
		self.assertEquals(incident.__class__.__name__, 'Incident')

	def testEditIncident(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		team = comp.createTeam(teamData)
		incidentData = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
		incident = comp.createIncident(incidentData)
		comp.editIncident(incidentId = incident.getId(), content = 'Actually it was their firewall #rekt')
		self.assertEquals(incident.getContent, 'Actually it was their firewall #rekt')

	def testGetIncident(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		team = comp.createTeam(teamData)
		incidentData = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
		comp.createIncident(incidentData)
		incident = comp.getIncident(subject = 'We super hacked them')
		self.assertEquals(incident.__class__.__name__, 'Incident')

	def testGetIncidents(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		team = comp.createTeam(teamData)
		incidentData1 = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
		incidentData2 = {'teamId': team.getId(), 'subject':'Rooted as hell', 'content':'Very back door. Such exploit. Wow.'}
		comp.createIncident(incidentData1)
		comp.createIncident(incidentData2)
		incidents = comp.getIncidents(teamId = team.getId())
		for i in incidents:
			self.assertEquals(i.__class__.__name__, 'Incident')

	def testDeleteIncident(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		team = comp.createTeam(teamData)
		incidentData = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
		incident = comp.createIncident(incidentData)
		comp.deleteIncident(incidentId = incident.getId())

	def testCreateIncidentResponse(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		team = comp.createTeam(teamData)
		incidentData = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
		incident = comp.createIncident(incidentData)
		incidentResponseData = {'teamId': team.getId(), 'incidentId': incident.getId(), 'content':"That wasn't our password! It was a default.."}
		incidentResponse = comp.createIncidentResponse(incidentResponseData)
		self.assertEquals(incidentResponse.__class__.__name__, 'IncidentResponse')

	def testEditIncidentResponse(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		team = comp.createTeam(teamData)
		incidentData = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
		incident = comp.createIncident(incidentData)
		incidentResponseData = {'teamId': team.getId(), 'incidentId': incident.getId(), 'content':"That wasn't our password! It was a default.."}
		incidentResponse = comp.createIncidentResponse(incidentResponseData)
		comp.editIncidentResponse(incidentResponseId = incidentResponse.getId(), content = 'Changed content!')
		self.assertEquals(incidentResponse.getContent(), 'Changed content!')

	def testGetIncidentResponse(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		team = comp.createTeam(teamData)
		incidentData = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
		incident = comp.createIncident(incidentData)
		incidentResponseData = {'teamId': team.getId(), 'incidentId': incident.getId(), 'content': "That wasn't our password! It was a default.."}
		comp.createIncidentResponse(incidentResponseData)
		incidentResponse = comp.getIncidentResponse(content = "That wasn't our password! It was a default..")
		self.assertEquals(incidentResponse.__class__.__name__, 'IncidentResponse')

	def testGetIncidentResponses(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		team = comp.createTeam(teamData)
		incidentData = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
		incident = comp.createIncident(incidentData)
		incidentResponseData1 = {'teamId': team.getId(), 'incidentId': incident.getId(), 'content': "That wasn't our password! It was a default.."}
		incidentResponseData2 = {'teamId': team.getId(), 'incidentId': incident.getId(), 'content': 'This is another response.'}
		comp.createIncidentResponse(incidentResponseData1)
		comp.createIncidentResponse(incidentResponseData2)
		incidentResponses = comp.getIncidentResponses(teamId = team.getId(), incidentId = incident.getId())
		self.assertEquals(len(incidentResponses), 2)
		for i in incidents:
			self.assertEquals(i.__class__.__name__, 'IncidentResponse')

	def testDeleteIncidentResponse(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})

	def testCreateInject(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})

	def testEditInject(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})

	def testGetInject(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})

	def testGetInjects(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})

	def testDeleteInject(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})

	def testCreateInjectResponse(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})

	def testEditInjectResponse(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})

	def testGetInjectResponse(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})

	def testGetInjectResponses(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})

	def testDelteInjectResponse(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})

	def testCreateScore(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})

	def testEditScore(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})

	def testGetScore(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})

	def testGetScores(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})

	def testDeleteScore(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})


class TeamEndpoints(TestCase):
	pass

class InjectEndpoints(TestCase):
	pass

class InjectResponseEndpoints(TestCase):
	pass

class IncidentEndpoints(TestCase):
	pass

class IncidentResponseEndpoints(TestCase):
	pass

class ScoreEndpoints(TestCase):
	pass
