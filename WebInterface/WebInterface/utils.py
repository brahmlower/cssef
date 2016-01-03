from django.shortcuts import render_to_response
from cssefclient.cssefclient import Configuration
from cssefclient.cssefclient import getConn as getCeleryConnection

config = Configuration('/etc/cssef/cssef.conf')

def makeApiRequest(apiEndpoint, argsDict, apiConnection = getCeleryConnection(config)):
	print '[UTILS] Making api request to endpoint "%s" with arguments "%s"' % (apiEndpoint, argsDict)
	command = apiEndpoint(apiConnection)
	return command.execute(**argsDict)

def getContext(contextClass, pageTemplate, request, **kwargs):
	context = contextClass(request, **kwargs)
	context.processContext()
	return render_to_response(pageTemplate, context.getContext())