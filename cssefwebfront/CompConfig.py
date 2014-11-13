from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
from django.core.context_processors import csrf

from forms import CreateCompetitionForm
from forms import AdminLoginForm
from forms import CreateTeamForm
from forms import CreateInjectForm
from forms import CreateServiceForm
from models import Competition
from models import Service
from models import Inject
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

def list(request):
	"""
	Displays list of competitions, add and remove competition options
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_list"] = Competition.objects.all()
	return render_to_response('CompConfig/list.html', c)

def create(request, competition=None):
	"""
	Creates a new competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c["form"] = {'comp': CreateCompetitionForm()}
	# Checks if the user is submitting the form, or requesting the form
	if request.method != "POST":
		c.update(csrf(request))
		return render_to_response('CompConfig/create.html', c)
	form_comp = CreateCompetitionForm(request.POST)
	# Checks that submitted form data is valid
	if not form_comp.is_valid():
		c["messages"].new_error("Invalid field data in competition form.", 1003)
		return render(request, 'CompConfig/create.html', c)
	# Create the new competition
	comp = Competition(**form_comp.cleaned_data)
	comp.save()
	# Set success message and render page
	c["messages"].new_success("Created competition", 1337)
	return render_to_response('CompConfig/create.html', c)

# General competition configuration modules
def summary(request, competition = None):
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
		return render_to_response('CompConfig/summary.html', c)
	comp_obj = comp_obj[0]
	c["competition_object"] = comp_obj
	return render_to_response('CompConfig/summary.html', c)

def details(request, competition = None):
	"""
	Displays competitions details form
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	return render_to_response('CompConfig/details.html', c)

def scoring(request, competition = None):
	"""
	Displays competitions scoring methods form
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	return render_to_response('CompConfig/scoring.html', c)

# Team related configuration modules
def teams_list(request, competition = None):
	"""
	Lists the teams in the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c["teams"] = Team.objects.filter(compid = c["competition_object"].compid)
	return render_to_response('CompConfig/teams_list.html', c)

def teams_edit(request, competition = None):
	"""
	Edit the team in the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c["teams"] = Team.objects.filter(compid = c["competition_object"].compid)
	return render_to_response('CompConfig/teams_edit.html', c)

def teams_delete(request, competition = None, teamid = None):
	"""
	Delete the team from the competition
	"""
	comp_obj = Competition.objects.get(compurl = competition)
	team_obj = Team.objects.get(compid=comp_obj.compid, teamid=int(teamid))
	team_obj.delete()
	return HttpResponseRedirect("/admin/competitions/%s/teams/" % competition)

def teams_create(request, competition = None):
	"""
	Create the team in the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c["form"] = {"team": CreateTeamForm()}
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c.update(csrf(request))

	if request.method != "POST":
		return render_to_response('CompConfig/teams_create.html', c)
	form_dict = request.POST.copy()
	form_dict["compid"] = c["competition_object"].compid
	team = CreateTeamForm(form_dict)
	if not team.is_valid():
		c["messages"].new_info("Invalid field data in team form: %s" % team.errors, 1001)
		return render_to_response('CompConfig/teams_create.html', c)
	team.save()
	return HttpResponseRedirect("/admin/competitions/%s/teams/" % competition)

# Service related configuration modules
def services_list(request, competition = None):
	"""
	Lists the services in the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c["services"] = Service.objects.filter(compid = c["competition_object"].compid)
	return render_to_response('CompConfig/services_list.html', c)

def services_edit(request, competition = None, servid = None):
	"""
	Edits the service in the competitions
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c["services"] = Service.objects.filter(compid = c["competition_object"].compid)
	return render_to_response('CompConfig/services_edit.html', c)

def services_delete(request, competition = None, servid = None):
	"""
	Deletes the service from the competition
	"""
	comp_obj = Competition.objects.get(compurl = competition)
	serv_obj = Service.objects.get(compid = comp_obj.compid, servid = int(servid))
	serv_obj.delete()
	return HttpResponseRedirect("/admin/competitions/%s/services/" % competition)

def services_create(request, competition = None):
	"""
	Create services in the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c["form"] = {"service": CreateServiceForm()}
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c.update(csrf(request))

	if request.method != "POST":
		return render_to_response('CompConfig/services_create.html', c)
	form_dict = request.POST.copy()
	form_dict["compid"] = c["competition_object"].compid
	service = CreateServiceForm(form_dict)
	if not service.is_valid():
		c["messages"].new_info("Invalid field data in service form: %s" % service.errors, 1001)
		return render_to_response('CompConfig/services_create.html', c)
	print "supposedly saving"
	service.save()
	return HttpResponseRedirect("/admin/competitions/%s/services/" % competition)

# Inject related configuration modules
def injects_list(request, competition = None):
	"""
	Lists the injects in the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c["injects"] = Inject.objects.filter(compid = c["competition_object"].compid)
	return render_to_response('CompConfig/injects_list.html', c)

def injects_edit(request, competition = None, ijctid = None):
	"""
	Edit the inject in the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c["injects"] = Inject.objects.filter(compid = c["competition_object"].compid)
	return render_to_response('CompConfig/injects_edit.html', c)

def injects_delete(request, competition = None, ijctid = None):
	"""
	Deletes the inject from the competition
	"""
	comp_obj = Competition.objects.get(compurl = competition)
	ijct_obj = Inject.objects.filter(compid = comp_obj.compid, ijctid = int(ijctid))
	ijct_obj.delete()
	return HttpResponseRedirect("/admin/competitions/%s/injects/" % competition)

def injects_create(request, competition = None):
	"""
	Create injects in the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c["form"] = {"inject": CreateInjectForm()}
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c.update(csrf(request))

	if request.method != "POST":
		return render_to_response('CompConfig/injects_create.html', c)
	form_dict = request.POST.copy()
	form_dict["compid"] = c["competition_object"].compid
	inject = CreateInjectForm(form_dict)
	if not inject.is_valid():
		c["messages"].new_info("Invalid field data in inject form: %s" % inject.errors, 1001)
		return render_to_response('CompConfig/injects_create.html', c)
	inject.save()
	return HttpResponseRedirect("/admin/competitions/%s/injects/" % competition)






