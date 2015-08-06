from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from WebApi.views.utils import objectExists
from WebApi.views.utils import listObjects
from WebApi.views.utils import listObject
from WebApi.views.utils import postObject
from WebApi.views.utils import patchObject
from WebApi.views.utils import deleteObject

from ScoringEngine.endpoints import Organization

@api_view(['GET', 'POST'])
def organizations(request):
	if request.method == 'GET':
		return listObjects(Organization, 'search')
		#return listObjects(Organization, OrganizationSerializer)
	elif request.method == 'POST':
		#return postObject(request, OrganizationSerializer)
		return postObject(Organization, 'create', request)

@api_view(['GET', 'PATCH', 'DELETE'])
def organization(request, organizationId):
	if request.method == 'GET':
		#return listObject(Organization, OrganizationSerializer, organizationId = organizationId)
		return listObject(Organization, '__init__', organizationId = organizationId)
	elif request.method == 'PATCH':
		return patchObject(request, Organization, OrganizationSerializer, organizationId = organizationId)
	elif request.method == 'DELETE':
		return deleteObject(Organization, organizationId = organizationId)

@api_view(['GET', 'POST'])
def members(request, organizationId):
	organization = Organization(organizationId)
	if request.method == 'GET':
		return listObjects(organization, Organization.getMembers)
	elif request.method == 'POST':
		return postObject(organization, Organization.newMember, request)

@api_view(['GET', 'PATCH', 'DELETE'])
def member(request, organizationId, memberId):
	organization = Organization(organizationId)
	if request.method == 'GET':
		return listObject(organization, Organization.getMember, userId = memberId)
	elif request.method == 'PATCH':
		return patchObject(organization, Organization.editMember, userId = memberId)
	elif request.method == 'DELETE':
		obj = organization.getMember(userId = memberId)
		return deleteObject(organization, Organization.deleteMember, obj)

@api_view(['GET', 'POST'])
def competitions(request, organizationId):
	organization = Organization(organizationId)
	if request.method == 'GET':
		return listObjects(organization, Organization.getCompetitions)
	elif request.method == 'POST':
		return postObject(organization, Organization.newCompetition, request)

@api_view(['GET', 'PATCH', 'DELETE'])
def competition(request, organizationId, competitionId):
	organization = Organization(organizationId)
	if request.method == 'GET':
		return listObject(organization, Organization.getCompetition, competitionId = competitionId)
	elif request.method == 'PATCH':
		return patchObject(organization, Organization.editCompetition, competitionId = competitionId)
	elif request.method == 'DELETE':
		obj = organization.getCompetition(competitionId = competitionId)
		return deleteObject(organization, Organization.deleteCompetition, obj)