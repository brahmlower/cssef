from django.shortcuts import render_to_response
from cssefclient import CssefClient

client = CssefClient()
client.config.loadConfigFile('/etc/cssef/cssef.yml')
client.connect()

def makeApiRequest(apiEndpointString, argsDict, apiConnection = client.config.serverConnection):
	#print '[UTILS] Making api request to endpoint "%s" with arguments "%s"' % (apiEndpoint, argsDict)
	#command = apiEndpoint(apiConnection)
	#return command.execute(**argsDict)
	x = ServerEndpoints()
	return getattr(x, apiEndpointString).execute(**argsDict)

def getContext(contextClass, pageTemplate, request, **kwargs):
	context = contextClass(request, **kwargs)
	context.processContext()
	return render_to_response(pageTemplate, context.getContext())