from unittest import TestCase
from framework.utils import databaseConnection
from framework.competition import *
from framework.core import Organization
from datetime import datetime

dbPath = '/home/sk4ly/Documents/cssef/Cssef/db.sqlite3'
dictOrganization = {
	'name': 'T Org',
	'url': 't_org',
	'maxCompetitions': 1}
dictCompetition = {
	'name': 'T Comp',
	'url': 't_comp'}
dictTeam = {
	'name': 'T User',
	'username': 'tuser',
	'password': 'tpass',
	'networkCidr': '192.168.1.1'}
dictScore = {
	'value': 100,
	'message': 'Success'}
dictInject = {
	'requireResponse': True,
	'manualDelivery': False,
	'datetimeDelivery': datetime.now(),
	'datetimeResponseDue': datetime.now(),
	'datetimeResponseClose': datetime.now(),
	'title': 'T Inject',
	'body': 'T body.'}
dictInjectResponse = {
	'datetime': datetime.now(),
	'content': 'T Inject Response content'}
dictIncident = {
	'datetime': datetime.now(),
	'subject': 'T Incident',
	'content': 'T Incident content'}
dictIncidentResponse = {
	'replyTo': None,
	'datetime': datetime.now(),
	'subject': 'T Incident Response',
	'content': 'T Incident Response content'}

class CompetitionEndpoints(TestCase):
	def testCompetition_fromDict(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		self.assertTrue(isinstance(competition, Competition))

	def testCompetition_fromDatabase(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		competition = Competition.fromDatabase(dbConn, competition.getId())
		self.assertTrue(isinstance(competition, Competition))

	def testCompetition_delete(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		pkid = competition.getId()
		competition.delete()
		competition = Competition.fromDatabase(dbConn, pkid)
		self.assertEquals(None, competition)

class TeamEndpoints(TestCase):
	def testTeam_fromDict(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		team = Team.fromDict(dbConn, dictTeam)
		self.assertTrue(isinstance(team, Team))

	def testTeam_fromDatabase(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		team = Team.fromDict(dbConn, dictTeam)
		team = Team.fromDatabase(dbConn, team.getId())
		self.assertTrue(isinstance(team, Team))

	def testTeam_delete(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		team = Team.fromDict(dbConn, dictTeam)
		pkid = team.getId()
		team.delete()
		team = Team.fromDatabase(dbConn, pkid)
		self.assertEquals(None, team)

class ScoreEndpoints(TestCase):
	def testScore_fromDict(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		score = Score.fromDict(dbConn, dictScore)
		self.assertTrue(isinstance(score, Score))

	def testScore_fromDatabase(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		score = Score.fromDict(dbConn, dictScore)
		score = Score.fromDatabase(dbConn, score.getId())
		self.assertTrue(isinstance(score, Score))

	def testScore_delete(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		score = Score.fromDict(dbConn, dictScore)
		pkid = score.getId()
		score.delete()
		score = Score.fromDatabase(dbConn, pkid)
		self.assertEquals(None, score)

class InjectEndpoints(TestCase):
	def testInject_fromDict(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		inject = Inject.fromDict(dbConn, dictInject)
		self.assertTrue(isinstance(inject, Inject))

	def testInject_fromDatabase(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		inject = Inject.fromDict(dbConn, dictInject)
		inject = Inject.fromDatabase(dbConn, inject.getId())
		self.assertTrue(isinstance(inject, Inject))

	def testInject_delete(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		inject = Inject.fromDict(dbConn, dictInject)
		pkid = inject.getId()
		inject.delete()
		inject = Inject.fromDatabase(dbConn, pkid)
		self.assertEquals(None, inject)

class InjectResponseEndpoints(TestCase):
	def testInjectResponse_fromDict(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		injectResponse = InjectResponse.fromDict(dbConn, dictInjectResponse)
		self.assertTrue(isinstance(injectResponse, InjectResponse))

	def testInjectResponse_fromDatabase(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		injectResponse = InjectResponse.fromDict(dbConn, dictInjectResponse)
		injectResponse = InjectResponse.fromDatabase(dbConn, injectResponse.getId())
		self.assertTrue(isinstance(injectResponse, InjectResponse))

	def testInjectResponse_delete(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		injectResponse = InjectResponse.fromDict(dbConn, dictInjectResponse)
		pkid = injectResponse.getId()
		injectResponse.delete()
		injectResponse = InjectResponse.fromDatabase(dbConn, pkid)
		self.assertEquals(None, injectResponse)

class IncidentEndpoints(TestCase):
	def testIncident_fromDict(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		incident = Incident.fromDict(dbConn, dictIncident)
		self.assertTrue(isinstance(incident, Incident))

	def testIncident_fromDatabase(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		incident = Incident.fromDict(dbConn, dictIncident)
		incident = Incident.fromDatabase(dbConn, incident.getId())
		self.assertTrue(isinstance(incident, Incident))

	def testIncident_delete(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		incident = Incident.fromDict(dbConn, dictIncident)
		pkid = incident.getId()
		incident.delete()
		incident = Incident.fromDatabase(dbConn, pkid)
		self.assertEquals(None, incident)

class IncidentResponseEndpoints(TestCase):
	def testIncidentResponse_fromDict(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		incidentResponse = IncidentResponse.fromDict(dbConn, dictIncidentResponse)
		self.assertTrue(isinstance(incidentResponse, IncidentResponse))

	def testIncidentResponse_fromDatabase(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		incidentResponse = IncidentResponse.fromDict(dbConn, dictIncidentResponse)
		incidentResponse = IncidentResponse.fromDatabase(dbConn, incidentResponse.getId())
		self.assertTrue(isinstance(incidentResponse, IncidentResponse))

	def testIncidentResponse_delete(self):
		dbConn = databaseConnection(dbPath)
		organization = Organization.fromDict(dbConn, dictOrganization)
		competition = Competition.fromDict(dbConn, dictCompetition)
		incidentResponse = IncidentResponse.fromDict(dbConn, dictIncidentResponse)
		pkid = incidentResponse.getId()
		incidentResponse.delete()
		incidentResponse = IncidentResponse.fromDatabase(dbConn, pkid)
		self.assertEquals(None, incidentResponse)
