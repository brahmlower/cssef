from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
from django.core.context_processors import csrf
from WebInterface.forms import LoginSiteAdmin
from WebInterface.forms import CreateOrganization
from WebInterface.forms import CreateUser
from WebInterface.forms import CreatePlugin
from WebInterface.forms import DeleteObject
from WebInterface.settings import SCORING_ENGINE_API_URL
from WebInterface.utils import ContextFactory
from django.core.files.uploadedfile import UploadedFile

from WebInterface.client import getConn as getCeleryConnection
# from WebInterface.client import CompetitionAdd as ApiCompetitionAdd
# from WebInterface.client import CompetitionDel as ApiCompetitionDel
# from WebInterface.client import CompetitionGet as ApiCompetitionGet
# from WebInterface.client import CompetitionSet as ApiCompetitionSet
# from WebInterface.client import CompetitionTeamAdd as 
# from WebInterface.client import CompetitionTeamDel as 
# from WebInterface.client import CompetitionTeamSet as 
# from WebInterface.client import CompetitionTeamGet as 
# from WebInterface.client import CompetitionScoreAdd as 
# from WebInterface.client import CompetitionScoreDel as 
# from WebInterface.client import CompetitionScoreSet as 
# from WebInterface.client import CompetitionScoreGet as 
# from WebInterface.client import CompetitionInjectAdd as 
# from WebInterface.client import CompetitionInjectDel as 
# from WebInterface.client import CompetitionInjectSet as 
# from WebInterface.client import CompetitionInjectGet as 
# from WebInterface.client import CompetitionInjectResponseAdd as 
# from WebInterface.client import CompetitionInjectResponseDel as 
# from WebInterface.client import CompetitionInjectResponseSet as 
# from WebInterface.client import CompetitionInjectResponseGet as 
# from WebInterface.client import CompetitionIncidentAdd as 
# from WebInterface.client import CompetitionIncidentDel as 
# from WebInterface.client import CompetitionIncidentSet as 
# from WebInterface.client import CompetitionIncidentGet as 
# from WebInterface.client import CompetitionIncidentResponseAdd as 
# from WebInterface.client import CompetitionIncidentResponseDel as 
# from WebInterface.client import CompetitionIncidentResponseSet as 
# from WebInterface.client import CompetitionIncidentResponseGet as 
# from WebInterface.client import DocumentAdd as 
# from WebInterface.client import DocumentDel as 
# from WebInterface.client import DocumentSet as 
# from WebInterface.client import DocumentGet as 
# from WebInterface.client import ScoringEngineAdd as 
# from WebInterface.client import ScoringEngineDel as 
# from WebInterface.client import ScoringEngineSet as 
# from WebInterface.client import ScoringEngineGet as 

from WebInterface.utils import CreateOrganizationContext
from WebInterface.utils import EditOrganizationContext
from WebInterface.utils import ListOrganizationContext

from WebInterface.utils import CreateUserContext
from WebInterface.utils import EditUserContext
from WebInterface.utils import ListUserContext

def getContext(contextClass, pageTemplate, request, **kwargs):
	context = contextClass(request, **kwargs)
	context.processContext()
	return render_to_response(pageTemplate, context.getContext())

def home(request):
	context = ContextFactory(request)
	return render_to_response('administrator/home.html', context.General())

def login(request):
	context = ContextFactory(request)
	context.push({'form': LoginSiteAdmin()})
	# Checks if the user is submitting the form, or requesting the form
	if request.method != "POST":
		return render_to_response('administrator/login.html', context.General())
	username = request.POST.get('username')
	password = request.POST.get('password')
	# TODO: The following line can throw a MultiValueDictKeyError
	admin = auth.authenticate(username = username, password = password)
	if admin == None:
		return render_to_response('administrator/login.html', context.General())
	# Checks that the submitted form data is valid
	auth.login(request, admin)
	return HttpResponseRedirect("/admin/home")

def siteConfig(request):
	context = ContextFactory(request)
	return render_to_response('administrator/siteConfigs.html', context.General())

#####################################
# User management pages
#####################################
def listUsers(request):
	pageTemplate = 'administrator/listUsers.html'
	return getContext(ListUserContext, pageTemplate, request)

def createUser(request):
	pageTemplate = 'administrator/createEditUser.html'
	return getContext(CreateUserContext, pageTemplate, request)

