from django.shortcuts import render_to_response
from django.shortcuts import redirect
from cssefclient import CssefClient
from cssefclient.utils import RPCEndpoint

client = CssefClient()
client.config.loadConfigFile('/etc/cssef/cssef.yml')
client.connect()
auth_dict = {'username': 'admin', 'password': 'admin', 'organization': 1}

def makeApiRequest(apiEndpointString, args_dict, apiConnection = client.config.serverConnection):
	print '[UTILS] Making api request to endpoint "%s" with arguments "%s"' % (apiEndpointString, args_dict)
	args_dict['auth'] = auth_dict
	output = RPCEndpoint(client.config, apiEndpointString).execute(**args_dict)
	return output.as_dict()

def getContext(contextClass, pageTemplate, request, redirect_url = None, **kwargs):
	context = contextClass(request, **kwargs)
	context.processContext()
	if not redirect_url:
		return render_to_response(pageTemplate, context.getContext())
	else:
		context.getContext()
		return redirect(redirect_url)