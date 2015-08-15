from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

#from WebApi.views.utils import objectExists
from WebApi.views.utils import listObjects
from WebApi.views.utils import listObject
from WebApi.views.utils import postObject
from WebApi.views.utils import patchObject
from WebApi.views.utils import deleteObject

from ScoringEngine.ScoringEngine import Plugin
from ScoringEngine.endpoints import User

@api_view(['GET', 'POST'])
def plugins(request):
	if request.method == 'GET':
		return listObjects(Plugin, 'search')
	elif request.method == 'POST':
		return postObject(Plugin, Plugin.newPlugin, request)

@api_view(['GET', 'PATCH', 'DELETE'])
def plugin(request, pluginId):
	if request.method == 'GET':
		return listObject(Plugin, Plugin.getPlugin, pluginId = pluginId)
	elif request.method == 'PATCH':
		return patchObject(Plugin, Plugin.editPlugin, pluginId = pluginId)
	elif request.method == 'DELETE':
		obj = Plugin.getPlugin(pluginId = pluginId)
		return deleteObject(Plugin, Plugin.deletePlugin, obj)

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
