from WebInterface.utils import getContext
from WebInterface.modules.competition.context import WhiteteamSummaryContext
from WebInterface.modules.competition.context import WhiteteamSettingsContext
from WebInterface.modules.competition.context import TeamListContext
from WebInterface.modules.competition.context import TeamEditContext
from WebInterface.modules.competition.context import TeamCreateContext
from WebInterface.modules.competition.context import InjectListContext
from WebInterface.modules.competition.context import InjectEditContext
from WebInterface.modules.competition.context import InjectCreateContext

templatePathPrefix = "competition/templates/whiteteam/"

def summary(request, competitionId):
	pageTemplate = templatePathPrefix + 'summary.html'
	return getContext(WhiteteamSummaryContext, pageTemplate, request, competitionId = competitionId)

def settings(request, competitionId):
	pageTemplate = templatePathPrefix + 'settings.html'
	return getContext(WhiteteamSettingsContext, pageTemplate, request, competitionId = competitionId)

# ==================================================
# Team Methods
# ==================================================
def listTeams(request, competitionId):
	pageTemplate = templatePathPrefix + 'listTeams.html'
	return getContext(TeamListContext, pageTemplate, request, competitionId = competitionId)

def createTeam(request, competitionId):
	pageTemplate = templatePathPrefix + 'createEditTeam.html'
	return getContext(TeamCreateContext, pageTemplate, request, competitionId = competitionId)

def editTeam(request, competitionId, teamId):
	pageTemplate = templatePathPrefix + 'createEditTeam.html'
	return getContext(TeamEditContext, pageTemplate, request, competitionId = competitionId, pkid = teamId)

# ==================================================
# Inject Methods
# ==================================================
def listInjects(request, competitionId):
	pageTemplate = templatePathPrefix + 'listInjects.html'
	return getContext(InjectListContext, pageTemplate, request, competitionId = competitionId)

def createInject(request, competitionId):
	pageTemplate = templatePathPrefix + 'createEditInject.html'
	return getContext(InjectCreateContext, pageTemplate, request, competitionId = competitionId)

def editInject(request, competitionId, injectId):
	pageTemplate = templatePathPrefix + 'createEditInject.html'
	return getContext(InjectEditContext, pageTemplate, request, competitionId = competitionId, pkid = injectId)