from cssefserver.framework.utils import databaseConnection
from cssefserver.framework.utils import handleException
from cssefserver.framework.utils import getEmptyReturnDict
from cssefserver.framework.utils import modelDel
from cssefserver.framework.utils import modelSet
from cssefserver.framework.utils import modelGet
from cssefserver.framework import CssefCeleryApp
from cssefserver.framework import dbPath
from cssefserver.modules.account import Organization
from cssefserver.modules.competition import Competition
from cssefserver.modules.competition import Team
from cssefserver.modules.competition import Score
from cssefserver.modules.competition import Inject
from cssefserver.modules.competition import InjectResponse
from cssefserver.modules.competition import Incident
from cssefserver.modules.competition import IncidentResponse
from cssefserver.modules.competition import ScoringEngine
from cssefserver.modules.account.utils import authorizeAccess

# ==================================================
# Competition Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'competitionAdd')
def competitionAdd(auth, organization = None, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
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
def competitionDel(auth, pkid = None):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelDel(Competition, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionSet')
def competitionSet(auth, pkid = None, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelSet(Competition, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionGet')
def competitionGet(auth, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		return modelGet(Competition, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionStart')
def competitionStart(auth, pkid = None):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		db = databaseConnection(dbPath)
		competition = Competition.fromDatabase(db, pkid)
		if not competition.autoStart:
			raise Exception
		competition.start()
	except Exception as e:
		return handleException(e)

# ==================================================
# Team Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'competitionTeamAdd')
def competitionTeamAdd(auth, competition = None, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
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
def competitionTeamDel(auth, pkid = None):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelDel(Team, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionTeamSet')
def competitionTeamSet(auth, pkid = None, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelSet(Team, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionTeamGet')
def competitionTeamGet(auth, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		return modelGet(Team, **kwargs)
	except Exception as e:
		return handleException(e)

# ==================================================
# Score Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'competitionScoreAdd')
def competitionScoreAdd(auth, competition = None, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
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
def competitionScoreDel(auth, pkid = None):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelDel(Score, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionScoreSet')
def competitionScoreSet(auth, pkid = None, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelSet(Score, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionScoreGet')
def competitionScoreGet(auth, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		return modelGet(Score, **kwargs)
	except Exception as e:
		return handleException(e)

# ==================================================
# Inject Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'competitionInjectAdd')
def competitionInjectAdd(auth, competition = None, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
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
def competitionInjectDel(auth, pkid = None):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelDel(Inject, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionInjectSet')
def competitionInjectSet(auth, pkid = None, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelSet(Inject, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionInjectGet')
def competitionInjectGet(auth, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		return modelGet(Inject, **kwargs)
	except Exception as e:
		return handleException(e)

# ==================================================
# Inject Response Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'competitionInjectResponseAdd')
def competitionInjectResponseAdd(auth, competition = None, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
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
def competitionInjectResponseDel(auth, pkid = None):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelDel(InjectResponse, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionInjectResponseSet')
def competitionInjectResponseSet(auth, pkid = None, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelSet(InjectResponse, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionInjectResponseGet')
def competitionInjectResponseGet(auth, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		return modelGet(InjectResponse, **kwargs)
	except Exception as e:
		return handleException(e)

# ==================================================
# Incident Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'competitionIncidentAdd')
def competitionIncidentAdd(auth, competition = None, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
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
def competitionIncidentDel(auth, pkid = None):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelDel(Incident, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionIncidentSet')
def competitionIncidentSet(auth, pkid = None, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelSet(Incident, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionIncidentGet')
def competitionIncidentGet(auth, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		return modelGet(Incident, **kwargs)
	except Exception as e:
		return handleException(e)

# ==================================================
# Incident Response Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'competitionIncidentResponseAdd')
def competitionIncidentResponseAdd(auth, competition = None, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
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
def competitionIncidentResponseDel(auth, pkid = None):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelDel(IncidentResponse, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionIncidentResponseSet')
def competitionIncidentResponseSet(auth, pkid = None, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelSet(IncidentResponse, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionIncidentResponseGet')
def compeititonIncidentResponseGet(auth, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		return modelGet(IncidentResponse, **kwargs)
	except Exception as e:
		return handleException(e)


# ==================================================
# Scoring Engine Endpoints
# ==================================================
@CssefCeleryApp.task(name = 'competitionScoringEngineAdd')
def competitionScoringEngineAdd(auth, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		db = databaseConnection(dbPath)
		scoringEngine = ScoringEngine.fromDict(db, kwargs)
		returnDict = getEmptyReturnDict()
		returnDict['content'].append(scoringEngine.asDict())
		return returnDict
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionScoringEngineDel')
def competitionScoringEngineDel(auth, pkid = None):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelDel(ScoringEngine, pkid)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionScoringEngineSet')
def competitionScoringEngineSet(auth, pkid = None, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		if not pkid:
			raise Exception
		return modelSet(ScoringEngine, pkid, **kwargs)
	except Exception as e:
		return handleException(e)

@CssefCeleryApp.task(name = 'competitionScoringEngineGet')
def competitionScoringEngineGet(auth, **kwargs):
	authResult = authorizeAccess(auth)
	if authResult is not None:
		return authResult
	try:
		return modelGet(ScoringEngine, **kwargs)
	except Exception as e:
		return handleException(e)


endpointsDict = {
	"name": "Competition",
	"author": "",
	"menuName": "competition",
	"endpoints": [
		# Scoring Engine Endpoints
		{	"name": "Add Scoring Engine",
			"celeryName": "competitionScoringEngineAdd",
			"menu": ["engine", "add"],
			"arguments": []
		},
		{	"name": "Del Scoring Engine",
			"celeryName": "competitionScoringEngineDel",
			"menu": ["engine", "del"],
			"arguments": []
		},
		{	"name": "Set Scoring Engine",
			"celeryName": "competitionScoringEngineSet",
			"menu": ["engine", "set"],
			"arguments": []
		},
		{	"name": "Get Scoring Engine",
			"celeryName": "competitionScoringEngineGet",
			"menu": ["engine", "get"],
			"arguments": []
		},
		# Competition Endpoints
		{	"name": "Add Competition",
			"celeryName": "competitionAdd",
			"menu": ["add"],
			"arguments": [
				{	"name": "Organization",
					"argument": "organization",
					"keyword": True,
					"optional": False
				},
				{	"name": "Name",
					"argument": "name",
					"keyword": True,
					"optional": False
				},
				{	"name": "URL",
					"argument": "url",
					"keyword": True,
					"optional": True
				},
				{	"name": "Description",
					"argument": "description",
					"keyword": True,
					"optional": True
				},
				{	"name": "Datetime Display",
					"argument": "datetimeDisplay",
					"keyword": True,
					"optional": True
				},
				{	"name": "Datetime Start",
					"argument": "datetimeStart",
					"keyword": True,
					"optional": True
				},
				{	"name": "Datetime Finish",
					"argument": "datetimeFinish",
					"keyword": True,
					"optional": True
				},
				{	"name": "Auto-Start",
					"argument": "autoStart",
					"keyword": True,
					"optional": True
				}
			]
		},
		{	"name": "Delete Competition",
			"celeryName": "competitionDel",
			"menu": ["del"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": False
				}
			]
		},
		{	"name": "Set Competition",
			"celeryName": "competitionSet",
			"menu": ["set"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": False
				},
				{	"name": "Name",
					"argument": "name",
					"keyword": True,
					"optional": True
				},
				{	"name": "URL",
					"argument": "url",
					"keyword": True,
					"optional": True
				},
				{	"name": "Description",
					"argument": "description",
					"keyword": True,
					"optional": True
				},
				{	"name": "Datetime Display",
					"argument": "datetimeDisplay",
					"keyword": True,
					"optional": True
				},
				{	"name": "Datetime Start",
					"argument": "datetimeStart",
					"keyword": True,
					"optional": True
				},
				{	"name": "Datetime Finish",
					"argument": "datetimeFinish",
					"keyword": True,
					"optional": True
				},
				{	"name": "Auto-Start",
					"argument": "autoStart",
					"keyword": True,
					"optional": True
				}
			]
		},
		{	"name": "Get Competition",
			"celeryName": "competitionGet",
			"menu": ["get"],
			"arguments": [
				{	"name": "Organization",
					"argument": "organization",
					"keyword": True,
					"optional": False,
				},
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": False,
				},
				{	"name": "Name",
					"argument": "name",
					"keyword": True,
					"optional": False
				},
				{	"name": "URL",
					"argument": "url",
					"keyword": True,
					"optional": True
				},
				{	"name": "Description",
					"argument": "description",
					"keyword": True,
					"optional": True
				},
				{	"name": "Datetime Display",
					"argument": "datetimeDisplay",
					"keyword": True,
					"optional": True
				},
				{	"name": "Datetime Start",
					"argument": "datetimeStart",
					"keyword": True,
					"optional": True
				},
				{	"name": "Datetime Finish",
					"argument": "datetimeFinish",
					"keyword": True,
					"optional": True
				},
				{	"name": "Auto-Start",
					"argument": "autoStart",
					"keyword": True,
					"optional": True
				}
			]
		},
		# Team Endpoints
		{	"name": "Add Team",
			"celeryName": "competitionTeamAdd",
			"menu": ["team", "add"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": True
				},
				{	"name": "Name",
					"argument": "name",
					"keyword": True,
					"optional": False
				},
				{	"name": "Username",
					"argument": "username",
					"keyword": True,
					"optional": False
				},
				{	"name": "Password",
					"argument": "password",
					"keyword": True,
					"optional": False
				},
				{	"name": "Network CIDR",
					"argument": "networkCidr",
					"keyword": True,
					"optional": False
				}
			]
		},
		{	"name": "Delete Team",
			"celeryName": "competitionTeamDel",
			"menu": ["team", "del"],
			"arguments": [
				{	"name": "Team",
					"argument": "team",
					"keyword": True,
					"optional": False
				}
			]
		},
		{	"name": "Set Team",
			"celeryName": "competitionTeamSet",
			"menu": ["team", "set"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": True
				},
				{	"name": "Name",
					"argument": "name",
					"keyword": True,
					"optional": True
				},
				{	"name": "Username",
					"argument": "username",
					"keyword": True,
					"optional": True
				},
				{	"name": "Password",
					"argument": "password",
					"keyword": True,
					"optional": True
				},
				{	"name": "Network CIDR",
					"argument": "networkCidr",
					"keyword": True,
					"optional": True
				}
			]
		},
		{	"name": "Get Team",
			"celeryName": "competitionTeamGet",
			"menu": ["team", "get"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": True
				},
				{	"name": "Name",
					"argument": "name",
					"keyword": True,
					"optional": True
				},
				{	"name": "Username",
					"argument": "username",
					"keyword": True,
					"optional": True
				},
				{	"name": "Network CIDR",
					"argument": "networkCidr",
					"keyword": True,
					"optional": True
				}
			]
		},
		# Score Endpoints
		{	"name": "Add Score",
			"celeryName": "competitionScoreAdd",
			"menu": ["score", "add"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": False
				},
				{	"name": "Team",
					"argument": "team",
					"keyword": True,
					"optional": False
				},
				{	"name": "Datetime",
					"argument": "datetime",
					"keyword": True,
					"optional": False
				},
				{	"name": "Value",
					"argument": "value",
					"keyword": True,
					"optional": False
				},
				{	"name": "Message",
					"argument": "message",
					"keyword": True,
					"optional": True
				}
			]
		},
		{	"name": "Delete Score",
			"celeryName": "competitionScoreDel",
			"menu": ["score", "del"],
			"arguments": [
				{	"name": "Score",
					"argument": "score",
					"keyword": True,
					"optional": False
				}
			]
		},
		{	"name": "Set Score",
			"celeryName": "competitionScoreSet",
			"menu": ["score", "set"],
			"arguments": [
				{	"name": "Score",
					"argument": "Score",
					"keyword": True,
					"optional": False
				},
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": False
				},
				{	"name": "Team",
					"argument": "team",
					"keyword": True,
					"optional": True
				},
				{	"name": "Datetime",
					"argument": "datetime",
					"keyword": True,
					"optional": True
				},
				{	"name": "Value",
					"argument": "value",
					"keyword": True,
					"optional": True
				},
				{	"name": "Message",
					"argument": "message",
					"keyword": True,
					"optional": True
				}
			]
		},
		{	"name": "Get Score",
			"celeryName": "competitionScoreGet",
			"menu": ["score", "get"],
			"arguments": [
				{	"name": "Score",
					"argument": "Score",
					"keyword": True,
					"optional": True
				},
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": True
				},
				{	"name": "Team",
					"argument": "team",
					"keyword": True,
					"optional": True
				},
				{	"name": "Datetime",
					"argument": "datetime",
					"keyword": True,
					"optional": True
				},
				{	"name": "Value",
					"argument": "value",
					"keyword": True,
					"optional": True
				},
				{	"name": "Message",
					"argument": "message",
					"keyword": True,
					"optional": True
				}
			]
		},
		# Inject Endpoints
		{	"name": "Add Inject",
			"celeryName": "competitionInjectAdd",
			"menu": ["inject", "add"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": False
				},
				{	"name": "Require Response",
					"argument": "requireResponse",
					"keyword": True,
					"optional": False
				},
				{	"name": "Manual Delivery",
					"argument": "manualDelivery",
					"keyword": True,
					"optional": True
				},
				{	"name": "Datetime Delivery",
					"argument": "datetimeDelivery",
					"keyword": True,
					"optional": True
				},
				{	"name": "Datetime Response Due",
					"argument": "datetimeResponseDue",
					"keyword": True,
					"optional": True
				},
				{	"name": "Datetime Response Close",
					"argument": "datetimeResponseClose",
					"keyword": True,
					"optional": True
				},
				{	"name": "Title",
					"argument": "title",
					"keyword": True,
					"optional": False
				},
				{	"name": "Body",
					"argument": "body",
					"keyword": True,
					"optional": False
				}
			]
		},
		{	"name": "Delete Inject",
			"celeryName": "competitionInjectDel",
			"menu": ["inject", "del"],
			"arguments": [
				{	"name": "Inject",
					"argument": "Inject",
					"keyword": True,
					"optional": False
				}
			]
		},
		{	"name": "Set Inject",
			"celeryName": "competitionInjectSet",
			"menu": ["inject", "set"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": False
				},
				{	"name": "Require Response",
					"argument": "requireResponse",
					"keyword": True,
					"optional": False
				},
				{	"name": "Manual Delivery",
					"argument": "manualDelivery",
					"keyword": True,
					"optional": False
				},
				{	"name": "Datetime Delivery",
					"argument": "datetimeDelivery",
					"keyword": True,
					"optional": False
				},
				{	"name": "Datetime Response Due",
					"argument": "datetimeResponseDue",
					"keyword": True,
					"optional": False
				},
				{	"name": "Datetime Response Close",
					"argument": "datetimeResponseClose",
					"keyword": True,
					"optional": False
				},
				{	"name": "Title",
					"argument": "title",
					"keyword": True,
					"optional": False
				},
				{	"name": "Body",
					"argument": "body",
					"keyword": True,
					"optional": False
				}
			]
		},
		{	"name": "Get Inject",
			"celeryName": "competitionInjectGet",
			"menu": ["inject", "get"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": False
				},
				{	"name": "Require Response",
					"argument": "requireResponse",
					"keyword": True,
					"optional": False
				},
				{	"name": "Manual Delivery",
					"argument": "manualDelivery",
					"keyword": True,
					"optional": False
				},
				{	"name": "Datetime Delivery",
					"argument": "datetimeDelivery",
					"keyword": True,
					"optional": False
				},
				{	"name": "Datetime Response Due",
					"argument": "datetimeResponseDue",
					"keyword": True,
					"optional": False
				},
				{	"name": "Datetime Response Close",
					"argument": "datetimeResponseClose",
					"keyword": True,
					"optional": False
				},
				{	"name": "Title",
					"argument": "title",
					"keyword": True,
					"optional": False
				},
				{	"name": "Body",
					"argument": "body",
					"keyword": True,
					"optional": False
				}
			]
		},
		# Inject Response Endpoints
		{	"name": "Add Inject Response",
			"celeryName": "competitionTInjectResponsedd",
			"menu": ["injectresponse", "add"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": False
				},
				{	"name": "Team",
					"argument": "team",
					"keyword": True,
					"optional": False
				},
				{	"name": "Inject",
					"argument": "Inject",
					"keyword": True,
					"optional": False
				},
				{	"name": "Datetime",
					"argument": "datetime",
					"keyword": True,
					"optional": False
				},
				{	"name": "Content",
					"argument": "content",
					"keyword": True,
					"optional": False
				}
			]
		},
		{	"name": "Delete Inject Response",
			"celeryName": "competitionInjectResponseDel",
			"menu": ["injectresponse", "del"],
			"arguments": [
				{	"name": "Inject Response",
					"argument": "injectResponse",
					"keyword": True,
					"optional": False
				}
			]
		},
		{	"name": "Set Inject Response",
			"celeryName": "competitionInjectResponseSet",
			"menu": ["injectresponse", "set"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Team",
					"argument": "team",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Inject",
					"argument": "Inject",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Datetime",
					"argument": "datetime",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Content",
					"argument": "content",
					"keyword": True,
					"optional": True,
				}
			]
		},
		{	"name": "Get Inject Response",
			"celeryName": "competitionInjectResponseGet",
			"menu": ["injectresponse", "get"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Team",
					"argument": "team",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Inject",
					"argument": "Inject",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Datetime",
					"argument": "datetime",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Content",
					"argument": "content",
					"keyword": True,
					"optional": True,
				}
			]
		},
		# Incident Endpoints
		{	"name": "Add Incident",
			"celeryName": "competitionIncidentAdd",
			"menu": ["incident", "add"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": False,
				},
				{	"name": "Team",
					"argument": "team",
					"keyword": True,
					"optional": False,
				},
				{	"name": "Datetime",
					"argument": "datetime",
					"keyword": True,
					"optional": False,
				},
				{	"name": "Subject",
					"argument": "subject",
					"keyword": True,
					"optional": False,
				},
				{	"name": "Content",
					"argument": "content",
					"keyword": True,
					"optional": False,
				}
			]
		},
		{	"name": "Delete Incident",
			"celeryName": "competitionIncidentDel",
			"menu": ["incident", "del"],
			"arguments": [
				{	"name": "Incident",
					"argument": "incident",
					"keyword": True,
					"optional": False,
				}
			]
		},
		{	"name": "Set Incident",
			"celeryName": "competitionIncidentSet",
			"menu": ["incident", "set"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": False,
				},
				{	"name": "Team",
					"argument": "team",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Datetime",
					"argument": "datetime",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Subject",
					"argument": "subject",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Content",
					"argument": "content",
					"keyword": True,
					"optional": True,
				}
			]
		},
		{	"name": "Get Incident",
			"celeryName": "competitionIncidentGet",
			"menu": ["incident", "get"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": False,
				},
				{	"name": "Team",
					"argument": "team",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Datetime",
					"argument": "datetime",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Subject",
					"argument": "subject",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Content",
					"argument": "content",
					"keyword": True,
					"optional": True,
				}
			]
		},
		# Incident Response Endpoints
		{	"name": "Add Incident Response",
			"celeryName": "competitionIncidentResponseAdd",
			"menu": ["incidentresponse", "add"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": False,
				},
				{	"name": "Team",
					"argument": "team",
					"keyword": True,
					"optional": False,
				},
				{	"name": "Incident",
					"argument": "incident",
					"keyword": True,
					"optional": False,
				},
				{	"name": "Reply To",
					"argument": "replyTo",
					"keyword": True,
					"optional": False,
				},
				{	"name": "Datetime",
					"argument": "datetime",
					"keyword": True,
					"optional": False,
				},
				{	"name": "Subject",
					"argument": "subject",
					"keyword": True,
					"optional": False,
				},
				{	"name": "Content",
					"argument": "content",
					"keyword": True,
					"optional": False,
				}
			]
		},
		{	"name": "Delete Incident Response",
			"celeryName": "competitionIncidentResponseDel",
			"menu": ["incidentresponse", "del"],
			"arguments": [
				{	"name": "Incident Response",
					"argument": "incidentResponse",
					"keyword": True,
					"optional": False,
				}
			]
		},
		{	"name": "Set Incident Response",
			"celeryName": "competitionIncidentResponseSet",
			"menu": ["incidentresponse", "set"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": False,
				},
				{	"name": "Team",
					"argument": "team",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Incident",
					"argument": "incident",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Reply To",
					"argument": "replyTo",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Datetime",
					"argument": "datetime",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Subject",
					"argument": "subject",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Content",
					"argument": "content",
					"keyword": True,
					"optional": True,
				}
			]
		},
		{	"name": "Get Incident Response",
			"celeryName": "competitionIncidentResponseGet",
			"menu": ["incidentresponse", "get"],
			"arguments": [
				{	"name": "Competition",
					"argument": "competition",
					"keyword": True,
					"optional": False,
				},
				{	"name": "Team",
					"argument": "team",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Incident",
					"argument": "incident",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Reply To",
					"argument": "replyTo",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Datetime",
					"argument": "datetime",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Subject",
					"argument": "subject",
					"keyword": True,
					"optional": True,
				},
				{	"name": "Content",
					"argument": "content",
					"keyword": True,
					"optional": True,
				}
			]
		}
	]
}