from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
#from ScoringEngine import ScoringEngine
from ScoringEngine.serializers import CompetitionSerializer
from ScoringEngine.serializers import TeamSerializer
from ScoringEngine.serializers import PluginSerializer
from ScoringEngine.serializers import ServiceSerializer
from ScoringEngine.serializers import ScoreSerializer
from ScoringEngine.serializers import InjectSerializer
from ScoringEngine.serializers import UserSerializer
from ScoringEngine.serializers import InjectResponseSerializer
from ScoringEngine.serializers import IncidentResponseSerializer
#from ScoringEngine.serializers import DocumentSerializer    # TODO: Not sure if necessary
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
from ScoringEngine import settings
from django.core.files.uploadedfile import UploadedFile
from hashlib import md5
from urllib import quote
import json

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def objectExists(objectType, **kwargs):
    try:
        objectType.objects.get(**kwargs)
        return True
    except objectType.DoesNotExist:
        return False

def listObject(objectType, objectTypeSerializer, **kwargs):
    objectInstance = objectType.objects.get(**kwargs)
    serializer = objectTypeSerializer(objectInstance)
    return JSONResponse(serializer.data)

def listObjects(objectType, objectTypeSerializer):
    objects = objectType.objects.all()
    serializer = objectTypeSerializer(objects, many = True)
    return JSONResponse(serializer.data)

def postObject(request, objectTypeSerializer):
    serializer = objectTypeSerializer(data = request.POST)
    if serializer.is_valid():
        serializerResult = serializer.save()
        if request.FILES:
            print request.FILES
            for i in request.FILES:
                saveDocument(request.FILES[i], serializerResult)
        return JSONResponse(serializer.data, status = status.HTTP_201_CREATED)
    print "Serializer object is not valid:"
    print serializer.errors
    return JSONResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

def patchObject(request, objectType, objectTypeSerializer, **kwargs):
    objectInstance = objectType.objects.get(**kwargs)
    serializer = objectTypeSerializer(objectInstance)
    data = serializer.data
    data.update(json.loads(request.body))
    serializer = objectTypeSerializer(objectInstance, data = data)
    if serializer.is_valid():
        serializer.save()
        return JSONResponse(serializer.data, status = status.HTTP_202_ACCEPTED)
    return JSONResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

def deleteObject(objectType, **kwargs):
    objectType.objects.get(**kwargs).delete()
    return Response(status = status.HTTP_204_NO_CONTENT)

def saveDocument(postedFile, relatedObject):
    uploadedFile = UploadedFile(postedFile)
    fileContent = uploadedFile.read()
    document = Document()
    document.fileHash = md5(fileContent).hexdigest()
    document.urlEncodedFilename = quote(uploadedFile.name)
    document.filename = uploadedFile.name
    document.contentType = uploadedFile.file.content_type
    document.filePath = settings.BASE_DIR + '/' + document.filename
    if relatedObject.__class__.__name__.lower() == "queryset":
        if len(relatedObject) == 1:
            setattr(document, relatedObject[0].__class__.__name__.lower(), relatedObject[0])
        else:
            print "ERROR: The queryset object had %d elements to it. Expected only one." % len(relatedObject)
            return None
    else:
        setattr(document, relatedObject.__class__.__name__.lower(), relatedObject)
    print document.filePath
    wfile = open(document.filePath, "w")
    wfile.write(fileContent)
    wfile.close()
    document.save()

@api_view(['GET', 'POST'])
def competitions(request):
    if request.method == 'GET':
        return listObjects(Competition, CompetitionSerializer)
    elif request.method == 'POST':
        # print "\nServer side - competitions:\n"+str(request.POST)
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
        # print "\nServer side - teams:\n"+str(request.POST)
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

@api_view(['GET', 'POST'])
def plugins(request):
    if request.method == 'GET':
        return listObjects(Plugin, PluginSerializer)
    elif request.method == 'POST':
        return postObject(request, PluginSerializer)

@api_view(['GET', 'PATCH', 'DELETE'])
def plugin(request, pluginId):
    if not objectExists(Plugin, pluginId = pluginId):
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        return listObject(Plugin, PluginSerializer, pluginId = pluginId)
    elif request.method == 'PATCH':
        return patchObject(request, Plugin, PluginSerializer, pluginId = pluginId)
    elif request.method == 'DELETE':
        return deleteObject(Plugin, pluginId = pluginId)

@api_view(['GET', 'POST'])
def users(request):
    if request.method == 'GET':
        return listObjects(User, UserSerializer)
    elif request.method == 'POST':
        return postObject(request, UserSerializer)

@api_view(['GET', 'PATCH', 'DELETE'])
def user(request, userId):
    if not objectExists(User, userId = userId):
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        return listObject(User, UserSerializer, userId = userId)
    elif request.method == 'PATCH':
        return patchObject(request, User, UserSerializer, userId = userId)
    elif request.method == 'DELETE':
        return deleteObject(User, userId = userId)

@api_view(['GET', 'POST'])
def organizations(request):
    if request.method == 'GET':
        return listObjects(Organization, OrganizationSerializer)
    elif request.method == 'POST':
        return postObject(request, OrganizationSerializer)

@api_view(['GET', 'PATCH', 'DELETE'])
def organization(request, organizationId):
    if not objectExists(Organization, organizationId = organizationId):
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        return listObject(Organization, OrganizationSerializer, organizationId = organizationId)
    elif request.method == 'PATCH':
        return patchObject(request, Organization, OrganizationSerializer, organizationId = organizationId)
    elif request.method == 'DELETE':
        return deleteObject(Organization, organizationId = organizationId)
