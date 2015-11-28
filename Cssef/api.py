from __future__ import absolute_import
import traceback
from framework.core import *
from framework.competition import *
from framework.utils import databaseConnection

from celery import Celery
CssefCeleryApp = Celery('api', backend='rpc://cssefd:cssefd-pass@localhost//', broker='amqp://cssefd:cssefd-pass@localhost//')

EmptyReturnDict = {
	'value': 0,
	'message': 'Success',
	'content': []
}

def modelDel(cls, pkid):
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	modelObj = cls.fromDatabase(db, pkid)
	modelObj.delete()
	return EmptyReturnDict

def modelSet(cls, pkid, **kwargs):
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	modelObj = cls.fromDatabase(db, pkid)
	modelObj.edit(**kwargs)
	returnDict = EmptyReturnDict
	returnDict['content'].append(modelObj.asDict())
	return returnDict

def modelGet(cls, **kwargs):
	db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
	modelObjs = cls.search(db, **kwargs)
	returnDict = EmptyReturnDict
	for i in modelObjs:
		returnDict['content'].append(i.asDict())
	print returnDict
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
@CssefCeleryApp.task(name = 'competitionAdd')
def competitionAdd(organization = None, name = None, **kwargs):
	try:
		if not organization or not name:
			raise Exception
		db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
		organization = Organization.fromDatabase(db, organization)
		competition = organization.createCompetition(db, kwargs)
		returnDict = EmptyReturnDict
		returnDict['content'].append(competition.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionDel')
def competitionDel(pkid = None):
	try:
		if not pkid:
			raise Exception
		return modelDel(Competition, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionSet')
def competitionSet(pkid = None, **kwargs):
	try:
		if not pkid:
			raise Exception
		return modelSet(Competition, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionGet')
def competitionGet(**kwargs):
	try:
		return modelGet(Competition, **kwargs)
	except Exception as e:
		return handleException(e)

# ==================================================
# Team Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'competitionTeamAdd')
def competitionTeamAdd(competition = None, **kwargs):
	try:
		if not competition:
			raise Exception
		db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
		competitionObj = Competition.fromDatabase(db, competition)
		#team = competitionObj.createTeam(**kwargs)
		tmpDict = kwargs
		tmpDict['competition'] = competitionObj.getId()
		team = Team.fromDict(db, tmpDict)
		returnDict = EmptyReturnDict
		returnDict['content'].append(team.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionTeamDel')
def competitionTeamDel(pkid = None):
	try:
		if not pkid:
			raise Exception
		return modelDel(Team, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionTeamSet')
def competitionTeamSet(pkid = None, **kwargs):
	try:
		if not pkid:
			raise Exception
		return modelSet(Team, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionTeamGet')
def competitionTeamGet(**kwargs):
	try:
		return modelGet(Team, **kwargs)
	except Exception as e:
		return handleException(e)

# ==================================================
# Score Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'competitionScoreAdd')
def competitionScoreAdd(competition = None, **kwargs):
	try:
		if not competition:
			raise Exception
		db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
		competitionObj = Competition.fromDatabase(db, competition)
		tmpDict = kwargs
		tmpDict['competition'] = competitionObj.getId()
		score = Score.fromDict(tmpDict)
		returnDict = EmptyReturnDict
		returnDict['content'].append(score.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionScoreDel')
def competitionScoreDel(score = None):
	try:
		if not score:
			raise Exception
		return modelDel(Score, score)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionScoreSet')
def competitionScoreSet(score = None, **kwargs):
	try:
		if not score:
			raise Exception
		return modelSet(Score, score, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionScoreGet')
def competitionScoreGet(**kwargs):
	try:
		return modelGet(Score, **kwargs)
	except Exception as e:
		return handleException(e)

# ==================================================
# Inject Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'competitionInjectAdd')
def competitionInjectAdd(competition = None, **kwargs):
	try:
		if not competition:
			raise Exception
		db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
		competitionObj = Competition.fromDatabase(db, competition)
		tmpDict = kwargs
		tmpDict['competition'] = competitionObj.getId()
		inject = Inject.fromDict(tmpDict)
		returnDict = EmptyReturnDict
		returnDict['content'].append(inject.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionInjectDel')
def competitionInjectDel(inject = None):
	try:
		if not inject:
			raise Exception
		return modelDel(Inject, inject)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionInjectSet')
def competitionInjectSet(inject = None, **kwargs):
	try:
		if not inject:
			raise Exception
		return modelSet(Inject, inject, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionInjectGet')
def competitionInjectGet(**kwargs):
	try:
		return modelGet(Inject, **kwargs)
	except Exception as e:
		return handleException(e)

# ==================================================
# Inject Response Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'competitionInjectResponseAdd')
def competitionInjectResponseAdd(competition = None, **kwargs):
	try:
		if not competition:
			raise Exception
		db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
		competitionObj = Competition.fromDatabase(db, competition)
		tmpDict = kwargs
		tmpDict['competition'] = competitionObj.getId()
		injectResponse = InjectResponse.fromDict(tmpDict)
		returnDict = EmptyReturnDict
		returnDict['content'].append(injectResponse.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionInjectResponseDel')
def competitionInjectResponseDel(injectResponse = None):
	try:
		if not injectResponse:
			raise Exception
		return modelDel(InjectResponse, injectResponse)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionInjectResponseSet')
def competitionInjectResponseSet(injectResponse = None, **kwargs):
	try:
		if not injectResponse:
			raise Exception
		return modelSet(InjectResponse, injectResponse, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionInjectResponseDel')
def competitionInjectResponseGet(**kwargs):
	try:
		return modelGet(InjectResponse, **kwargs)
	except Exception as e:
		return handleException(e)

# ==================================================
# Incident Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'competitionIncidentAdd')
def competitionIncidentAdd(competition = None, **kwargs):
	try:
		if not competition:
			raise Exception
		db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
		competitionObj = Competition.fromDatabase(db, competition)
		tmpDict = kwargs
		tmpDict['competition'] = competitionObj.getId()
		incident = Incident.fromDict(tmpDict)
		returnDict = EmptyReturnDict
		returnDict['content'].append(incident.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionIncidentDel')
def competitionIncidentDel(incident = None):
	try:
		if not incident:
			raise Exception
		return modelDel(Incident, incident)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionIncidentSet')
def competitionIncidentSet(incident = None, **kwargs):
	try:
		if not incident:
			raise Exception
		return modelSet(Incident, incident, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionIncidentGet')
def competitionIncidentGet(**kwargs):
	try:
		return modelGet(Incident, **kwargs)
	except Exception as e:
		return handleException(e)

# ==================================================
# Incident Response Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'competitionIncidentResponseAdd')
def competitionIncidentResponseAdd(competition = None, **kwargs):
	try:
		if not competition:
			raise Exception
		db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
		competitionObj = Competition.fromDatabase(db, competition)
		tmpDict = kwargs
		tmpDict['competition'] = competitionObj.getId()
		incidentResponse = IncidentResponse.fromDict(tmpDict)
		returnDict = EmptyReturnDict
		returnDict['content'].append(incidentResponse.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionIncidentResponseDel')
def competitionIncidentResponseDel(incidentResponse = None):
	try:
		if not incidentResponse:
			raise Exception
		return modelDel(IncidentResponse, incidentResponse)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionIncidentResponseSet')
def competitionIncidentResponseSet(incidentResponse = None, **kwargs):
	try:
		if not incidentResponse:
			raise Exception
		return modelSet(IncidentResponse, incidentResponse, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionIncidentResponseGet')
def compeititonIncidentResponseGet(**kwargs):
	try:
		return modelGet(IncidentResponse, **kwargs)
	except Exception as e:
		return handleException(e)

# ==================================================
# Organization Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'organizationAdd')
def organizationAdd(**kwargs):
	try:
		db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
		organization = Organization.fromDict(db, kwargs)
		returnDict = EmptyReturnDict
		returnDict['content'].append(organization.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'organizationDel')
def organizationDel(pkid = None):
	try:
		if not pkid:
			raise Exception
		return modelDel(Organization, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'organizationSet')
def organizationSet(pkid = None, **kwargs):
	try:
		if not pkid:
			raise Exception
		return modelSet(Organization, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'organizationGet')
def organizationGet(**kwargs):
	try:
		x = modelGet(Organization, **kwargs)
		print x
		return x
	except Exception as e:
		return handleException(e)

# ==================================================
# User Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'userAdd')
def userAdd(organization = None, **kwargs):
	try:
		db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
		organization = Organization.fromDatabase(pkid = organization)
		user = organization.createMember(**kwargs)
		returnDict = EmptyReturnDict
		returnDict['content'].append(user.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'userDel')
def userDel(user = None):
	try:
		if not user:
			raise Exception
		return modelDel(User, user)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'userSet')
def userSet(user = None, **kwargs):
	try:
		if not user:
			raise Exception
		return modelSet(User, user, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'userGet')
def userGet(**kwargs):
	try:
		return modelGet(User, **kwargs)
	except Exception as e:
		return handleException(e)


# ==================================================
# Document Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'documentAdd')
def documentAdd(**kwargs):
	try:
		db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
		document = Document.fromDict(db, kwargs)
		returnDict = EmptyReturnDict
		returnDict['content'].append(document.asDict())
		return returnDic
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'documentDel')
def documentDel(document = None):
	try:
		if not document:
			raise Exception
		return modelDel(Document, document)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'documentSet')
def documentSet(document = None, **kwargs):
	try:
		if not document:
			raise Exception
		return modelSet(Document, document, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'documentGet')
def documentGet(**kwargs):
	try:
		return modelGet(Document, **kwargs)
	except Exception as e:
		return handleException(e)


# ==================================================
# Scoring Engine Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'scoringEngineAdd')
def scoringengineAdd(**kwargs):
	try:
		db = databaseConnection('/home/sk4ly/Documents/cssef/Cssef/db.sqlite3')
		scoringEngine = ScoringEngine.fromDict(db, kwargs)
		returnDict = EmptyReturnDict
		returnDict['content'].append(scoringEngine.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'scoringEngineDel')
def scoringengineDel(scoringEngine = None):
	try:
		if not scoringEngine:
			raise Exception
		return modelDel(ScoringEngine, scoringEngine)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'scoringEngineSet')
def scoringengineSet(scoringEngine = None, **kwargs):
	try:
		if not scoringEngine:
			raise Exception
		return modelSet(ScoringEngine, scoringEngine, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'scoringEngineGet')
def scoringengineGet(**kwargs):
	try:
		return modelGet(ScoringEngine, **kwargs)
	except Exception as e:
		return handleException(e)
