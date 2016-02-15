from django.shortcuts import render_to_response
from cssefclient.cssefclient import Configuration
from cssefclient.cssefclient import getConn as getCeleryConnection
from cssefclient.cssefclient import ServerEndpoints

config = Configuration('/etc/cssef/cssef.conf')

def makeApiRequest(apiEndpointString, argsDict, apiConnection = getCeleryConnection(config)):
	#print '[UTILS] Making api request to endpoint "%s" with arguments "%s"' % (apiEndpoint, argsDict)
	#command = apiEndpoint(apiConnection)
	#return command.execute(**argsDict)
	x = ServerEndpoints(apiConnection)
	return getattr(x, apiEndpointString).execute(**argsDict)

def getContext(contextClass, pageTemplate, request, **kwargs):
	context = contextClass(request, **kwargs)
	context.processContext()
	return render_to_response(pageTemplate, context.getContext())