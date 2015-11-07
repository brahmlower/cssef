from cssefd import celeryApp
from framework.core import Organization

@celeryApp.task
def competitionAdd(organization = None, name = None, **kwargs):
	organizationObj = Organization(pkid = organization)
	competitionObj = org.createCompetition(name = name, **kwargs)
	return competition

@celeryApp.task
def competitionDel(competition = None):
	competitionObj = getCompetition(competition = competition)
	competitionObj.delete()

@celeryApp.task
def competitionSet(competition = None, **kwargs):
	competitionObj = getCompetition(competition = competition)
	competitionObj.edit(**kwargs)

@celeryApp.task
def competitionGet():
	pass

@celeryApp.task
def competitionTeamAdd(competition = None, **kwargs):
	competitionObj = getCompetition(competition = competition)
	team = competitionObj.createTeam(**kwargs)
	return team

@celeryApp.task
def competitionTeamDel():
	pass

@celeryApp.task
def competitionTeamSet():
	pass

@celeryApp.task
def competitionTeamGet():
	pass

@celeryApp.task
def competitionInjectAdd(competition = None, **kwargs):
	competitionObj = getCompetition(competition = competition)
	inject = competitionObj.createInject(**kwargs)
	return inject

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