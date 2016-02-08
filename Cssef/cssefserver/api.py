from __future__ import absolute_import
import traceback
from cssefserver.framework.core import *
from cssefserver.framework.competition import *
from cssefserver.framework.utils import databaseConnection
from celery import Celery

versionMajor = '0'
versionMinor = '0'
versionPatch = '1'
version = ".".join([versionMajor, versionMinor, versionPatch])

# Todo: pull the backend url from the config file instead of hardcoding
CssefCeleryApp = Celery(
	'api',
	backend='rpc://cssefd:cssefd-pass@localhost//',
	broker='amqp://cssefd:cssefd-pass@localhost//')

# Todo: pull the sqlite database path from the config file instead of hardcoding
dbPath = '/home/sk4ly/Documents/cssef/Cssef/db.sqlite3'

def getEmptyReturnDict():
	return {
		'value': 0,
		'message': 'Success',
		'content': []
	}

def modelDel(cls, pkid):
	db = databaseConnection(dbPath)
	if pkid == "*":
		# todo: implement a wildcard
		returnDict = getEmptyReturnDict()
		returnDict['value'] = 1
		returnDict['message'] = ["Wildcards are not implemented yet."]
		return returnDict
	elif type(pkid) == str and "-" in pkid:
		x = pkid.split("-")
		if len(x) == 2:
			try:
				for pkid in range(int(x[0]), int(x[1])+1):
					modelObj = cls.fromDatabase(db, pkid)
					if modelObj:
						modelObj.delete()
			except ValueError:
				# One of the ranges provided could not be cast as an integer. Return error.
				returnDict = getEmptyReturnDict()
				returnDict['value'] = 1
				returnDict['message'] = ["Range value could not be cast to integer. Expected integer range like 1-4. Got '%s' instead." % pkid]
				return returnDict
		else:
			print x
			returnDict = getEmptyReturnDict()
			returnDict['value'] = 1
			returnDict['message'] = ["Expected integer range like 1-4. Got '%s' instead." % pkid]
			return returnDict
	elif type(pkid) == int:
		modelObj = cls.fromDatabase(db, pkid)
		modelObj.delete()
	else:
		# We don't know what the hell we were given. Disregard it and thow an error :(
		returnDict = getEmptyReturnDict()
		returnDict['value'] = 1
		returnDict['message'] = ["Expected integer value (5) or range (2-7). Got '%s' of type %s instead." % (str(pkid), str(type(pkid)))]
	return getEmptyReturnDict()

def modelSet(cls, pkid, **kwargs):
	db = databaseConnection(dbPath)
	modelObj = cls.fromDatabase(db, pkid)
	modelObj.edit(**kwargs)
	returnDict = getEmptyReturnDict()
	returnDict['content'].append(modelObj.asDict())
	return returnDict

def modelGet(cls, **kwargs):
	db = databaseConnection(dbPath)
	modelObjs = cls.search(db, **kwargs)
	returnDict = getEmptyReturnDict()
	for i in modelObjs:
		returnDict['content'].append(i.asDict())
	return returnDict

def handleException(e):
	# todo
	# log the full stacktrace!
	returnDict = getEmptyReturnDict()
	returnDict['value'] = 1
	returnDict['message'] = traceback.format_exc().splitlines()
	return returnDict

