from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import authenticate
from django.core.context_processors import csrf

from forms import CreateCompetitionForm
from forms import AdminLoginForm
from forms import CreateTeamForm
from forms import CreateServiceForm
from models import Competition
from models import Service
from models import Team

from utils import UserMessages
from utils import getAuthValues

def home(request):
	"""
	Page displayed after loggin in
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
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

	#login = AdminLoginForm(request.POST)
	form_dict = request.POST.copy()
	admin = authenticate(username = form_dict["username"], password = form_dict["password"])
	if admin == None:
		c["messages"].new_info("Incorrect credentials.", 4321)
		return render_to_response('AdminConfig/login.html', c)
	# Checks that the submitted form data is valid
	auth.login(request, admin)
	return HttpResponseRedirect("/admin/home") #render_to_response('AdminConfig/home.html', c)

def logout(request):
	"""
	Page for teams to logout of a competition
	"""
	auth.logout(request)
	c = {}
	c["messages"] = UserMessages()
	return HttpResponseRedirect("/")

def site_config(request):
	"""
	Displays configuration options for the overall site
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	return render_to_response('AdminConfig/home.html', c)

def comp_list(request):
	"""
	Displays list of competitions, add and remove competition options
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["competition_list"] = Competition.objects.all()
	return render_to_response('AdminConfig/list.html', c)

def comp_create(request, competition=None):
	"""
	Creates a new competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["form"] = {'comp': CreateCompetitionForm()}
	# Checks if the user is submitting the form, or requesting the form
	if request.method != "POST":
		c.update(csrf(request))
		return render_to_response('AdminConfig/create.html', c)
	form_comp = CreateCompetitionForm(request.POST)
	# Checks that submitted form data is valid
	if not form_comp.is_valid():
		c["messages"].new_error("Invalid field data in competition form.", 1003)
		return render(request, 'AdminConfig/create.html', c)
	# Create the new competition
	comp = Competition(**form_comp.cleaned_data)
	comp.save()
	# Set success message and render page
	c["messages"].new_success("Created competition", 1337)
	#return render_to_response('AdminConfig/create.html', c)
	return HttpResponseRedirect('/admin/competitions/')

def comp_delete(request, competition = None):
	"""
	Delete the competition and all related objects (teams, scores, injects, services)
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
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

def users_list(request):
	"""
	Displays site or competition administrative users
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	return render_to_response('AdminConfig/users_list.html', c)

def users_edit(request):
	"""
	Edit a site or competition administrative user
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	return render_to_response('AdminConfig/users_edit.html', c)

def users_delete(request):
	"""
	Delete site or competition administrative users
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	return HttpResponseRedirect('/admin/users/')

def users_create(request):
	"""
	Create site or competition administrative users
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	return render_to_response('AdminConfig/users_create.html', c)

