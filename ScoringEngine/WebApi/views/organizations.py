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
from ScoringEngine.endpoints import Organization
from ScoringEngine.endpoints import User

@api_view(['GET', 'POST'])
def organizations(request):
	if request.method == 'GET':
		return listObjects(Organization, 'search')
	elif request.method == 'POST':
		return postObject(endpoints, 'createOrganization', request)

@api_view(['GET', 'PATCH', 'DELETE'])
def organization(request, organizationId):
	if request.method == 'GET':
		return listObject(Organization, '__init__', organizationId = organizationId)
	elif request.method == 'PATCH':
		return patchObject(Organization, 'edit', request, organizationId = organizationId)
	elif request.method == 'DELETE':
		return deleteObject(Organization, 'delete', organizationId = organizationId)

@api_view(['GET', 'POST'])
def members(request, organizationId):
	organization = Organization(organizationId = organizationId)
	if request.method == 'GET':
		return listObjects(organization, 'getMembers')
	elif request.method == 'POST':
		return postObject(organization, 'createMember', request)

@api_view(['GET', 'PATCH', 'DELETE'])
def member(request, organizationId, memberId):
	organization = Organization(organizationId = organizationId)
	if request.method == 'GET':
		return callObject(organization, 'getMember', content = True, userId = memberId)
	elif request.method == 'PATCH':
		return patchObject(organization, 'editMember', request, userId = memberId)
	elif request.method == 'DELETE':
		return callObject(organization, 'deleteMember', content = False, userId = memberId)

@api_view(['GET', 'POST'])
def competitions(request, organizationId):
	organization = Organization(organizationId = organizationId)
	if request.method == 'GET':
		return listObjects(organization, 'getCompetitions')
	elif request.method == 'POST':
		return postObject(organization, 'createCompetition', request)

@api_view(['GET', 'PATCH', 'DELETE'])
def competition(request, organizationId, competitionId):
	organization = Organization(organizationId = organizationId)
	if request.method == 'GET':
		return callObject(organization, 'getCompetition', content = True, competitionId = competitionId)
	elif request.method == 'PATCH':
		return patchObject(organization, 'edit', request, competitionId = competitionId)
	elif request.method == 'DELETE':
		return callObject(organization, 'deleteCompetition', content = False, competitionId = competitionId)

@api_view(['GET'])
def users(request):
	if request.method == 'GET':
		return listObjects(User, 'search')
	# User creation should only happen from within the Organization member list

@api_view(['GET', 'PATCH'])
def user(request, userId):
	if request.method == 'GET':
		#return listObject(User, User.getUser, userId = userId)
		return listObject(User, '__init__', userId = userId)
	elif request.method == 'PATCH':
		#return patchObject(User, User.editUser, request, userId = userId)
		return patchObject(User, 'edit', request, userId = userId)

