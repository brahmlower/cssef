from __future__ import absolute_import
import traceback
from framework.core import *
from framework.competition import *
from framework.utils import databaseConnection


from celery import Celery
celeryApp = Celery('api', backend='rpc://butts:butts@localhost//', broker='amqp://butts:butts@localhost//')

EmptyReturnDict = {
	'value': 0,
	'message': 'Success',
	'content': []
}

def modelDel(cls, db, pkid):
	modelObj = cls.fromDatabase(db, pkid)
	modelObj.delete()
	return EmptyReturnDict

def modelSet(cls, db, pkid, **kwargs):
	modelObj = cls.fromDatabase(db, pkid)
	modelObj.edit(**kwargs)
	returnDict = EmptyReturnDict
	returnDict['content'].append(modelObj.asDict())
	return returnDict

def modelGet(cls, db, **kwargs):
	modelObjs = cls.search(db, **kwargs)
	returnDict = EmptyReturnDict
	for i in modelObjs:
		returnDict['content'].append(i.asDict())
	return returnDict

def handleException(e):
	# todo
	# log the full stacktrace!
	returnDict = EmptyReturnDict
	returnDict['value'] = 1
	returnDict['message'] = traceback.format_exc().splitlines()
	return returnDict

# ==================================================
# Competition Endpoints
# ==================================================
@celeryApp.task(name = 'competitionAdd')
def competitionAdd(organization = None, name = None, **kwargs):
	if not organization or not name:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	organization = Organization.fromDatabase(db, organization)
	competition = organization.createCompetition(db, kwargs)
	returnDict = EmptyReturnDict
	returnDict['content'].append(competition.asDict())
	return returnDict

@celeryApp.task(name = 'competitionDel')
def competitionDel(competition = None):
	if not competition:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelDel(Competition, db, competition)

@celeryApp.task(name = 'competitionSet')
def competitionSet(competition = None, **kwargs):
	if not competition:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelSet(Competition, db, competition, **kwargs)

@celeryApp.task(name = 'competitionGet')
def competitionGet(**kwargs):
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelGet(Competition, db, **kwargs)

# ==================================================
# Team Endpoints
# ==================================================
@celeryApp.task(name = 'competitionTeamAdd')
def competitionTeamAdd(competition = None, **kwargs):
	if not competition:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	competitionObj = Competition.fromDatabase(db, competition)
	team = competitionObj.createTeam(**kwargs)
	returnDict = EmptyReturnDict
	returnDict['content'].append(team.asDict())
	return returnDict

@celeryApp.task(name = 'competitionTeamDel')
def competitionTeamDel(team = None):
	if not team:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelDel(Team, db, team)

@celeryApp.task(name = 'competitionTeamSet')
def competitionTeamSet(team = None, **kwargs):
	if not team:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelSet(Team, db, team, **kwargs)

@celeryApp.task(name = 'competitionTeamGet')
def competitionTeamGet(**kwargs):
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelGet(Team, db, **kwargs)

# ==================================================
# Score Endpoints
# ==================================================

@celeryApp.task(name = 'competitionTeamAdd')
def competitionScoreAdd(competition = None, **kwargs):
	if not competition:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	competitionObj = Competition.fromDatabase(db, competition)
	score = competitionObj.createScore(**kwargs)
	returnDict = EmptyReturnDict
	returnDict['content'].append(score.asDict())
	return returnDict

@celeryApp.task(name = 'competitionTeamDel')
def competitionScoreDel(score = None):
	if not score:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelDel(Score, db, score)

@celeryApp.task(name = 'competitionTeamSet')
def competitionScoreSet(score = None, **kwargs):
	if not score:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelSet(Score, db, score, **kwargs)

@celeryApp.task(name = 'competitionTeamGet')
def competitionScoreGet(**kwargs):
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelGet(Score, db, **kwargs)

# ==================================================
# Inject Endpoints
# ==================================================
@celeryApp.task(name = 'competitionInjectAdd')
def competitionInjectAdd(competition = None, **kwargs):
	if not competition:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	competitionObj = Competition.fromDatabase(db, competition)
	inject = competitionObj.createInject(**kwargs)
	returnDict = EmptyReturnDict
	returnDict['content'].append(inject.asDict())
	return returnDict

@celeryApp.task(name = 'competitionInjectDel')
def competitionInjectDel(inject = None):
	if not inject:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelDel(Inject, db, inject)

@celeryApp.task(name = 'competitionInjectSet')
def competitionInjectSet(inject = None, **kwargs):
	if not inject:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelSet(Inject, db, inject, **kwargs)

@celeryApp.task(name = 'competitionInjectGet')
def competitionInjectGet(**kwargs):
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelGet(Inject, db, **kwargs)

# ==================================================
# Inject Response Endpoints
# ==================================================
@celeryApp.task(name = 'competitionInjectResponseAdd')
def competitionInjectResponseAdd(competition = None, **kwargs):
	if not competition:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	competitionObj = Competition.fromDatabase(db, competition)
	injectResponse = competitionObj.createInjectResponse(**kwargs)
	returnDict = EmptyReturnDict
	returnDict['content'].append(injectResponse.asDict())
	return returnDict

@celeryApp.task(name = 'competitionInjectResponseDel')
def competitionInjectResponseDel(injectResponse = None):
	if not injectResponse:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelDel(InjectResponse, db, injectResponse)

@celeryApp.task(name = 'competitionInjectResponseSet')
def competitionInjectResponseSet(injectResponse = None, **kwargs):
	if not injectResponse:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelSet(InjectResponse, db, injectResponse, **kwargs)