# ==================================================
# Competition Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'competitionAdd')
def competitionAdd(organization = None, **kwargs):
	try:
		if not organization:
			raise Exception
		db = databaseConnection(dbPath)
		organization = Organization.fromDatabase(db, organization)
		competition = organization.createCompetition(kwargs)
		returnDict = getEmptyReturnDict()
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
		db = databaseConnection(dbPath)
		competitionObj = Competition.fromDatabase(db, competition)
		tmpDict = kwargs
		tmpDict['competition'] = competitionObj.getId()
		team = Team.fromDict(db, tmpDict)
		returnDict = getEmptyReturnDict()
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
		db = databaseConnection(dbPath)
		competitionObj = Competition.fromDatabase(db, competition)
		tmpDict = kwargs
		tmpDict['competition'] = competitionObj.getId()
		score = Score.fromDict(db, tmpDict)
		returnDict = getEmptyReturnDict()
		returnDict['content'].append(score.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionScoreDel')
def competitionScoreDel(pkid = None):
	try:
		if not pkid:
			raise Exception
		return modelDel(Score, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionScoreSet')
def competitionScoreSet(pkid = None, **kwargs):
	try:
		if not pkid:
			raise Exception
		return modelSet(Score, pkid, **kwargs)
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
		db = databaseConnection(dbPath)
		competitionObj = Competition.fromDatabase(db, competition)
		tmpDict = kwargs
		tmpDict['competition'] = competitionObj.getId()
		inject = Inject.fromDict(db, tmpDict)
		returnDict = getEmptyReturnDict()
		returnDict['content'].append(inject.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionInjectDel')
def competitionInjectDel(pkid = None):
	try:
		if not pkid:
			raise Exception
		return modelDel(Inject, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionInjectSet')
def competitionInjectSet(pkid = None, **kwargs):
	try:
		if not pkid:
			raise Exception
		return modelSet(Inject, pkid, **kwargs)
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
		db = databaseConnection(dbPath)
		competitionObj = Competition.fromDatabase(db, competition)
		tmpDict = kwargs
		tmpDict['competition'] = competitionObj.getId()
		injectResponse = InjectResponse.fromDict(db, tmpDict)
		returnDict = getEmptyReturnDict()
		returnDict['content'].append(injectResponse.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionInjectResponseDel')
def competitionInjectResponseDel(pkid = None):
	try:
		if not pkid:
			raise Exception
		return modelDel(InjectResponse, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionInjectResponseSet')
def competitionInjectResponseSet(pkid = None, **kwargs):
	try:
		if not pkid:
			raise Exception
		return modelSet(InjectResponse, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionInjectResponseGet')
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
		db = databaseConnection(dbPath)
		competitionObj = Competition.fromDatabase(db, competition)
		tmpDict = kwargs
		tmpDict['competition'] = competitionObj.getId()
		incident = Incident.fromDict(db, tmpDict)
		returnDict = getEmptyReturnDict()
		returnDict['content'].append(incident.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionIncidentDel')
def competitionIncidentDel(pkid = None):
	try:
		if not pkid:
			raise Exception
		return modelDel(Incident, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionIncidentSet')
def competitionIncidentSet(pkid = None, **kwargs):
	try:
		if not pkid:
			raise Exception
		return modelSet(Incident, pkid, **kwargs)
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
		db = databaseConnection(dbPath)
		competitionObj = Competition.fromDatabase(db, competition)
		tmpDict = kwargs
		tmpDict['competition'] = competitionObj.getId()
		incidentResponse = IncidentResponse.fromDict(db, tmpDict)
		returnDict = getEmptyReturnDict()
		returnDict['content'].append(incidentResponse.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionIncidentResponseDel')
def competitionIncidentResponseDel(pkid = None):
	try:
		if not pkid:
			raise Exception
		return modelDel(IncidentResponse, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionIncidentResponseSet')
def competitionIncidentResponseSet(pkid = None, **kwargs):
	try:
		if not pkid:
			raise Exception
		return modelSet(IncidentResponse, pkid, **kwargs)
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
		db = databaseConnection(dbPath)
		organization = Organization.fromDict(db, kwargs)
		returnDict = getEmptyReturnDict()
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
		return modelGet(Organization, **kwargs)
	except Exception as e:
		return handleException(e)

# ==================================================
# User Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'userAdd')
def userAdd(organization = None, **kwargs):
	try:
		db = databaseConnection(dbPath)
		organization = Organization.fromDatabase(db, organization)
		user = organization.createMember(kwargs)
		returnDict = getEmptyReturnDict()
		returnDict['content'].append(user.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'userDel')
def userDel(pkid = None):
	try:
		if not pkid:
			raise Exception
		return modelDel(User, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'userSet')
def userSet(pkid = None, **kwargs):
	try:
		if not pkid:
			raise Exception
		return modelSet(User, pkid, **kwargs)
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
		db = databaseConnection(dbPath)
		document = Document.fromDict(db, kwargs)
		returnDict = getEmptyReturnDict()
		returnDict['content'].append(document.asDict())
		return returnDict
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
		db = databaseConnection(dbPath)
		scoringEngine = ScoringEngine.fromDict(db, kwargs)
		returnDict = getEmptyReturnDict()
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
