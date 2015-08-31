from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from WebApi.views.utils import callObject
from WebApi.views.utils import listObjects
from WebApi.views.utils import listObject
from WebApi.views.utils import postObject
from WebApi.views.utils import patchObject
from WebApi.views.utils import deleteObject

from ScoringEngine.endpoints import Competition
import endpoints

@api_view(['GET', 'POST'])
def services(request, competitionId):
	if request.method == 'GET':
		return listObjects(endpoints, 'getServices')
	elif request.method == 'POST':
		return postObject(endpoints, 'createService', request)

@api_view(['GET', 'PATCH', 'DELETE'])
def service(request, competitionId, serviceId):
	if request.method == 'GET':
		return callObject(endpoints, 'getService', content = True, serviceId = serviceId, competitionId = competitionId)
	elif request.method == 'PATCH':
		return patchObject(endpoints, 'editService', request, serviceId = serviceId, competitionId = competitionId)
	elif request.method == 'DELETE':
		return callObject(endpoints, 'deleteService', content = False, serviceId = serviceId, competitionId = competitionId)

@api_view(['GET', 'POST'])
def plugins(request):
	if request.method == 'GET':
		return callObject(endpoints, 'getServices', content = True)
	elif request.method == 'POST':
		return postObject(endpoints, 'createPlugin', request)

@api_view(['GET', 'PATCH', 'DELETE'])
def plugin(request, pluginId):
	if request.method == 'GET':
		return callObject(endpoints, 'getService', content = True, pluginId = pluginId)
	elif request.method == 'PATCH':
		return patchObject(endpoints, 'editPlugin', request, pluginId = pluginId)
	elif request.method == 'DELETE':
		return callObject(endpoints, 'deletePlugin', content = False, pluginId = pluginId)