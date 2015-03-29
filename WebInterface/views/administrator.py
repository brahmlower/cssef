from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
from django.core.context_processors import csrf

API_URL="http://127.0.0.1/api/v1/"

def home(request):
	"""
	Page displayed after loggin in
	"""
	return render_to_response('administrator/home.html', c)

def login(request):
	"""
	Page for admins to login to for competition management
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	c["form"] = {'login': AdminLoginForm()}

	c.update(csrf(request))
	# Checks if the user is submitting the form, or requesting the form
	if request.method != "POST":
		return render_to_response('administrator/login.html', c)
	username = request.POST.get('username')
	password = request.POST.get('password')
	# TODO: The following line can throw a MultiValueDictKeyError
	admin = auth.authenticate(username = username, password = password)
	if admin == None:
		c["messages"].new_info("Incorrect credentials.", 4321)
		return render_to_response('administrator/login.html', c)
	# Checks that the submitted form data is valid
	auth.login(request, admin)
	return HttpResponseRedirect("/admin/home")

def logout(request):
	"""
	Page for teams to logout of a competition
	"""
	auth.logout(request)
	return HttpResponseRedirect("/")

def siteConfig(request):
	"""
	Displays configuration options for the overall site
	"""
	return render_to_response('administrator/home.html', c)

def listUsers(request):
	"""
	Displays site or competition administrative users
	"""
	return render_to_response('administrator/listUsers.html', c)

def editUser(request):
	"""
	Edit a site or competition administrative user
	"""
	return render_to_response('administrator/editUser.html', c)

def deleteUser(request):
	"""
	Delete site or competition administrative users
	"""
	return HttpResponseRedirect('/admin/users/')

def createUser(request):
	"""
	Create site or competition administrative users
	"""
	return render_to_response('administrator/createUser.html', c)

def listPlugins(request):
	# Query the webapi to get a list of the plugins
	queryUrl = API_URL + "plugins.json"
	jsonString = urlopen(queryUrl).read()
	pluginList = json.loads(jsonString)
	context = {'pluginList': pluginList}
	return render_to_response('administrator/listPlugins.html', c)

def createPlugin(request):
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	if request.method != "POST":
		c.update(csrf(request))
		c["action"] = "create"
		c["form"] = CreateServiceModuleForm()
		return render_to_response('administrator/createEditPlugin.html', c)
	form_obj = CreateServiceModuleForm(request.POST, request.FILES)
	if 'docfile' in request.FILES and form_obj.is_valid():
		form_obj.cleaned_data.pop('docfile', None)
		servmdul_obj = ServiceModule(**form_obj.cleaned_data)
		servmdul_obj.save()
		save_document(request.FILES['docfile'], settings.CONTENT_PLUGGINS_PATH, servmdul_obj, ashash = False)
	else:
		# Not exactly giving the user an error message here (TODO)
		c.update(csrf(request))
		c["action"] = "create"
		c["form"] = CreateServiceModuleForm()
		return render_to_response('administrator/createEditPlugin.html', c)
	return HttpResponseRedirect('/admin/servicemodules/')

def deletePlugin(request, servmdulid = None):
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	servmdul_obj = ServiceModule.objects.get(servmdulid = servmdulid)
	servmdul_obj.delete()
	return HttpResponseRedirect("/admin/servicemodules/")

def editPlugin(request, servmdulid = None):
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c.update(csrf(request))
	c["action"] = "edit"
	if request.method != "POST":
		servmdul_obj = ServiceModule.objects.filter(servmdulid = servmdulid)
		c["servmdulid"] = servmdul_obj[0].servmdulid
		c["docfile"] = Document.objects.get(servicemodule = servmdul_obj[0])
		c["form"] = CreateServiceModuleForm(initial = servmdul_obj.values()[0])
		return render_to_response('administrator/createEditPlugin.html', c)
	form_obj = CreateServiceModuleForm(request.POST, request.FILES)
	if 'docfile' in request.FILES and form_obj.is_valid():
		form_obj.cleaned_data.pop('docfile', None)
		servmdul_obj = ServiceModule.objects.filter(servmdulid = servmdulid)
		servmdul_obj.update(**form_obj.cleaned_data)
		docfile = Document.objects.get(servicemodule = servmdul_obj[0].servmdulid)
		docfile.delete()
		save_document(request.FILES['docfile'], settings.CONTENT_PLUGGINS_PATH, servmdul_obj[0], ashash = False)
		return HttpResponseRedirect('/admin/servicemodules/')
	else:
		# Not exactly giving the user an error message here (TODO)
		print "there were errors"
		c["form"] = CreateServiceModuleForm()
		return render_to_response('administrator/createEditPlugin.html', c)

def testPlugin(request, servmdulid = None):
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
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