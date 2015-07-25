from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ScoringEngine.serializers import OrganizationSerializer
from ScoringEngine.serializers import UserSerializer
from ScoringEngine.models import Organization
from ScoringEngine.models import User

from WebApi.views.utils import objectExists
from WebApi.views.utils import listObjects
from WebApi.views.utils import postObject
from WebApi.views.utils import listObject
from WebApi.views.utils import patchObject
from WebApi.views.utils import deleteObject

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

@api_view(['GET', 'POST'])
def members(request, organizationId):
	if request.method == 'GET':
		return listObjects(User, UserSerializer)
	elif request.method == 'POST':
		return postObject(request, UserSerializer)

@api_view(['GET', 'PATCH', 'DELETE'])
def member(request, organizationId, memberId):
	if not objectExists(User, organizationId = organizationId, userId=memberId):
		return Response(status = status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		return listObject(User, UserSerializer, organizationId = organizationId, userId=memberId)
	elif request.method == 'PATCH':
		return patchObject(request, User, UserSerializer, organizationId = organizationId, userId=memberId)
	elif request.method == 'DELETE':
		return deleteObject(User, organizationId = organizationId, userId=memberId)

@api_view(['GET', 'POST'])
def competitions(request, organizationId):
	if request.method == 'GET':
		return listObjects(Competition, CompetitionSerializer)
	elif request.method == 'POST':
		return postObject(request, CompetitionSerializer)

@api_view(['GET', 'PATCH', 'DELETE'])
def competition(request, organizationId, competitionId):
	if not objectExists(Competition, organizationId = organizationId, competitionId=competitionId):
		return Response(status = status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		return listObject(Competition, CompetitionSerializer, organizationId = organizationId, competitionId=competitionId)
	elif request.method == 'PATCH':
		return patchObject(request, Competition, CompetitionSerializer, organizationId = organizationId, competitionId=competitionId)
	elif request.method == 'DELETE':
		return deleteObject(Competition, organizationId = organizationId, competitionId=competitionId)