@celeryApp.task(name = 'competitionInjectResponseDel')
def competitionInjectResponseGet(**kwargs):
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelGet(InjectResponse, db, **kwargs)

# ==================================================
# Incident Endpoints
# ==================================================
@celeryApp.task(name = 'competitionIncidentAdd')
def competitionIncidentAdd(competition = None, **kwargs):
	if not competition:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	competitionObj = Competition.fromDatabase(db, competition)
	incident = competitionObj.createIncident(**kwargs)
	returnDict = EmptyReturnDict
	returnDict['content'].append(incident.asDict())
	return returnDict

@celeryApp.task(name = 'competitionIncidentDel')
def competitionIncidentDel(incident = None):
	if not incident:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelDel(Incident, db, incident)

@celeryApp.task(name = 'competitionIncidentSet')
def competitionIncidentSet(incident = None, **kwargs):
	if not incident:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelSet(Incident, db, incident, **kwargs)

@celeryApp.task(name = 'competitionIncidentGet')
def competitionIncidentGet(**kwargs):
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelGet(Incident, db, **kwargs)

# ==================================================
# Incident Response Endpoints
# ==================================================
@celeryApp.task(name = 'competitionIncidentResponseAdd')
def competitionIncidentResponseAdd(competition = None, **kwargs):
	if not competition:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	competitionObj = Competition.fromDatabase(db, competition)
	incidentResponse = competitionObj.createIncidentResponse(**kwargs)
	returnDict = EmptyReturnDict
	returnDict['content'].append(incidentResponse.asDict())
	return returnDict

@celeryApp.task(name = 'competitionIncidentResponseDel')
def competitionIncidentResponseDel(incidentResponse = None):
	if not incidentResponse:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelDel(IncidentResponse, db, incidentResponse)

@celeryApp.task(name = 'competitionIncidentResponseSet')
def competitionIncidentResponseSet(incidentResponse = None, **kwargs):
	if not incidentResponse:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelSet(IncidentResponse, db, incidentResponse, **kwargs)

@celeryApp.task(name = 'competitionIncidentResponseGet')
def compeititonIncidentResponseGet(**kwargs):
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelGet(IncidentResponse, db, **kwargs)

# ==================================================
# Organization Endpoints
# ==================================================
@celeryApp.task(name = 'organizationAdd')
def organizationAdd(**kwargs):
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	organization = Organization.fromDict(db, kwargs)
	returnDict = EmptyReturnDict
	returnDict['content'].append(organization.asDict())
	return returnDict

@celeryApp.task(name = 'organizationDel')
def organizationDel(organization = None):
	try:
		if not organization:
			raise Exception
		db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
		return modelDel(Organization, db, organization)
	except Exception as e:
		return handleException(e)

@celeryApp.task(name = 'organizationSet')
def organizationSet(pkid = None, **kwargs):
	try:
		if not pkid:
			raise Exception
		db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
		return modelSet(Organization, db, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@celeryApp.task(name = 'organizationGet')
def organizationGet(**kwargs):
	try:
		db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
		return modelGet(Organization, db, **kwargs)
	except Exception as e:
		return handleException(e)

# ==================================================
# User Endpoints
# ==================================================
@celeryApp.task(name = 'userAdd')
def userAdd(organization = None, **kwargs):
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	organization = Organization.fromDatabase(pkid = organization)
	user = organization.createMember(**kwargs)
	returnDict = EmptyReturnDict
	returnDict['content'].append(user.asDict())
	return returnDict

@celeryApp.task(name = 'userDel')
def userDel(user = None):
	if not user:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelDel(User, db, user)

@celeryApp.task(name = 'userSet')
def userSet(user = None, **kwargs):
	if not user:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelSet(User, db, user, **kwargs)

@celeryApp.task(name = 'userGet')
def userGet(**kwargs):
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelGet(User, db, **kwargs)


# ==================================================
# Document Endpoints
# ==================================================
@celeryApp.task(name = 'documentAdd')
def documentAdd(**kwargs):
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	document = Document.fromDict(db, kwargs)
	returnDict = EmptyReturnDict
	returnDict['content'].append(document.asDict())
	return returnDict

@celeryApp.task(name = 'documentDel')
def documentDel(document = None):
	if not document:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelDel(Document, db, document)

@celeryApp.task(name = 'documentSet')
def documentSet(document = None, **kwargs):
	if not document:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelSet(Document, db, document, **kwargs)

@celeryApp.task(name = 'documentGet')
def documentGet(**kwargs):
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelGet(Document, db, **kwargs)


# ==================================================
# Scoring Engine Endpoints
# ==================================================
@celeryApp.task(name = 'scoringEngineAdd')
def scoringengineAdd(**kwargs):
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	scoringEngine = ScoringEngine.fromDict(db, kwargs)
	returnDict = EmptyReturnDict
	returnDict['content'].append(scoringEngine.asDict())
	return returnDict

@celeryApp.task(name = 'scoringEngineDel')
def scoringengineDel(scoringEngine = None):
	if not scoringEngine:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelDel(ScoringEngine, db, scoringEngine)

@celeryApp.task(name = 'scoringEngineSet')
def scoringengineSet(scoringEngine = None, **kwargs):
	if not scoringEngine:
		raise Exception
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelSet(ScoringEngine, db, scoringEngine, **kwargs)

@celeryApp.task(name = 'scoringEngineGet')
def scoringengineGet(**kwargs):
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	return modelGet(ScoringEngine, db, **kwargs)
