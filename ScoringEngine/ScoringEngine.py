from models import Competition
from models import Team
from models import Score
from models import Service
from models import Inject
from models import InjectResponse
from models import IncidentResponse
from models import Plugin
from models import User
from models import Organization
#from django.core.exceptions import DoesNotExist

import json

def formatOutput(modelList, asJson):
	if asJson:
		return toJson(modelList)
	return modelList

def toJson(modelList):
	returnData = []
	for i in modelList:
		# consider replacing the follwing line with some form of
		# jsonpickler or custom JSON serilaizer
		returnData.append(i.asDict())
	return json.JSONEncoder().encode(returnData)

def getCompetitions(asJson=False):
	competitions = Competition.objects.all()
	return formatOutput(competitions, asJson)

def getCompetition(competitionId, asJson=False):
	try:
		competition = Competition.objects.get(competitionId = competitionId)
	except Competition.DoesNotExist:
		competition = []
	return formatOutput(competition, asJson)

def getTeams(competitionId, asJson=False):
	teams = Team.objects.filter(competitionId = competitionId)
	return formatOutput(teams, asJson)

def getTeam(competitionId, teamId, asJson=False):
	try:
		team = Team.objects.get(competitionId = competitionId, teamId = teamId)
	except Team.DoesNotExist:
		team = []
	return formatOutput(team, asJson)

def getServices(competitionId, asJson=False):
	services = Service.objects.filter(competitionId = competitionId)
	return formatOutput(services, asJson)

def getService(competitionId, serviceId, asJson=False):
	try:
		service = Service.objects.get(competitionId = competitionId, serviceId = serviceId)
	except Service.DoesNotExist:
		service = []
	return formatOutput(service, asJson)

def getScores(competitionId, asJson=False):
	scores = Score.objects.filter(competitionId = competitionId)
	return formatOutput(scores, asJson)

def getScore(competitionId, scoreId, asJson=False):
	try:
		score = Score.objects.get(competitionId = competitionId)
	except Score.DoesNotExist:
		score = []
	return formatOutput(score, asJson)

def getInjects(competitionId, asJson=False):
	injects = Inject.objects.filter(competitionId = competitionId)
	return formatOutput(injects, asJson)

def getInject(competitionId, injectId, asJson=False):
	try:
		inject = Inject.objects.get(competitionId = competitionId, injectId = injectId)
	except Inject.DoesNotExist:
		inject = []
	return formatOutput(inject, asJson)

def getInjectResponses(competitionId, asJson=False):
	injectResponses = InjectResponse.objects.filter(competitionId = competitionId)
	return formatOutput(injectResponses, asJson)

def getInjectResponse(competitionId, injectResponseId, asJson=False):
	try:
		injectResponse = InjectResponse.objects.get(competitionId = competitionId, injectResponseId = injectResponseId)
	except InjectResponse.DoesNotExist:
		injectResponse = []
	return formatOutput(injectResponse, asJson)

def getIncidentResponses(competitionId, asJson=False):
	incidentResponses = IncidentResponse.objects.filter(competitionId = competitionId)
	return formatOutput(incidentResponses, asJson)

def getIncidentResponse(competitionId, incidentResponseId, asJson=False):
	incidentResponse = IncidentResponse.objects.filter(competitionId = competitionId, incidentResponseId = incidentResponseId)
	return formatOutput(incidentResponse, asJson)

def getPlugins(asJson=False):
	plugins = Plugin.objects.all()
	return formatOutput(plugins, asJson)

def getPlugin(pluginId, asJson=False):
	try:
		plugin = Plugin.objects.get(pluginId = pluginId)
	except Plugin.DoesNotExist:
		plugin = []
	return formatOutput(plugin, asJson)

def getUsers(asJson=False):
	users = User.objects.all()
	return formatOutput(users, asJson)

def getUser(userId, asJson=False):
	try:
		user = User.objects.get(userId = userId)
	except User.DoesNotExist:
		user = []
	return formatOutput(user, asJson)

def getOrganizations(asJson=False):
	organizations = Organization.objects.all()
	return formatOutput(organizations, asJson)

def getOrganization(organizationId, asJson=False):
	organization = Organization.objects.filter(organizationId = organizationId)
	return formatOutput(organization, asJson)