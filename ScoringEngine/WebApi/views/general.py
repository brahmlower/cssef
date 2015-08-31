from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

#from WebApi.views.utils import objectExists
from WebApi.views.utils import listObjects
from WebApi.views.utils import listObject
from WebApi.views.utils import postObject
from WebApi.views.utils import patchObject
from WebApi.views.utils import deleteObject

# from ScoringEngine.ScoringEngine import Plugin
# from ScoringEngine.endpoints import User

# @api_view(['GET', 'POST'])
# def plugins(request):
# 	if request.method == 'GET':
# 		return listObjects(Plugin, 'search')
# 	elif request.method == 'POST':
# 		return postObject(Plugin, Plugin.newPlugin, request)

# @api_view(['GET', 'PATCH', 'DELETE'])
# def plugin(request, pluginId):
# 	if request.method == 'GET':
# 		return listObject(Plugin, Plugin.getPlugin, pluginId = pluginId)
# 	elif request.method == 'PATCH':
# 		return patchObject(Plugin, Plugin.editPlugin, pluginId = pluginId)
# 	elif request.method == 'DELETE':
# 		return callObject(Plugin, 'delete', content = False, pluginId = pluginId)
# 		#obj = Plugin.getPlugin(pluginId = pluginId)
# 		#return deleteObject(Plugin, Plugin.deletePlugin, obj)

