from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
from django.core.context_processors import csrf
from urllib import urlencode
import urllib2
from WebInterface.forms import LoginSiteAdmin
from WebInterface.forms import CreateOrganization
from WebInterface.forms import CreateUser
from WebInterface.forms import CreatePlugin
from WebInterface.forms import DeleteObject
from WebInterface.settings import SCORING_ENGINE_API_URL
import json

class ContextFactory():
	ACTION_EDIT = 'create'
	ACTION_CREATE = 'edit'
	def __init__(self, request, objectId):
		self.request = request
		self.data = None
		if not objectId:
			self.objectId = objectId
			self.action = ContextFactory.ACTION_EDIT
		else:
			self.objectId = str(objectId)
			self.action = ContextFactory.ACTION_CREATE
		self.context = {}
		self.context.update(csrf(self.request))
		self.context['action'] = self.action

	def Organization(self):
		if self.objectId:
			self.context['organizationId'] = self.objectId
			self.data = apiQuery('organizations/%s.json' % self.objectId)
		self.context['form'] = CreateOrganization(initial = self.data)
		return self.context

	def User(self):
		if self.objectId:
			self.context['userId'] = self.objectId
			self.data = apiQuery('users/%s.json' % self.objectId)
		self.context['form'] = CreateUser(initial = self.data)
		return self.context

def apiPost(page, unencodedData):
	url = SCORING_ENGINE_API_URL + page
	data = urlencode(unencodedData)
	return urllib2.urlopen(url, data)

def apiGet(page):
	url = SCORING_ENGINE_API_URL + page
	return urllib2.urlopen(url)

def apiDelete(page):
	url = SCORING_ENGINE_API_URL + page
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	request = urllib2.Request(url, None)
	request.get_method = lambda: 'DELETE'
	return urllib2.urlopen(request)

def apiQuery(page):
	response = apiGet(page)
	jsonString = response.read()
	return json.loads(jsonString)

def home(request):
	context = {}
	return render_to_response('administrator/home.html', context)

def login(request):
	context = {}
	context["form"] = LoginSiteAdmin()
	context.update(csrf(request))
	# Checks if the user is submitting the form, or requesting the form
	if request.method != "POST":
		return render_to_response('administrator/login.html', context)
	username = request.POST.get('username')
	password = request.POST.get('password')
	# TODO: The following line can throw a MultiValueDictKeyError
	admin = auth.authenticate(username = username, password = password)
	if admin == None:
		return render_to_response('administrator/login.html', context)
	# Checks that the submitted form data is valid
	auth.login(request, admin)
	return HttpResponseRedirect("/admin/home")

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/")

def siteConfig(request):
	context = {}
	return render_to_response('administrator/siteConfigs.html', context)

def listUsers(request):
	if request.method == 'POST':
		response = apiDelete('users/%s.json' % request.POST['objectId'])
		return HttpResponseRedirect('/admin/users/')
	context = {}
	context.update(csrf(request))
	context['users'] = apiQuery('users.json')
	for i in context['users']:
		i['deleteForm'] = DeleteObject(objectId = i['userId'])
	return render_to_response('administrator/listUsers.html', context)

def createEditUser(request, userId = None):
	context = ContextFactory(request, userId)
	if request.method != 'POST':
		return render_to_response('administrator/createEditUser.html', context.User())
	formData = CreateUser(request.POST)
	if not formData.is_valid():
		return render_to_response('administrator/createEditUser.html', context.User())
	response = apiPost('users.json', formData.cleaned_data)
	return HttpResponseRedirect('/admin/users/')

def listOrganizations(request):
	if request.method == 'POST':
		response = apiDelete('organizations/%s.json' % request.POST['objectId'])
		return HttpResponseRedirect('/admin/organizations/')
	context = {}
	context.update(csrf(request))
	context['organizations'] = apiQuery('organizations.json')
	for i in context['organizations']:
		i['deleteForm'] = DeleteObject(objectId = i['organizationId'])
	return render_to_response('administrator/listOrganizations.html', context)

def createEditOrganization(request, organizationId = None):
	context = ContextFactory(request, organizationId)
	if request.method != 'POST':
		return render_to_response('administrator/createEditOrganization.html', context.Organization())
	formData = CreateOrganization(request.POST)
	if not formData.is_valid():
		return render_to_response('administrator/createEditOrganization.html', context.Organization())
	response = apiPost('organizations.json', formData.cleaned_data)
	return HttpResponseRedirect('/admin/organizations/')

def listPlugins(request):
	if request.method == 'POST':
		response = apiDelete('plugins/%s.json' % request.POST['objectId'])
		return HttpResponseRedirect('/admin/plugins/')
	context = {}
	context.update(csrf(request))
	context['plugins'] = apiQuery('plugins.json')
	for i in context['plugins']:
		i['deleteForm'] = DeleteObject(objectId = i['pluginId'])
	return render_to_response('administrator/listPlugins.html', context)

def createPlugin(request):
	context = {}
	context.update(csrf(request))
	context["form"] = CreatePlugin()
	context["action"] = "create"
	if request.method != "POST":
		return render_to_response('administrator/createEditPlugin.html', context)
	form_obj = CreatePlugin(request.POST, request.FILES)
	if 'docfile' not in request.FILES and not form_obj.is_valid():
		# TODO: Not exactly giving the user an error message here
		return render_to_response('administrator/createEditPlugin.html', context)
	form_obj.cleaned_data.pop('docfile', None)
	# Create the plugin via the webAPI
	response = apiPost('plugins.json', form_obj.cleaned_data)
	# Need to handle a file that was uploaded (field isn't currently showing up for some reason...)
	#save_document(request.FILES['docfile'], settings.CONTENT_PLUGGINS_PATH, plugin, ashash = False)		
	return HttpResponseRedirect('/admin/plugins/')

def editPlugin(request, servmdulid = None):
	c.update(csrf(request))
	c["action"] = "edit"
	if request.method != "POST":
		plugin = ServiceModule.objects.filter(servmdulid = servmdulid)
		c["servmdulid"] = plugin[0].servmdulid
		c["docfile"] = Document.objects.get(servicemodule = plugin[0])
		c["form"] = CreatePlugin(initial = plugin.values()[0])
		return render_to_response('administrator/createEditPlugin.html', c)
	form_obj = CreatePlugin(request.POST, request.FILES)
	if 'docfile' in request.FILES and form_obj.is_valid():
		form_obj.cleaned_data.pop('docfile', None)
		plugin = ServiceModule.objects.filter(servmdulid = servmdulid)
		plugin.update(**form_obj.cleaned_data)
		docfile = Document.objects.get(servicemodule = plugin[0].servmdulid)
		docfile.delete()
		save_document(request.FILES['docfile'], settings.CONTENT_PLUGGINS_PATH, plugin[0], ashash = False)
		return HttpResponseRedirect('/admin/plugins/')
	else:
		# Not exactly giving the user an error message here (TODO)
		print "there were errors"
		c["form"] = CreatePlugin()
		return render_to_response('administrator/createEditPlugin.html', c)

def testPlugin(request, servmdulid = None):
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