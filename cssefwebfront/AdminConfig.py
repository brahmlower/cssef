from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
from django.core.context_processors import csrf
from forms import CompetitionSettingsGeneralForm
from forms import AdminLoginForm
from forms import CreateTeamForm
from forms import TestServiceForm
from forms import CreateServiceForm
from forms import CreateServiceModuleForm
from models import ServiceModule
from models import Competition
from models import Document
from models import Service
from models import Team
from utils import UserMessages
from utils import getAuthValues
from utils import save_document
from utils import run_plugin_test
from utils import buildServiceConfigForm
import settings

def home(request):
	"""
	Page displayed after loggin in
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	return render_to_response('AdminConfig/home.html', c)

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
		return render_to_response('AdminConfig/login.html', c)
	username = request.POST.get('username')
	password = request.POST.get('password')
	# TODO: The following line can throw a MultiValueDictKeyError
	admin = auth.authenticate(username = username, password = password)
	if admin == None:
		c["messages"].new_info("Incorrect credentials.", 4321)
		return render_to_response('AdminConfig/login.html', c)
	# Checks that the submitted form data is valid
	auth.login(request, admin)
	return HttpResponseRedirect("/admin/home")

def logout(request):
	"""
	Page for teams to logout of a competition
	"""
	auth.logout(request)
	return HttpResponseRedirect("/")

def site_config(request):
	"""
	Displays configuration options for the overall site
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	return render_to_response('AdminConfig/home.html', c)

def comp_list(request):
	"""
	Displays list of competitions, add and remove competition options
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["competition_list"] = Competition.objects.all()
	return render_to_response('AdminConfig/competition_list.html', c)

def comp_create(request, competition=None):
	"""
	Creates a new competition
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	# Checks if the user is submitting the form, or requesting the form
	if request.method != "POST":
		c.update(csrf(request))
		c["form"] = CompetitionSettingsGeneralForm()
		return render_to_response('AdminConfig/competition_create.html', c)
	form_comp = CompetitionSettingsGeneralForm(request.POST)
	# Checks that submitted form data is valid
	if not form_comp.is_valid():
		print form_comp.errors
		return render(request, 'AdminConfig/competition_create.html', c)
	# Create the new competition
	Competition(**form_comp.cleaned_data).save()
	return HttpResponseRedirect('/admin/competitions/')

def comp_delete(request, competition = None):
	"""
	Delete the competition and all related objects (teams, scores, injects, services)
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	comp_obj = Competition.objects.get(compurl = competition)
	# Gets and deletes all teams associated with the competition
	team_list = Team.objects.filter(compid = comp_obj.compid)
	for i in team_list:
		i.delete()
	# Gets and deletes all services associated with the competition
	serv_list = Service.objects.filter(compid = comp_obj.compid)
	for i in serv_list:
		i.delete()
	# Gets and deletes all inject responses associated with the competition (TODO: This doesn't delete any uploaded files associated with the response)
	resp_list = InjectResponse.objects.filter(compid = comp_obj.compid)
	for i in resp_list:
		i.delete()
	# Gets and deletes all injects associated with the competition
	ijct_list = Inject.objects.filter(compid = comp_obj.compid)
	for i in ijct_list:
		i.delete()
	# Gets and deletes all scores associated with the competition
	scor_list = Score.objects.filter(compid = comp_obj.compid)
	for i in scor_list:
		i.delete()
	# Deletes the competition itself
	comp_obj.delete()
	return HttpResponseRedirect("/admin/competitions/")

def servicemodule_list(request):
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["module_list"] = []
	for i in ServiceModule.objects.all():
		c["module_list"].append({
			"module": i,
			"file": Document.objects.get(servicemodule = i)
		})
	return render_to_response('AdminConfig/servicemodule_list.html', c)

def servicemodule_create(request):
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	if request.method != "POST":
		c.update(csrf(request))
		c["action"] = "create"
		c["form"] = CreateServiceModuleForm()
		return render_to_response('AdminConfig/servicemodule_create-edit.html', c)
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
		return render_to_response('AdminConfig/servicemodule_create-edit.html', c)
	return HttpResponseRedirect('/admin/servicemodules/')

def servicemodule_delete(request, servmdulid = None):
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	servmdul_obj = ServiceModule.objects.get(servmdulid = servmdulid)
	servmdul_obj.delete()
	return HttpResponseRedirect("/admin/servicemodules/")

def servicemodule_edit(request, servmdulid = None):
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
		return render_to_response('AdminConfig/servicemodule_create-edit.html', c)
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
		return render_to_response('AdminConfig/servicemodule_create-edit.html', c)

def servicemodule_test(request, servmdulid = None):
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c.update(csrf(request))
	c['servmdul_obj'] = ServiceModule.objects.get(servmdulid = servmdulid)
	serv_obj = Service(servicemodule = c['servmdul_obj'])
	if request.method != "POST":
		# Serve blank form with no results
		c["service_configs"] = buildServiceConfigForm(serv_obj, TestServiceForm())
		return render_to_response('AdminConfig/servicemodule_test.html', c)
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
	return render_to_response('AdminConfig/servicemodule_test.html', c)

def users_list(request):
	"""
	Displays site or competition administrative users
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	return render_to_response('AdminConfig/users_list.html', c)

def users_edit(request):
	"""
	Edit a site or competition administrative user
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	return render_to_response('AdminConfig/users_edit.html', c)

def users_delete(request):
	"""
	Delete site or competition administrative users
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	return HttpResponseRedirect('/admin/users/')

def users_create(request):
	"""
	Create site or competition administrative users
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	return render_to_response('AdminConfig/users_create.html', c)