def editUser(request):
	pageTemplate = 'administrator/createEditUser.html'
	return getContext(EditUserContext, pageTemplate, request)

# def createEditUser(request, userId = None):
# 	context = ContextFactory(request, userId)
# 	if request.method != 'POST':
# 		return render_to_response('administrator/createEditUser.html', context.User())
# 	formData = CreateUser(request.POST)
# 	if not formData.is_valid():
# 		return render_to_response('administrator/createEditUser.html', context.User())
# 	print formData.cleaned_data
# 	response = cssefApi.post('users.json', formData.cleaned_data)
# 	if response.status_code/200 != 1:
# 		return HttpResponse(response.text)
# 	return HttpResponseRedirect('/admin/users/')

#####################################
# Organization management pages
#####################################
def listOrganizations(request):
	pageTemplate = 'administrator/listOrganizations.html'
	return getContext(ListOrganizationContext, pageTemplate, request)

def createOrganization(request):
	pageTemplate = 'administrator/createEditOrganization.html'
	return getContext(CreateOrganizationContext, pageTemplate, request)

def editOrganization(request, organizationId):
	pageTemplate = 'administrator/createEditOrganization.html'
	return getContext(EditOrganizationContext, pageTemplate, request, pkid = organizationId)

#####################################
# Plugin management pages
#####################################
def listPlugins(request):
	context = ContextFactory(request)
	command = CssefClient.pluginsGet
	command.conn = getCeleryConnection()
	output = command()
	if output['value'] == 0:
		context.push({'plugins': output['value']})
	return render_to_response('administrator/listPlugins.html', context.General())

def createEditPlugin(request, pluginId = None):
	context = ContextFactory(request, pluginId)
	if request.method != "POST":
		return render_to_response('administrator/createEditPlugin.html', context.Plugin())
	print 'not posting'
	formData = CreatePlugin(request.POST, request.FILES)
	if not formData.is_valid():
		# TODO: Not exactly giving the user an error message here
		return render_to_response('administrator/createEditPlugin.html', context.Plugin())
	if 'pluginFile' in request.FILES:
		# A file was uploaded
		uploadedFile = UploadedFile(request.FILES['pluginFile'])
		fileDict = {uploadedFile.name: uploadedFile.read()}
		del formData.cleaned_data['pluginFile']
		response = cssefApi.post('plugins.json', formData.cleaned_data, files=fileDict)
	else:
		# No file was uploaded
		response = cssefApi.post('plugins.json', formData.cleaned_data)
	if response.status_code/200 != 1:
		return HttpResponse(response.text)
	return HttpResponseRedirect('/admin/plugins/')

def testPlugin(request, pluginId = None):
	c.update(csrf(request))
	c['servmdul_obj'] = ServiceModule.objects.get(servmdulid = servmdulid)
	serv_obj = Service(servicemodule = c['servmdul_obj'])
	c["depend_list"] = buildServiceDependencyList(serv_obj)
	if request.method != "POST":
		# Serve blank form with no results
		c["service_configs"] = buildServiceConfigForm(serv_obj, TestServiceForm())
		return render_to_response('administrator/testPlugin.html', c)
	c["service_configs"] = buildServiceConfigForm(serv_obj, TestServiceForm(), request.POST)

	form_dict = request.POST.copy().dict()
	form_dict.pop('csrfmiddlewaretoken')
	# Clean network address
	if form_dict['networkaddr'][-1] == ".":
		form_dict['networkaddr'] = form_dict['networkaddr'][:-1]
	if form_dict['networkaddr'][0] == ".":
		form_dict['networkaddr'] = form_dict['networkaddr'][1:]
	# Clean machine address value
	if form_dict['networkloc'][0] == ".":
		form_dict['networkloc'] = form_dict['networkloc'][1:]
	if form_dict['networkloc'][-1] == ".":
		form_dict['networkloc'] = form_dict['networkloc'][:-1]
	# Prepare the service object for use in the module
	if form_dict.pop('connectip') == u'0':
		serv_obj.connectip = False
	else:
		serv_obj.connectip = True
	serv_obj.name = c['servmdul_obj'].modulename
	serv_obj.networkloc = str(form_dict.pop('networkloc'))
	serv_obj.defaultport = int(form_dict.pop('defaultport'))
	serv_obj.points = 100
	c['score_obj'] = run_plugin_test(serv_obj, form_dict)
	return render_to_response('administrator/testPlugin.html', c)