from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from ScoringEngine.serializers import CompetitionSerializer
from ScoringEngine.serializers import TeamSerializer
from ScoringEngine.serializers import PluginSerializer
from ScoringEngine.serializers import ServiceSerializer
from ScoringEngine.serializers import ScoreSerializer
from ScoringEngine.serializers import InjectSerializer
from ScoringEngine.serializers import UserSerializer
from ScoringEngine.serializers import InjectResponseSerializer
from ScoringEngine.serializers import IncidentResponseSerializer
from ScoringEngine.models import Competition
from ScoringEngine.models import Team
from ScoringEngine.models import Plugin
from ScoringEngine.models import Service
from ScoringEngine.models import Score
from ScoringEngine.models import Inject
from ScoringEngine.models import User
from ScoringEngine.models import InjectResponse
from ScoringEngine.models import IncidentResponse

from WebApi.views.utils import objectExists
from WebApi.views.utils import listObjects
from WebApi.views.utils import listObject
from WebApi.views.utils import postObject
from WebApi.views.utils import patchObject
from WebApi.views.utils import deleteObject

@api_view(['GET', 'POST'])
def competitions(request):
	if request.method == 'GET':
		return listObjects(Competition, CompetitionSerializer)
	elif request.method == 'POST':
		return postObject(request, CompetitionSerializer)

@api_view(['GET', 'PATCH', 'DELETE'])
def competition(request, competitionId):
	if not objectExists(Competition, competitionId = competitionId):
		return Response(status = status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		return listObject(Competition, CompetitionSerializer, competitionId = competitionId)
	elif request.method == 'PATCH':
		return patchObject(request, Competition, CompetitionSerializer, competitionId = competitionId)
	elif request.method == 'DELETE':
		return deleteObject(Competition, competitionId = competitionId)

@api_view(['GET', 'POST'])
def teams(request, competitionId):
	if request.method == 'GET':
		return listObjects(Team, TeamSerializer)
	elif request.method == 'POST':
		return postObject(request, TeamSerializer)

@api_view(['GET', 'PATCH', 'DELETE'])
def team(request, competitionId, teamId):
	if not objectExists(Team, competitionId = competitionId, teamId = teamId):
		return Response(status = status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		return listObject(Team, TeamSerializer, teamId = teamId)
	elif request.method == 'PATCH':
		return patchObject(request, Team, TeamSerializer, teamId = teamId)
	elif request.method == 'DELETE':
		return deleteObject(Team, teamId = teamId)

@api_view(['GET', 'POST'])
def services(request, competitionId):
	if request.method == 'GET':
		return listObjects(Service, ServiceSerializer)
	elif request.method == 'POST':
		return postObject(request, ServiceSerializer)

@api_view(['GET', 'PATCH', 'DELETE'])
def service(request, competitionId, serviceId):
	if not objectExists(Service, competitionId = competitionId, serviceId = serviceId):
		return Response(status = status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		return listObject(Service, ServiceSerializer, serviceId = serviceId)
	elif request.method == 'PATCH':
		return patchObject(request, Service, ServiceSerializer, serviceId = serviceId)
	elif request.method == 'DELETE':
		return deleteObject(Service, serviceId = serviceId)

@api_view(['GET', 'POST'])
def scores(request, competitionId):
	if request.method == 'GET':
		return listObjects(Score, ScoreSerializer)
	elif request.method == 'POST':
		return postObject(request, ScoreSerializer)

@api_view(['GET', 'PATCH', 'DELETE'])
def score(request, competitionId, scoreId):
	if not objectExists(Score, competitionId = competitionId, scoreId = scoreId):
		return Response(status = status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		return listObject(Score, ScoreSerializer, scoreId = scoreId)
	elif request.method == 'PATCH':
		return patchObject(request, Score, ScoreSerializer, scoreId = scoreId)
	elif request.method == 'DELETE':
		return deleteObject(Score, scoreId = scoreId)

@api_view(['GET', 'POST'])
def injects(request, competitionId=None, injectId=None):
	if request.method == 'GET':
		return listObjects(Inject, InjectSerializer)
	elif request.method == 'POST':
		return postObject(request, InjectSerializer)

@api_view(['GET', 'PATCH', 'DELETE'])
def inject(request, competitionId, injectId):
	if not objectExists(Inject, competitionId = competitionId, injectId = injectId):
		return Response(status = status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		return listObject(Inject, InjectSerializer, injectId = injectId)
	elif request.method == 'PATCH':
		return patchObject(request, Inject, InjectSerializer, injectId = injectId)
	elif request.method == 'DELETE':
		return deleteObject(Inject, injectId = injectId)

@api_view(['GET', 'POST'])
def injectresponses(request, competitionId):
	if request.method == 'GET':
		return listObjects(InjectResponse, InjectResponseSerializer)
	elif request.method == 'POST':
		return postObject(request, InjectResponseSerializer)

@api_view(['GET', 'PATCH', 'DELETE'])
def injectresponse(request, competitionId, injectResponseId):
	if not objectExists(InjectResponse, competitionId = competitionId, injectResponseId = injectResponseId):
		return Response(status = status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		return listObject(InjectResponse, InjectResponseSerializer, injectResponseId = injectResponseId)
	elif request.method == 'PATCH':
		return patchObject(request, InjectResponse, InjectResponseSerializer, injectResponseId = injectResponseId)
	elif request.method == 'DELETE':
		return deleteObject(InjectResponse, injectResponseId = injectResponseId)

@api_view(['GET', 'POST'])
def incidentresponses(request, competitionId):
	if request.method == 'GET':
		return listObjects(IncidentResponse, IncidentResponseSerializer)
	elif request.method == 'POST':
		return postObject(request, IncidentResponseSerializer)

@api_view(['GET', 'PATCH', 'DELETE'])
def incidentresponse(request, competitionId, incidentResponseId):
	if not objectExists(IncidentResponse, competitionId = competitionId, incidentResponseId = incidentResponseId):
		return Response(status = status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		return listObject(IncidentResponse, IncidentResponseSerializer, incidentResponseId = incidentResponseId)
	elif request.method == 'PATCH':
		return patchObject(request, IncidentResponse, IncidentResponseSerializer, incidentResponseId = incidentResponseId)
	elif request.method == 'DELETE':
		return deleteObject(IncidentResponse, incidentResponseId = incidentResponseId)