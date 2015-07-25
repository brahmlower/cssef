from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from ScoringEngine.serializers import PluginSerializer
from ScoringEngine.serializers import UserSerializer
from ScoringEngine.models import User
from ScoringEngine.models import Plugin

from WebApi.views.utils import objectExists
from WebApi.views.utils import listObjects
from WebApi.views.utils import listObject
from WebApi.views.utils import postObject
from WebApi.views.utils import patchObject
from WebApi.views.utils import deleteObject

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

