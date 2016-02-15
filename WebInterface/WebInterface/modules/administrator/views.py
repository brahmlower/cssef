from WebInterface.utils import getContext
from WebInterface.context import BaseContext
from WebInterface.modules.administrator.context import CreateOrganizationContext
from WebInterface.modules.administrator.context import EditOrganizationContext
from WebInterface.modules.administrator.context import ListOrganizationContext
from WebInterface.modules.administrator.context import CreateUserContext
from WebInterface.modules.administrator.context import DeleteUserContext
from WebInterface.modules.administrator.context import EditUserContext
from WebInterface.modules.administrator.context import ListUserContext
from WebInterface.modules.administrator.context import ListScoringEnginesContext

templatePathPrefix = "administrator/templates/"

def home(request):
	pageTemplate = templatePathPrefix + "home.html"
	return getContext(BaseContext, pageTemplate, request)

def siteConfig(request):
	pageTemplate = templatePathPrefix + "siteConfigs.html"
	return getContext(BaseContext, pageTemplate, request)

#####################################
# User management pages
#####################################
def listUsers(request):
	pageTemplate = templatePathPrefix + 'listUsers.html'
	return getContext(ListUserContext, pageTemplate, request)

def createUser(request):
	pageTemplate = templatePathPrefix + 'createEditUser.html'
	return getContext(CreateUserContext, pageTemplate, request)

def editUser(request, userId):
	pageTemplate = templatePathPrefix + 'createEditUser.html'
	return getContext(EditUserContext, pageTemplate, request, pkid = userId)

def deleteUser(request):
	pageTemplate = templatePathPrefix + 'pageTemplate.html'
	return getContext(DeleteUserContext, pageTemplate, request)

#####################################
# Organization management pages
#####################################
def listOrganizations(request):
	pageTemplate = templatePathPrefix + 'listOrganizations.html'
	return getContext(ListOrganizationContext, pageTemplate, request)

def createOrganization(request):
	pageTemplate = templatePathPrefix + 'createEditOrganization.html'
	return getContext(CreateOrganizationContext, pageTemplate, request)

def editOrganization(request, organizationId):
	pageTemplate = templatePathPrefix + 'createEditOrganization.html'
	return getContext(EditOrganizationContext, pageTemplate, request, pkid = organizationId)

#####################################
# Organization management pages
#####################################
def listScoringEngines(request):
	pageTemplate = templatePathPrefix + 'listScoringEngines.html'
	return getContext(ListScoringEnginesContext, pageTemplate, request)

def createScoringEngine(request):
	pass

def editScoringEngine(request):
	pass

# Holding on to the plugin code until I work out how best to include it in the new codebase.
#####################################
# Plugin management pages
#####################################
# def listPlugins(request):
# 	context = ContextFactory(request)
# 	command = CssefClient.pluginsGet
# 	command.conn = getCeleryConnection(config)
# 	output = command()
# 	if output['value'] == 0:
# 		context.push({'plugins': output['value']})
# 	return render_to_response('administrator/listPlugins.html', context.General())

# def createEditPlugin(request, pluginId = None):
# 	context = ContextFactory(request, pluginId)
# 	if request.method != "POST":
# 		return render_to_response('administrator/createEditPlugin.html', context.Plugin())
# 	print 'not posting'
# 	formData = CreatePlugin(request.POST, request.FILES)
# 	if not formData.is_valid():
# 		# TODO: Not exactly giving the user an error message here
# 		return render_to_response('administrator/createEditPlugin.html', context.Plugin())
# 	if 'pluginFile' in request.FILES:
# 		# A file was uploaded
# 		uploadedFile = UploadedFile(request.FILES['pluginFile'])
# 		fileDict = {uploadedFile.name: uploadedFile.read()}
# 		del formData.cleaned_data['pluginFile']
# 		response = cssefApi.post('plugins.json', formData.cleaned_data, files=fileDict)
# 	else:
# 		# No file was uploaded
# 		response = cssefApi.post('plugins.json', formData.cleaned_data)
# 	if response.status_code/200 != 1:
# 		return HttpResponse(response.text)
# 	return HttpResponseRedirect('/admin/plugins/')

# def testPlugin(request, pluginId = None):
# 	c.update(csrf(request))
# 	c['servmdul_obj'] = ServiceModule.objects.get(servmdulid = servmdulid)
# 	serv_obj = Service(servicemodule = c['servmdul_obj'])
# 	c["depend_list"] = buildServiceDependencyList(serv_obj)
# 	if request.method != "POST":
# 		# Serve blank form with no results
# 		c["service_configs"] = buildServiceConfigForm(serv_obj, TestServiceForm())
# 		return render_to_response('administrator/testPlugin.html', c)
# 	c["service_configs"] = buildServiceConfigForm(serv_obj, TestServiceForm(), request.POST)

# 	form_dict = request.POST.copy().dict()
# 	form_dict.pop('csrfmiddlewaretoken')
# 	# Clean network address
# 	if form_dict['networkaddr'][-1] == ".":
# 		form_dict['networkaddr'] = form_dict['networkaddr'][:-1]
# 	if form_dict['networkaddr'][0] == ".":
# 		form_dict['networkaddr'] = form_dict['networkaddr'][1:]
# 	# Clean machine address value
# 	if form_dict['networkloc'][0] == ".":
# 		form_dict['networkloc'] = form_dict['networkloc'][1:]
# 	if form_dict['networkloc'][-1] == ".":
# 		form_dict['networkloc'] = form_dict['networkloc'][:-1]
# 	# Prepare the service object for use in the module
# 	if form_dict.pop('connectip') == u'0':
# 		serv_obj.connectip = False
# 	else:
# 		serv_obj.connectip = True
# 	serv_obj.name = c['servmdul_obj'].modulename
# 	serv_obj.networkloc = str(form_dict.pop('networkloc'))
# 	serv_obj.defaultport = int(form_dict.pop('defaultport'))
# 	serv_obj.points = 100
# 	c['score_obj'] = run_plugin_test(serv_obj, form_dict)
# 	return render_to_response('administrator/testPlugin.html', c)