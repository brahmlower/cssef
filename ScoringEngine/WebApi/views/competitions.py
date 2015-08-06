from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from WebApi.views.utils import objectExists
from WebApi.views.utils import listObjects
from WebApi.views.utils import listObject
from WebApi.views.utils import postObject
from WebApi.views.utils import patchObject
from WebApi.views.utils import deleteObject

from ScoringEngine import Competition

@api_view(['GET', 'POST'])
def competitions(request):
	if request.method == 'GET':
		return listObjects(Competition, CompetitionSerializer)
	elif request.method == 'POST':
		return postObject(request, CompetitionSerializer)

@api_view(['GET', 'PATCH', 'DELETE'])
def competition(request, competitionId):
	if request.method == 'GET':
		return listObject(Competition, CompetitionSerializer, competitionId = competitionId)
	elif request.method == 'PATCH':
		return patchObject(request, Competition, CompetitionSerializer, competitionId = competitionId)
	elif request.method == 'DELETE':
		return deleteObject(Competition, competitionId = competitionId)

@api_view(['GET', 'POST'])
def teams(request, competitionId):
	competition = Competition(competitionId)
	if request.method == 'GET':
		return listObjects(competition, Competition.getTeams)
	elif request.method == 'POST':
		return postObject(competition, Competition.newTeam, request)

@api_view(['GET', 'PATCH', 'DELETE'])
def team(request, competitionId, teamId):
	competition = Competition(competitionId)
	if request.method == 'GET':
		return listObject(competition, Competition.getTeam, teamId = teamId)
	elif request.method == 'PATCH':
		return patchObject(competition, Competition.editTeam, request, teamId = teamId)
	elif request.method == 'DELETE':
		obj = competition.getTeam(teamId = teamId)
		return deleteObject(competition, Competition.deleteTeam, obj)

@api_view(['GET', 'POST'])
def services(request, competitionId):
	competition = Competition(competitionId)
	if request.method == 'GET':
		return listObjects(competition, Competition.getServices)
	elif request.method == 'POST':
		return postObject(competition, Competition.newService, request)

@api_view(['GET', 'PATCH', 'DELETE'])
def service(request, competitionId, serviceId):
	competition = Competition(competitionId)
	if request.method == 'GET':
		return listObject(competition, Competition.getService, serviceId = serviceId)
	elif request.method == 'PATCH':
		return patchObject(competition, Competition.editService, request, serviceId = serviceId)
	elif request.method == 'DELETE':
		obj = competition.getService(serviceId = serviceId)
		return deleteObject(competition, Competition.deleteService, obj)

@api_view(['GET', 'POST'])
def scores(request, competitionId):
	competition = Competition(competitionId)
	if request.method == 'GET':
		return listObjects(competition, Competition.getScores)
	elif request.method == 'POST':
		return postObject(competition, Competition.newScore, request)

@api_view(['GET', 'PATCH', 'DELETE'])
def score(request, competitionId, scoreId):
	competition = Competition(competitionId)
	if request.method == 'GET':
		return listObject(competition, Competition.getScore, scoreId = scoreId)
	elif request.method == 'PATCH':
		return patchObject(competition, Competition.editScore, request, scoreId = scoreId)
	elif request.method == 'DELETE':
		obj = competition.getScore(scoreId = scoreId)
		return deleteObject(competition, Competition.deleteScore, obj)

@api_view(['GET', 'POST'])
def injects(request, competitionId=None, injectId=None):
	competition = Competition(competitionId)
	if request.method == 'GET':
		return listObjects(competition, Competition.getInjects)
	elif request.method == 'POST':
		return postObject(competition, Competition.newInject, request)

@api_view(['GET', 'PATCH', 'DELETE'])
def inject(request, competitionId, injectId):
	competition = Competition(competitionId)
	if request.method == 'GET':
		return listObject(competition, Competition.getInject, injectId = injectId)
	elif request.method == 'PATCH':
		return patchObject(competition, Competition.editInject, request, injectId = injectId)
	elif request.method == 'DELETE':
		obj = competition.getInject(injectId = injectId)
		return deleteObject(competition, Competition.deleteInject, obj)

@api_view(['GET', 'POST'])
def injectresponses(request, competitionId):
	competition = Competition(competitionId)
	if request.method == 'GET':
		return listObjects(competition, Competition.getInjectResponses)
	elif request.method == 'POST':
		return postObject(competition, Competition.newInjectResponse, request)

@api_view(['GET', 'PATCH', 'DELETE'])
def injectresponse(request, competitionId, injectResponseId):
	competition = Competition(competitionId)
	if request.method == 'GET':
		return listObject(competition, Competition.getInjectResponse, injectresponseId = injectresponseId)
	elif request.method == 'PATCH':
		return patchObject(competition, Competition.editInjectResponse, request, injectResponseId = injectResponseId)
	elif request.method == 'DELETE':
		obj = competition.getInjectResponse(injectresponseId = injectresponseId)
		return deleteObject(competition, Competition.deleteInjectResponse, obj)

@api_view(['GET', 'POST'])
def incidents(request, competitionId):
	competition = Competition(competitionId)
	if request.method == 'GET':
		return listObjects(competition, Competition.getIncidents)
	elif request.method == 'POST':
		return postObject(competition, Competition.newIncident, request)

@api_view(['GET', 'PATCH', 'DELETE'])
def incident(request, competitionId, incidentId):
	competition = Competition(competitionId)
	if request.method == 'GET':
		return listObject(competition, Competition.getIncident, incidentId = incidentId)
	elif request.method == 'PATCH':
		return patchObject(competition, Competition.editIncident, request, incidentId = incidentId)
	elif request.method == 'DELETE':
		obj = competition.getIncident(incidentId = incidentId)
		return deleteObject(competition, Competition.deleteIncident, obj)

@api_view(['GET', 'POST'])
def incidentresponses(request, competitionId):
	competition = Competition(competitionId)
	if request.method == 'GET':
		return listObjects(competition, Competition.getIncidentResponses)
	elif request.method == 'POST':
		return postObject(competition, Competition.newIncidentResponse, request)

@api_view(['GET', 'PATCH', 'DELETE'])
def incidentresponse(request, competitionId, incidentResponseId):
	competition = Competition(competitionId)
	if request.method == 'GET':
		return listObject(competition, Competition.getIncidentResponse, incidentResponseId = incidentResponseId)
	elif request.method == 'PATCH':
		return patchObject(competition, Competition.editIncidentResponse, request, incidentResponseId = incidentResponseId)
	elif request.method == 'DELETE':
		obj = competition.getIncidentResponse(incidentResponseId = incidentResponseId)
		return deleteObject(competition, Competition.deleteIncidentResponse, obj)