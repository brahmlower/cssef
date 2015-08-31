from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from WebApi.views.utils import callObject
from WebApi.views.utils import listObjects
from WebApi.views.utils import listObject
from WebApi.views.utils import postObject
from WebApi.views.utils import patchObject
from WebApi.views.utils import deleteObject

from ScoringEngine import endpoints
from ScoringEngine.endpoints import Competition

@api_view(['GET'])
def competitions(request):
	if request.method == 'GET':
		return listObjects(endpoints, 'getCompetitions')

@api_view(['GET'])
def competition(request, competitionId):
	if request.method == 'GET':
		return listObject(endpoints, 'getCompetition', competitionId = competitionId)

@api_view(['GET', 'POST'])
def teams(request, competitionId):
	competition = Competition(competitionId = competitionId)
	if request.method == 'GET':
		return listObjects(competition, 'getTeams')
	elif request.method == 'POST':
		return postObject(competition, 'createTeam', request)

@api_view(['GET', 'PATCH', 'DELETE'])
def team(request, competitionId, teamId):
	competition = Competition(competitionId = competitionId)
	if request.method == 'GET':
		return callObject(competition, 'getTeam', content = True, teamId = teamId)
	elif request.method == 'PATCH':
		return patchObject(competition, 'editTeam', request, teamId = teamId)
	elif request.method == 'DELETE':
		return callObject(competition, 'deleteTeam', content = False, teamId = teamId)

@api_view(['GET', 'POST'])
def services(request, competitionId):
	competition = Competition(competitionId = competitionId)
	if request.method == 'GET':
		return listObjects(competition, 'getServices')
	elif request.method == 'POST':
		return postObject(competition, 'createService', request)

@api_view(['GET', 'PATCH', 'DELETE'])
def service(request, competitionId, serviceId):
	competition = Competition(competitionId = competitionId)
	if request.method == 'GET':
		return callObject(competition, 'getService', content = True, serviceId = serviceId)
	elif request.method == 'PATCH':
		return patchObject(competition, 'editService', request, serviceId = serviceId)
	elif request.method == 'DELETE':
		return callObject(competition, 'deleteService', content = False, serviceId = serviceId)

@api_view(['GET', 'POST'])
def scores(request, competitionId):
	competition = Competition(competitionId = competitionId)
	if request.method == 'GET':
		return listObjects(competition, 'getScores')
	elif request.method == 'POST':
		return postObject(competition, 'createScore', request)

@api_view(['GET', 'PATCH', 'DELETE'])
def score(request, competitionId, scoreId):
	competition = Competition(competitionId = competitionId)
	if request.method == 'GET':
		return callObject(competition, 'getScore', content = True, scoreId = scoreId)
	elif request.method == 'PATCH':
		return patchObject(competition, 'editScore', request, scoreId = scoreId)
	elif request.method == 'DELETE':
		return callObject(competition, 'deleteScore', content = False, scoreId = scoreId)

@api_view(['GET', 'POST'])
def injects(request, competitionId=None, injectId=None):
	competition = Competition(competitionId = competitionId)
	if request.method == 'GET':
		return listObjects(competition, 'getInjects')
	elif request.method == 'POST':
		return postObject(competition, 'createInject', request)

@api_view(['GET', 'PATCH', 'DELETE'])
def inject(request, competitionId, injectId):
	competition = Competition(competitionId = competitionId)
	if request.method == 'GET':
		return callObject(competition, 'getInject', content = True, injectId = injectId)
	elif request.method == 'PATCH':
		return patchObject(competition, 'editInject', request, injectId = injectId)
	elif request.method == 'DELETE':
		return callObject(competition, 'deleteInject', content = False, injectId = injectId)

@api_view(['GET', 'POST'])
def injectresponses(request, competitionId):
	competition = Competition(competitionId = competitionId)
	if request.method == 'GET':
		return listObjects(competition, 'getInjectResponses')
	elif request.method == 'POST':
		return postObject(competition, 'createInjectResponse', request)

@api_view(['GET', 'PATCH', 'DELETE'])
def injectresponse(request, competitionId, injectResponseId):
	competition = Competition(competitionId = competitionId)
	if request.method == 'GET':
		return callObject(competition, 'getInjectResponse', content = True, injectResponseId = injectResponseId)
	elif request.method == 'PATCH':
		return patchObject(competition, 'editInjectResponse', request, injectResponseId = injectResponseId)
	elif request.method == 'DELETE':
		return callObject(competition, 'deleteInjectResponse', content = False, injectResponseId = injectResponseId)

@api_view(['GET', 'POST'])
def incidents(request, competitionId):
	competition = Competition(competitionId = competitionId)
	if request.method == 'GET':
		return listObjects(competition, 'getIncidents')
	elif request.method == 'POST':
		return postObject(competition, 'createIncident', request)

@api_view(['GET', 'PATCH', 'DELETE'])
def incident(request, competitionId, incidentId):
	competition = Competition(competitionId = competitionId)
	if request.method == 'GET':
		return callObject(competition, 'getIncident', content = True, incidentId = incidentId)
	elif request.method == 'PATCH':
		return patchObject(competition, 'editIncident', request, incidentId = incidentId)
	elif request.method == 'DELETE':
		return callObject(competition, 'deleteIncident', content = False, incidentId = incidentId)

@api_view(['GET', 'POST'])
def incidentresponses(request, competitionId):
	competition = Competition(competitionId = competitionId)
	if request.method == 'GET':
		return listObjects(competition, 'getIncidentResponses')
	elif request.method == 'POST':
		return postObject(competition, 'createIncidentResponse', request)

@api_view(['GET', 'PATCH', 'DELETE'])
def incidentresponse(request, competitionId, incidentResponseId):
	competition = Competition(competitionId = competitionId)
	if request.method == 'GET':
		return callObject(competition, 'getIncidentResponse', content = True, incidentResponseId = incidentResponseId)
	elif request.method == 'PATCH':
		return patchObject(competition, 'editIncidentResponse', request, incidentResponseId = incidentResponseId)
	elif request.method == 'DELETE':
		return callObject(competition, 'deleteIncidentResponse', content = False, incidentResponseId = incidentResponseId)