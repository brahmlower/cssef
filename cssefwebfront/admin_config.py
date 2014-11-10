from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
from django.core.context_processors import csrf

from forms import CreateCompetitionForm
from forms import AdminLoginForm
from forms import CreateTeamForm
from forms import CreateServiceForm
from models import Competition
from models import Service
from models import Team

class UserMessages:
	def __init__(self):
		self.info = []
		self.error = []
		self.success = []
	def new_info(self, string, num):
		self.info.append({"string":string, "num":num})

	def new_error(self, string, num):
		self.error.append({"string":string, "num":num})

	def new_success(self, string, num):
		self.success.append({"string":string, "num":num})

	def clear(self):
		self.info = []
		self.error = []
		self.success = []

def home(request):
	"""
	Page displayed after loggin in
	"""
	return render_to_response('admin_config/home.html')

def users(request):
	"""
	Displays users, add and remove user options
	"""
	return render_to_response('admin_config/users.html')

def teams(request, competition='None'):
	"""
	Edit/Create teams
	"""
	c = {}
	c["messages"] = UserMessages()
	c["form"] = {"team": CreateTeamForm()}
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c.update(csrf(request))

	if request.method != "POST":
		return render_to_response('admin_config/teams.html', c)
	form_dict = request.POST.copy()
	form_dict["compid"] = c["competition_object"].compid
	team = CreateTeamForm(form_dict)
	if not team.is_valid():
		c["messages"].new_info("Invalid field data in team form: %s" % team.errors, 1001)
		return render_to_response('admin_config/teams.html', c)
	team.save()
	return HttpResponseRedirect("/admin/competitions/%s/teams/" % competition)

def services(request, competition='None'):
	"""
	Edit/Create services
	"""
	c = {}
	c["messages"] = UserMessages()
	c["form"] = {"service": CreateServiceForm()}
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c.update(csrf(request))

	if request.method != "POST":
		return render_to_response('admin_config/services.html', c)
	form_dict = request.POST.copy()
	form_dict["compid"] = c["competition_object"].compid
	print form_dict
	service = CreateServiceForm(form_dict)
	if not service.is_valid():
		c["messages"].new_info("Invalid field data in service form: %s" % service.errors, 1001)
		return render_to_response('admin_config/services.html', c)
	print "supposedly saving"
	service.save()
	return HttpResponseRedirect("/admin/competitions/%s/services/" % competition)

def login(request):
	"""
	Page for admins to login to for competition management
	"""
	c = {}
	c["messages"] = UserMessages()
	c["form"] = {'team': AdminLoginForm()}
	# Checks if the user is submitting the form, or requesting the form
	if request.method != "POST":
		c.update(csrf(request))
		return render_to_response('admin_config/login.html', c)
	login = AdminLoginForm(request.POST)
	# Checks that the submitted form data is valid
	if not login.is_valid():
		c["messages"].new_error("Invalid field data in competition form.", 1003)
		return render(request, 'admin_config/login.html', c)

	return render_to_response('admin_config/home.html', c)

def comp_list(request):
	"""
	Displays list of competitions, add and remove competition options
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_list"] = Competition.objects.all()
	return render_to_response('admin_config/comp_list.html', c)

def comp_create(request, competition='None'):
	"""
	Creates a new competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c["form"] = {'comp': CreateCompetitionForm()}
	# Checks if the user is submitting the form, or requesting the form
	if request.method != "POST":
		c.update(csrf(request))
		return render_to_response('admin_config/create_competition.html', c)
	form_comp = CreateCompetitionForm(request.POST)
	# Checks that submitted form data is valid
	if not form_comp.is_valid():
		c["messages"].new_error("Invalid field data in competition form.", 1003)
		return render(request, 'admin_config/create_competition.html', c)
	# Create the new competition
	comp = Competition(**form_comp.cleaned_data)
	comp.save()
	# Set success message and render page
	c["messages"].new_success("Created competition", 1337)
	return render_to_response('admin_config/create_competition.html', c)

def comp_config_summary(request, competition='None'):
	"""
	Displays general competitions configurations form
	"""
	current_url = request.build_absolute_uri()
	if request.build_absolute_uri()[-8:] != "summary/":
		return HttpResponseRedirect(current_url + "summary/")
	c = {}
	c["messages"] = UserMessages()
	comp_obj = Competition.objects.filter(compurl = competition)
	if len(comp_obj) > 1:
		c["messages"].new_error("Multiple database entries for URLID: '%s'" % competition, 1234)
		return render_to_response('admin_config/comp_config_summary.html', c)
	comp_obj = comp_obj[0]
	c["competition_object"] = comp_obj
	return render_to_response('admin_config/comp_config_summary.html', c)

def comp_config_details(request, competition='None'):
	"""
	Displays competitions details form
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	return render_to_response('admin_config/comp_config_details.html', c)

def comp_config_injects(request, competition='None'):
	"""
	Displays competition injects form
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	return render_to_response('admin_config/comp_config_injects.html', c)

def comp_config_teams(request, competition='None'):
	"""
	Displays competition teams form
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c["teams"] = Team.objects.filter(compid = c["competition_object"].compid)
	return render_to_response('admin_config/comp_config_teams.html', c)

def comp_config_services(request, competition='None'):
	"""
	Displays competitions services form
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c["services"] = Service.objects.filter(compid = c["competition_object"].compid)
	return render_to_response('admin_config/comp_config_services.html', c)

def comp_config_service_delete(request, competition='None', servid='None'):
	"""
	Deletes the specified service
	"""
	comp_obj = Competition.objects.get(compurl = competition)
	serv_obj = Service.objects.get(compid = comp_obj.compid, servid = int(servid))
	serv_obj.delete()
	return HttpResponseRedirect("/admin/competitions/%s/services/" % competition)

def comp_config_scoring(request, competition='None'):
	"""
	Displays competitions scoring methods form
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	return render_to_response('admin_config/comp_config_scoring.html', c)
