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
from WebInterface import cssefApi
from WebInterface.utils import ContextFactory
from django.core.files.uploadedfile import UploadedFile

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

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/")

def siteConfig(request):
	context = ContextFactory(request)
	return render_to_response('administrator/siteConfigs.html', context.General())

def listUsers(request):
	if request.method == 'POST':
		response = cssefApi.delete('users/%s.json' % request.POST['objectId'])
		return HttpResponseRedirect('/admin/users/')
	context = ContextFactory(request)
	context.push({'users': cssefApi.get('users.json')})
	for i in context['users']:
		i['deleteForm'] = DeleteObject(objectId = i['userId'])
	return render_to_response('administrator/listUsers.html', context.General())

def createEditUser(request, userId = None):
	context = ContextFactory(request, userId)
	if request.method != 'POST':
		return render_to_response('administrator/createEditUser.html', context.User())
	formData = CreateUser(request.POST)
	if not formData.is_valid():
		return render_to_response('administrator/createEditUser.html', context.User())
	response = cssefApi.post('users.json', formData.cleaned_data)
	return HttpResponseRedirect('/admin/users/')

def listOrganizations(request):
	if request.method == 'POST':
		response = cssefApi.delete('organizations/%s.json' % request.POST['objectId'])
		return HttpResponseRedirect('/admin/organizations/')
	context = ContextFactory(request)
	context.push({'organizations': cssefApi.get('organizations.json')})
	for i in context['organizations']:
		i['deleteForm'] = DeleteObject(objectId = i['organizationId'])
	return render_to_response('administrator/listOrganizations.html', context.General())

def createEditOrganization(request, organizationId = None):
	context = ContextFactory(request, organizationId)
	if request.method != 'POST':
		return render_to_response('administrator/createEditOrganization.html', context.Organization())
	formData = CreateOrganization(request.POST)
	if not formData.is_valid():
		return render_to_response('administrator/createEditOrganization.html', context.Organization())
	response = cssefApi.post('organizations.json', formData.cleaned_data)
	return HttpResponseRedirect('/admin/organizations/')

def listPlugins(request):
	if request.method == 'POST':
		response = cssefApi.delete('plugins/%s.json' % request.POST['objectId'])
		return HttpResponseRedirect('/admin/plugins/')
	context = ContextFactory(request)
	context.push({'plugins': cssefApi.get('plugins.json')})
	for i in context['plugins']:
		i['deleteForm'] = DeleteObject(objectId = i['pluginId'])
	return render_to_response('administrator/listPlugins.html', context.General())

def createEditPlugin(request, pluginId = None):
	context = ContextFactory(request, pluginId)
	if request.method != "POST":
		return render_to_response('administrator/createEditPlugin.html', context.Plugin())
	formData = CreatePlugin(request.POST, request.FILES)
	if 'docfile' not in request.FILES and not formData.is_valid():
		# TODO: Not exactly giving the user an error message here
		return render_to_response('administrator/createEditPlugin.html', context.Plugin())
	uploadedFile = UploadedFile(request.FILES['pluginFile'])
	fileDict = {uploadedFile.name: uploadedFile.read()}
	del formData.cleaned_data['pluginFile']
	response = cssefApi.post('plugins.json', formData.cleaned_data, files=fileDict)
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