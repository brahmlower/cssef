from django.shortcuts import render_to_response
from django.shortcuts import redirect
from cssefclient import CssefClient
from cssefclient.utils import RPCEndpoint

client = CssefClient()
client.config.load_config_file('/etc/cssef/cssef.yml')
client.connect()
auth_dict = {'username': 'admin', 'password': 'admin', 'organization': 1}

def makeApiRequest(apiEndpointString, args_dict, apiConnection = client.config.server_connection):
	print '[UTILS] Making api request to endpoint "%s" with arguments "%s"' % (apiEndpointString, args_dict)
	args_dict['auth'] = auth_dict
	output = RPCEndpoint(client.config, apiEndpointString).execute(**args_dict)
	return output.as_dict()

def getContext(contextClass, request, page_template = None, redirect_url = None, **kwargs):
	context = contextClass(request, **kwargs)
	context.processContext()
	if page_template and not redirect_url:
		return render_to_response(page_template, context.getContext())
	elif redirect_url and not page_template:
		context.getContext()
		return redirect(redirect_url)
	else:
		print "Neither a page_template nor redirect_url was provided."
		raise Exception