from django.http import HttpResponse
from rest_framework import status
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from ScoringEngine import ScoringEngine
from ScoringEngine.serializers import CompetitionSerializer
from ScoringEngine.serializers import TeamSerializer
from ScoringEngine.serializers import PluginSerializer
from ScoringEngine.serializers import ServiceSerializer
from ScoringEngine.serializers import ScoreSerializer
from ScoringEngine.serializers import InjectSerializer
from ScoringEngine.serializers import UserSerializer
from ScoringEngine.serializers import InjectResponseSerializer
from ScoringEngine.serializers import IncidentResponseSerializer
from ScoringEngine.serializers import DocumentSerializer    # TODO: Not sure if necessary
from ScoringEngine.serializers import OrganizationSerializer
from ScoringEngine.models import Competition
from ScoringEngine.models import Team
from ScoringEngine.models import Plugin
from ScoringEngine.models import Service
from ScoringEngine.models import Score
from ScoringEngine.models import Inject
from ScoringEngine.models import User
from ScoringEngine.models import InjectResponse
from ScoringEngine.models import IncidentResponse
from ScoringEngine.models import Document   # TODO: Not sure if necessary
from ScoringEngine.models import Organization

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def listObject(objectType, objectTypeSerializer, **kwargs):
    objectInstance = objectType.objects.get(**kwargs)
    serializer = objectTypeSerializer(objectInstance)
    return JSONResponse(serializer.data)

def listObjects(objectType, objectTypeSerializer):
    objects = objectType.objects.all()
    serializer = objectTypeSerializer(objects, many=True)
    return JSONResponse(serializer.data)

def postObject(request, objectTypeSerializer, objectInstance=None):
    if not objectInstance:
        serializer = objectTypeSerializer(data = request.POST)
    else:
        serializer = objectTypeSerializer(objectInstance, data = request.POST)
    if serializer.is_valid():
        serializer.save()
        return JSONResponse(serializer.data, status = HTTP_201_CREATED)
    return JSONResponse(serializer.errors, status = HTTP_400_BAD_REQUEST)

