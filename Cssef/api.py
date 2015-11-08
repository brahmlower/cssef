from cssefd import celeryApp
from framework.core import Organization

@celeryApp.task
def competitionAdd(organization = None, name = None, **kwargs):
	if not competition:
		pass
		# Raise some error
	organizationObj = Organization(pkid = organization)
	competitionObj = org.createCompetition(name = name, **kwargs)
	return competition

@celeryApp.task
def competitionDel(competition = None):
	if not competition:
		pass
		# Raise some error
	competitionObj = getCompetition(competition = competition)
	competitionObj.delete()

@celeryApp.task
def competitionSet(competition = None, **kwargs):
	if not competition:
		pass
		# Raise some error
	competitionObj = getCompetition(competition = competition)
	competitionObj.edit(**kwargs)

@celeryApp.task
def competitionGet():
	pass

@celeryApp.task
def competitionTeamAdd(competition = None, **kwargs):
	if not competition:
		pass
		# Raise some error
	competitionObj = getCompetition(competition = competition)
	teamObj = competitionObj.createTeam(**kwargs)
	return teamObj

@celeryApp.task
def competitionTeamDel(competition = None, Team = None):
	if not competition:
		pass
	teamObj = Team(competition = competition, team = team)
	teamObj.delete()

@celeryApp.task
def competitionTeamSet():
	pass

@celeryApp.task
def competitionTeamGet():
	pass

@celeryApp.task
def competitionInjectAdd(competition = None, **kwargs):
	if not competition:
		pass
		# Raise some error
	competitionObj = getCompetition(competition = competition)
	injectObj = competitionObj.createInject(**kwargs)
	return injectObj

@celeryApp.task
def competitionInjectDel():
	pass

@celeryApp.task
def competitionInjectSet():
	pass

@celeryApp.task
def competitionInjectGet():
	pass

@celeryApp.task
def competitionInjectResponseAdd(competition = None, **kwargs):
	if not competition:
		pass
		# Raise some error
	competitionObj = getCompetition(competition = competition)
	injectResponse = competitionObj.createInjectResponse(**kwargs)
	return injectResponse

@celeryApp.task
def competitionInjectResponseDel():
	pass

@celeryApp.task
def competitionInjectResponseSet():
	pass

@celeryApp.task
def competitionInjectResponseGet():
	pass

@celeryApp.task
def competitionIncidentAdd():
	pass

@celeryApp.task
def competitionIncidentDel():
	pass

@celeryApp.task
def competitionIncidentSet():
	pass

@celeryApp.task
def competitionIncidentGet():
	pass

@celeryApp.task
def competitionIncidentResponseAdd():
	pass

@celeryApp.task
def competitionIncidentResponseDel():
	pass

@celeryApp.task
def competitionIncidentResponseSet():
	pass

@celeryApp.task
def compeititonIncidentResponseGet():
	pass

@celeryApp.task
def organizationAdd():
	pass

@celeryApp.task
def organizationDel():
	pass

@celeryApp.task
def organizationSet():
	pass

@celeryApp.task
def organizationGet():
	pass

@celeryApp.task
def userAdd():
	pass

@celeryApp.task
def userDel():
	pass

@celeryApp.task
def userSet():
	pass

@celeryApp.task
def userGet():
	pass

@celeryApp.task
def documentAdd():
	pass

@celeryApp.task
def documentDel():
	pass

@celeryApp.task
def documentSet():
	pass

@celeryApp.task
def documentGet():
	pass

@celeryApp.task
def scoringengineAdd():
	pass

@celeryApp.task
def scoringengineDel():
	pass

@celeryApp.task
def scoringengineSet():
	pass

@celeryApp.task
def scoringengineGet():
	pass