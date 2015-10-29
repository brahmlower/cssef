from django.test import TestCase
from ScoringEngine.framework.core import *
from ScoringEngine.framework.competition import *

class CompetitionEndpoints(TestCase):
	def testCount(self):
		pass

	def testGetName(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp', 'scoringEngine': se.getId()})
		self.assertEquals(comp.name, 'Super Comp')

	def testCheck(self):
		pass

	def testCreateTeam(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp', 'scoringEngine': se.getId()})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		team = comp.createTeam(teamData)
		self.assertEquals(team.__class__.__name__, 'Team')

	# def testEditTeam(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	team = comp.createTeam(teamData)
	# 	comp.editTeam(teamId = team.getId(), networkCidr = '192.168.2.0/24')
	# 	self.assertEquals(team.networkCidr, '192.168.2.0/24')

	# def testGetTeam(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	comp.createTeam(teamData)
	# 	team = comp.getTeam(name = 'UAF Team')
	# 	self.assertEquals(team.__class__.__name__, 'Team')

	# def testGetTeams(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	teamData1 = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	teamData2 = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	comp.createTeam(teamData1)
	# 	comp.createTeam(teamData2)
	# 	teams = comp.getTeams()
	# 	self.assertEquals(len(teams), 2)
	# 	for i in teams:
	# 		self.assertEquals(i.__class__.__name__, 'Team')

	# def testDeleteTeam(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	comp.createTeam(teamData)
	# 	team = comp.getTeam(name = 'UAF Team')
	# 	comp.deleteTeam(teamId = team.getId())
	# 	teams = comp.getTeams()
	# 	self.assertEquals(len(teams), 0)

	def testCreateIncident(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp', 'scoringEngine': se.getId()})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		team = comp.createTeam(teamData)
		incidentData = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
		incident = comp.createIncident(incidentData)
		self.assertEquals(incident.__class__.__name__, 'Incident')

	# def testEditIncident(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	team = comp.createTeam(teamData)
	# 	incidentData = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
	# 	incident = comp.createIncident(incidentData)
	# 	comp.editIncident(incidentId = incident.getId(), content = 'Actually it was their firewall #rekt')
	# 	self.assertEquals(incident.getContent(), 'Actually it was their firewall #rekt')

	# def testGetIncident(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	team = comp.createTeam(teamData)
	# 	incidentData = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
	# 	comp.createIncident(incidentData)
	# 	incident = comp.getIncident(subject = 'We super hacked them')
	# 	self.assertEquals(incident.__class__.__name__, 'Incident')

	# def testGetIncidents(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	team = comp.createTeam(teamData)
	# 	incidentData1 = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
	# 	incidentData2 = {'teamId': team.getId(), 'subject':'Rooted as hell', 'content':'Very back door. Such exploit. Wow.'}
	# 	comp.createIncident(incidentData1)
	# 	comp.createIncident(incidentData2)
	# 	incidents = comp.getIncidents(teamId = team.getId())
	# 	for i in incidents:
	# 		self.assertEquals(i.__class__.__name__, 'Incident')

	# def testDeleteIncident(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	team = comp.createTeam(teamData)
	# 	incidentData = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
	# 	incident = comp.createIncident(incidentData)
	# 	comp.deleteIncident(incidentId = incident.getId())
	# 	incidents = comp.getIncidents()
	# 	self.assertEquals(len(incidents), 0)

	def testCreateIncidentResponse(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp', 'scoringEngine': se.getId()})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		team = comp.createTeam(teamData)
		incidentData = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
		incident = comp.createIncident(incidentData)
		incidentResponseData = {'teamId': team.getId(), 'incidentId': incident.getId(), 'content':"That wasn't our password! It was a default..", 'replyTo': -1}
		incidentResponse = comp.createIncidentResponse(incidentResponseData)
		self.assertEquals(incidentResponse.__class__.__name__, 'IncidentResponse')

	# def testEditIncidentResponse(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	team = comp.createTeam(teamData)
	# 	incidentData = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
	# 	incident = comp.createIncident(incidentData)
	# 	incidentResponseData = {'teamId': team.getId(), 'incidentId': incident.getId(), 'content':"That wasn't our password! It was a default..", 'replyTo': -1}
	# 	incidentResponse = comp.createIncidentResponse(incidentResponseData)
	# 	comp.editIncidentResponse(incidentResponseId = incidentResponse.getId(), content = 'Changed content!')
	# 	self.assertEquals(incidentResponse.getContent(), 'Changed content!')

	# def testGetIncidentResponse(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	team = comp.createTeam(teamData)
	# 	incidentData = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
	# 	incident = comp.createIncident(incidentData)
	# 	incidentResponseData = {'teamId': team.getId(), 'incidentId': incident.getId(), 'content': "That wasn't our password! It was a default..", 'replyTo': -1}
	# 	comp.createIncidentResponse(incidentResponseData)
	# 	incidentResponse = comp.getIncidentResponse(content = "That wasn't our password! It was a default..")
	# 	self.assertEquals(incidentResponse.__class__.__name__, 'IncidentResponse')

	# def testGetIncidentResponses(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	team = comp.createTeam(teamData)
	# 	incidentData = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
	# 	incident = comp.createIncident(incidentData)
	# 	incidentResponseData1 = {'teamId': team.getId(), 'incidentId': incident.getId(), 'content': "That wasn't our password! It was a default..", 'replyTo': -1}
	# 	incidentResponseData2 = {'teamId': team.getId(), 'incidentId': incident.getId(), 'content': 'This is another response.', 'replyTo': -1}
	# 	comp.createIncidentResponse(incidentResponseData1)
	# 	comp.createIncidentResponse(incidentResponseData2)
	# 	incidentResponses = comp.getIncidentResponses(teamId = team.getId(), incidentId = incident.getId())
	# 	self.assertEquals(len(incidentResponses), 2)
	# 	for i in incidentResponses:
	# 		self.assertEquals(i.__class__.__name__, 'IncidentResponse')

	# def testDeleteIncidentResponse(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	team = comp.createTeam(teamData)
	# 	incidentData = {'teamId': team.getId(), 'subject':'We super hacked them', 'content':'Their passwords suck! *mic drop*'}
	# 	incident = comp.createIncident(incidentData)
	# 	incidentResponseData = {'teamId': team.getId(), 'incidentId': incident.getId(), 'content': "That wasn't our password! It was a default..", 'replyTo': -1}
	# 	comp.createIncidentResponse(incidentResponseData)
	# 	incidentResponse = comp.getIncidentResponse(content = "That wasn't our password! It was a default..")
	# 	comp.deleteIncidentResponse(incidentResponseId = incidentResponse.getId())
	# 	incidentResponses = comp.getIncidentResponses()
	# 	self.assertEquals(len(incidentResponses), 0)

	def testCreateInject(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp', 'scoringEngine': se.getId()})
		inject = comp.createInject({'title':'Test Inject', 'body':'Test inject body'})
		self.assertEquals(inject.__class__.__name__, 'Inject')

	# def testEditInject(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	inject = comp.createInject({'title':'Test Inject', 'body':'Test inject body'})
	# 	comp.editInject(injectId = inject.getId(), title = 'Different title')
	# 	self.assertEquals(inject.getTitle(), 'Different title')

	# def testGetInject(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	comp.createInject({'title':'Test Inject', 'body':'Test inject body'})
	# 	inject = comp.getInject(title = 'Test Inject')
	# 	self.assertEquals(inject.__class__.__name__, 'Inject')

	# def testGetInjects(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	comp.createInject({'title':'Test Inject One', 'body':'Test inject one body'})
	# 	comp.createInject({'title':'Test Inject Two', 'body':'Test inject two body'})
	# 	injects = comp.getInjects()
	# 	self.assertEquals(len(injects), 2)
	# 	for i in injects:
	# 		self.assertEquals(i.__class__.__name__, 'Inject')

	# def testDeleteInject(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	inject = comp.createInject({'title':'Test Inject', 'body':'Test inject body'})
	# 	comp.deleteInject(injectId = inject.getId())
	# 	injects = comp.getInjects()
	# 	self.assertEquals(len(injects), 0)

	def testCreateInjectResponse(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp', 'scoringEngine': se.getId()})
		inject = comp.createInject({'title':'Test Inject', 'body':'Test inject body'})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		team = comp.createTeam(teamData)
		injectResponseData = {'teamId': team.getId(), 'injectId': inject.getId(), 'content': 'Inject response content', 'replyTo': inject.getId()}
		injectResponse = comp.createInjectResponse(injectResponseData)
		self.assertEquals(injectResponse.__class__.__name__, 'InjectResponse')

	# def testEditInjectResponse(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	inject = comp.createInject({'title':'Test Inject', 'body':'Test inject body'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	team = comp.createTeam(teamData)
	# 	injectResponseData = {'teamId': team.getId(), 'injectId': inject.getId(), 'content': 'Inject response content'}
	# 	injectResponse = comp.createInjectResponse(injectResponseData)
	# 	comp.editInjectResponse(injectResponseId = injectResponse.getId(), content = 'New content')
	# 	self.assertEquals(injectResponse.getContent(), 'New content')

	# def testGetInjectResponse(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	inject = comp.createInject({'title':'Test Inject', 'body':'Test inject body'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	team = comp.createTeam(teamData)
	# 	injectResponseData = {'teamId': team.getId(), 'injectId': inject.getId(), 'content': 'Inject response content', 'replyTo': inject.getId()}
	# 	comp.createInjectResponse(injectResponseData)
	# 	injectResponse = comp.getInjectResponse(content = 'Inject response')
	# 	self.assertEquals(injectResponse.__class__.__name__, 'InjectResponse')

	# def testGetInjectResponses(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	inject = comp.createInject({'title':'Test Inject', 'body':'Test inject body'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	team = comp.createTeam(teamData)
	# 	injectResponseData1 = {'teamId': team.getId(), 'injectId': inject.getId(), 'content': 'Inject response content one', 'replyTo': -1}
	# 	injectResponseData2 = {'teamId': team.getId(), 'injectId': inject.getId(), 'content': 'Inject response content two', 'replyTo': -1}
	# 	comp.createInjectResponse(injectResponseData1)
	# 	comp.createInjectResponse(injectResponseData2)
	# 	injectResponses = comp.getInjectResponses(injectId = inject.getId())
	# 	self.assertEquals(len(injectResponses), 2)
	# 	for i in injectResponses:
	# 		self.assertEquals(i.__class__.__name__, 'InjectResponse')

	# def testDeleteInjectResponse(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	inject = comp.createInject({'title':'Test Inject', 'body':'Test inject body'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	team = comp.createTeam(teamData)
	# 	injectResponseData = {'teamId': team.getId(), 'injectId': inject.getId(), 'content': 'Inject response content', 'replyTo': inject.getId()}
	# 	comp.createInjectResponse(injectResponseData)
	# 	injectResponse = comp.getInjectResponse(content = 'Inject response')
	# 	comp.deleteInjectResponse(injectResponse.getId())
	# 	injectResponses = comp.getInjectResponses(injectId = injectId.get())
	# 	self.assertEquals(len(injectResponses), 0)

	def testCreateScore(self):
		org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
		se = createScoringEngine({'name':'CSSEF SE', 'packageName':'CssefScoringEngine', 'ownership':1, 'disabled':False})
		comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp', 'scoringEngine': se.getId()})
		teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
		team = comp.createTeam(teamData)
		score = comp.createScore({'teamId': team.getId(), 'value': 100, 'message': 'Scored up!'})
		self.assertEquals(score.__class__.__name__, 'Score')

	# def testEditScore(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	team = comp.createTeam(teamData)
	# 	score = comp.createScore({'teamId': team.getId(), 'value': 100, 'message': 'Scored up!'})
	# 	comp.editScore(scoreId = score.getId(), message = 'This is a new message.')
	# 	self.assertEquals(score.getMessage(), 'This is a new message.')

	# def testGetScore(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	team = comp.createTeam(teamData)
	# 	score = comp.createScore({'teamId': team.getId(), 'value': 100, 'message': 'Scored up!'})
	# 	gotScore = comp.getScore(scoreId = score.getId())
	# 	self.assertEquals(gotScore.__class__.__name__, 'Score')

	# def testGetScores(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	team = comp.createTeam(teamData)
	# 	comp.createScore({'teamId': team.getId(), 'value': 100, 'message': 'Scored up!'})
	# 	comp.createScore({'teamId': team.getId(), 'value': 0, 'message': 'Scored down :('})
	# 	scores = comp.getScores()
	# 	self.assertEquals(len(scores), 2)
	# 	for i in scores:
	# 		self.assertEquals(i.__class__.__name__, 'Score')

	# def testDeleteScore(self):
	# 	org = createOrganization({'name': 'New Org', 'url': 'new_org', 'maxCompetitions': 5})
	# 	comp = org.createCompetition({'name': 'Super Comp', 'url': 'super_comp'})
	# 	teamData = {'name': 'UAF Team', 'username': 'uafteam', 'password': 'U@fR0(k5', 'networkCidr': '192.168.1.0/24'}
	# 	team = comp.createTeam(teamData)
	# 	score = comp.createScore({'teamId': team.getId(), 'value': 100, 'message': 'Scored up!'})
	# 	comp.deleteScore(scoreId = score.getId())
	# 	scores = comp.getScores()
	# 	self.assertEquals(len(scores), 0)

class TeamEndpoints(TestCase):
	pass

class ScoreEndpoints(TestCase):
	pass

class InjectEndpoints(TestCase):
	pass

class InjectResponseEndpoints(TestCase):
	pass

class IncidentEndpoints(TestCase):
	pass

class IncidentResponseEndpoints(TestCase):
	pass