@csrf_exempt
def competitions(request):
    if request.method == 'GET':
        return listObjects(Competition, CompetitionSerializer)
    elif request.method == 'POST':
        return postObject(request, CompetitionSerializer)
    else:
        return Response(status = HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST', 'DELETE'])
def competition(request, competitionId):
    try:
        Competition.objects.get(competitionId = competitionId)
    except Competition.DoesNotExist:
        return Response(status = HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        return listObject(Competition, CompetitionSerializer, competitionId = competitionId)
    elif request.method == 'POST':
        competition = Competition.objects.get(competitionId = competitionId)
        return postObject(request, CompetitionSerializer, competition)
    elif request.method == 'DELETE':
        Competition.objects.get(competitionId = competitionId).delete()
        return Response(status = HTTP_204_NO_CONTENT)

@csrf_exempt
def teams(request, competitionId):
    if request.method == 'GET':
        return listObjects(Team, TeamSerializer)
    elif request.method == 'POST':
        return postObject(request, TeamSerializer)
    else:
        return Response(status = status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST', 'DELETE'])
def team(request, competitionId, teamId):
    try:
        Team.objects.get(teamId = teamId)
    except Team.DoesNotExist:
        return Response(status = HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        return listObject(Team, TeamSerializer, teamId = teamId)
    elif request.method == 'POST':
        team = Team.objects.get(teamId = teamId)
        return postObject(request, TeamSerializer, team)
    elif request.method == 'DELETE':
        Team.objects.get(teamId = teamId).delete()
        return Response(status = HTTP_204_NO_CONTENT)

@csrf_exempt
def services(request, competitionId):
    if request.method == 'GET':
        return listObjects(Service, ServiceSerializer)
    elif request.method == 'POST':
        return postObject(request, ServiceSerializer)
    else:
        return Response(status = HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST', 'DELETE'])
def service(request, competitionId, serviceId):
    try:
        Service.objects.get(serviceId = serviceId)
    except Service.DoesNotExist:
        return Response(status = HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        return listObject(Service, ServiceSerializer, serviceId = serviceId)
    elif request.method == 'POST':
        service = Service.objects.get(serviceId = serviceId)
        return postObject(request, ServiceSerializer, service)
    elif request.method == 'DELETE':
        Service.objects.get(serviceId = serviceId).delete()
        return Response(status = HTTP_204_NO_CONTENT)

@csrf_exempt
def scores(request, competitionId):
    if request.method == 'GET':
        return listObjects(Score, ScoreSerializer)
    elif request.method == 'POST':
        return postObject(request, ScoreSerializer)
    else:
        return Response(status = HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST', 'DELETE'])
def score(request, competitionId, scoreId):
    try:
        Score.objects.get(scoreId = scoreId)
    except Score.DoesNotExist:
        return Response(status = HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        return listObject(Score, ScoreSerializer, scoreId = scoreId)
    elif request.method == 'POST':
        score = Score.objects.get(scoreId = scoreId)
        return postObject(request, ScoreSerializer, score)
    elif request.method == 'DELETE':
        Score.objects.get(scoreId = scoreId).delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

@csrf_exempt
def injects(request, competitionId=None, injectId=None):
    if request.method == 'GET':
        return listObjects(Inject, InjectSerializer)
    elif request.method == 'POST':
        return postObject(request, InjectSerializer)
    else:
        return Response(status = HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST', 'DELETE'])
def inject(request, competitionId, injectId):
    try:
        Inject.objects.get(injectId = injectId)
    except Inject.DoesNotExist:
        return Response(status = HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        return listObject(Inject, InjectSerializer, injectId = injectId)
    elif request.method == 'POST':
        inject = Inject.objects.get(injectId = injectId)
        return postObject(request, InjectSerializer, inject)
    elif request.method == 'DELETE':
        Inject.objects.get(injectId = injectId).delete()
        return Response(status = HTTP_204_NO_CONTENT)

@csrf_exempt
def injectresponses(request, competitionId):
    if request.method == 'GET':
        return listObjects(InjectResponse, InjectResponseSerializer)
    elif request.method == 'POST':
        return postObject(request, InjectResponseSerializer)
    else:
        return Response(status = HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST', 'DELETE'])
def injectresponse(request, competitionId, injectResponseId):
    try:
        InjectResponse.objects.get(injectResponseId = injectResponseId)
    except InjectResponse.DoesNotExist:
        return Response(status = HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        return listObject(InjectResponse, InjectResponseSerializer, injectResponseId = injectResponseId)
    elif request.method == 'POST':
        injectresponse = InjectResponse.objects.get(injectResponseId = injectResponseId)
        return postObject(request, InjectResponseSerializer, injectresponse)
    elif request.method == 'DELETE':
        InjectResponse.objects.get(injectResponseId = injectResponseId).delete()
        return Response(status = HTTP_204_NO_CONTENT)

@csrf_exempt
def incidentresponses(request, competitionId):
    if request.method == 'GET':
        return listObjects(IncidentResponse, IncidentResponseSerializer)
    elif request.method == 'POST':
        return postObject(request, IncidentResponseSerializer)
    else:
        return Response(status = HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST', 'DELETE'])
def incidentresponse(request, competitionId, incidentResponseId):
    try:
        IncidentResponse.objects.get(incidentResponseId = incidentResponseId)
    except IncidentResponse.DoesNotExist:
        return Response(status = HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        return listObject(IncidentResponse, IncidentResponseSerializer, incidentResponseId = incidentResponseId)
    elif request.method == 'POST':
        incidentresponse = IncidentResponse.objects.get(incidentResponseId = incidentResponseId)
        return postObject(request, IncidentResponseSerializer, incidentresponse)
    elif request.method == 'DELETE':
        IncidentResponse.objects.get(incidentResponseId = incidentResponseId).delete()
        return Response(status = HTTP_204_NO_CONTENT)

@csrf_exempt
def plugins(request):
    if request.method == 'GET':
        return listObjects(Plugin, PluginSerializer)
    elif request.method == 'POST':
        return postObject(request, PluginSerializer)
    else:
        return Response(status = HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST', 'DELETE'])
def plugin(request, pluginId):
    try:
        Plugin.objects.get(pluginId = pluginId)
    except Plugin.DoesNotExist:
        return Response(status = HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        return listObject(Plugin, PluginSerializer, pluginId = pluginId)
    elif request.method == 'POST':
        plugin = Plugin.objects.get(pluginId = pluginId)
        return postObject(request, PluginSerializer, plugin)
    elif request.method == 'DELETE':
        Plugin.objects.get(pluginId = pluginId).delete()
        return Response(status = HTTP_204_NO_CONTENT)

@csrf_exempt
def users(request):
    if request.method == 'GET':
        return listObjects(User, UserSerializer)
    elif request.method == 'POST':
        return postObject(request, UserSerializer)
    else:
        return Response(status = HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST', 'DELETE'])
def user(request, userId):
    try:
        User.objects.get(userId = userId)
    except User.DoesNotExist:
        return Response(status = HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        return listObject(User, UserSerializer, userId = userId)
    elif request.method == 'POST':
        user = User.objects.get(userId = userId)
        return postObject(request, UserSerializer, user)
    elif request.method == 'DELETE':
        User.objects.get(userId = userId).delete()
        return Response(status = HTTP_204_NO_CONTENT)

@csrf_exempt
def organizations(request):
    if request.method == 'GET':
        return listObjects(Organization, OrganizationSerializer)
    elif request.method == 'POST':
        return postObject(request, OrganizationSerializer)
    else:
        return Response(status = HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET', 'POST', 'DELETE'])
def organization(request, organizationId):
    try:
        Organization.objects.get(organizationId = organizationId)
    except Organization.DoesNotExist:
        return Response(status = HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        return listObject(Organization, OrganizationSerializer, organizationId = organizationId)
    elif request.method == 'POST':
        organization = Organization.objects.get(organizationId = organizationId)
        return postObject(request, OrganizationSerializer, organization)
    elif request.method == 'DELETE':
        Organization.objects.get(organizationId = organizationId).delete()
        return Response(status = HTTP_204_NO_CONTENT)