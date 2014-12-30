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
from models import Score
from models import Team

from utils import UserMessages
from utils import getAuthValues
from utils import add_teams_scoreconfigs
from utils import clean_teams_scoreconfigs

# General competition configuration modules
def summary(request, competition = None):
	"""
	Displays general competitions configurations form
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	current_url = request.build_absolute_uri()
	if request.build_absolute_uri()[-8:] != "summary/":
		return HttpResponseRedirect(current_url + "summary/")
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
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["competition_object"] = Competition.objects.get(compurl = competition)
	return render_to_response('CompConfig/details.html', c)

def scoring(request, competition = None):
	"""
	Displays competitions scoring methods form
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["competition_object"] = Competition.objects.get(compurl = competition)
	return render_to_response('CompConfig/scoring.html', c)

# Team related configuration modules
def teams_list(request, competition = None):
	"""
	Lists the teams in the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c["teams"] = Team.objects.filter(compid = c["competition_object"].compid)
	return render_to_response('CompConfig/teams_list.html', c)

def teams_edit(request, competition = None, teamid = None):
	"""
	Edit the team in the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["action"] = "edit"
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c.update(csrf(request))
	if request.method != "POST":
		team_obj = Team.objects.filter(compid = c["competition_object"].compid, teamid = int(teamid))
		c["teamid"] = team_obj[0].teamid
		c["form"] = {"team": CreateTeamForm(initial = team_obj.values()[0])}
		return render_to_response('CompConfig/teams_create-edit.html', c)
	# TODO: This part is super gross. I should improve efficiency at some point
	tmp_dict = {}
	tmp_dict['teamname'] = request.POST['teamname']
	tmp_dict['password'] = request.POST['password']
	tmp_dict['domainname'] = request.POST['domainname']
	tmp_dict['score_configs'] = request.POST['score_configs']
	team_obj = Team.objects.filter(compid = c["competition_object"].compid, teamid = int(teamid))
	team_obj.update(**tmp_dict)
	return HttpResponseRedirect('/admin/competitions/%s/teams/' % competition)

def teams_delete(request, competition = None, teamid = None):
	"""
	Delete the team from the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
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
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["action"] = "create"
	c["form"] = {"team": CreateTeamForm()}
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c.update(csrf(request))

	if request.method != "POST":
		return render_to_response('CompConfig/teams_create-edit.html', c)
	form_dict = request.POST.copy()
	form_dict["compid"] = c["competition_object"].compid
	team = CreateTeamForm(form_dict)
	if not team.is_valid():
		c["messages"].new_info("Invalid field data in team form: %s" % team.errors, 1001)
		return render_to_response('CompConfig/teams_create-edit.html', c)
	team.save()
	add_teams_scoreconfigs(c["competition_object"].compid)
	return HttpResponseRedirect("/admin/competitions/%s/teams/" % competition)

# Service related configuration modules
def services_list(request, competition = None):
	"""
	Lists the services in the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c["services"] = Service.objects.filter(compid = c["competition_object"].compid)
	return render_to_response('CompConfig/services_list.html', c)

def services_edit(request, competition = None, servid = None):
	"""
	Edits the service in the competitions
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["action"] = "edit"
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c.update(csrf(request))
	if request.method != "POST":
		serv_obj = Service.objects.filter(compid = c["competition_object"].compid, servid = int(servid))
		c["servid"] = serv_obj[0].servid
		c["form"] = {"service": CreateServiceForm(initial = serv_obj.values()[0])}
		return render_to_response('CompConfig/services_create-edit.html', c)
	# TODO: This part is super gross. I should improve efficiency at some point
	tmp_dict = {}
	tmp_dict['module'] = request.POST['module']
	tmp_dict['name'] = request.POST['name']
	tmp_dict['desc'] = request.POST['desc']
	tmp_dict['points'] = request.POST['points']
	tmp_dict['config'] = request.POST['config']
	tmp_dict['subdomain'] = request.POST['subdomain']
	serv_obj = Service.objects.filter(compid = c["competition_object"].compid, servid = int(servid))
	serv_obj.update(**tmp_dict)
	return HttpResponseRedirect('/admin/competitions/%s/services/' % competition)

def services_delete(request, competition = None, servid = None):
	"""
	Deletes the service from the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	comp_obj = Competition.objects.get(compurl = competition)
	serv_obj = Service.objects.get(compid = comp_obj.compid, servid = int(servid))
	clean_teams_scoreconfigs(comp_obj.compid, serv_obj.module)
	serv_obj.delete()
	return HttpResponseRedirect("/admin/competitions/%s/services/" % competition)

def services_create(request, competition = None):
	"""
	Create services in the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["form"] = {"service": CreateServiceForm()}
	c["action"] = "create"
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c.update(csrf(request))

	if request.method != "POST":
		return render_to_response('CompConfig/services_create-edit.html', c)
	form_dict = request.POST.copy()
	form_dict["compid"] = c["competition_object"].compid
	service = CreateServiceForm(form_dict)
	if not service.is_valid():
		c["messages"].new_info("Invalid field data in service form: %s" % service.errors, 1001)
		return render_to_response('CompConfig/services_create-edit.html', c)
	service.save()
	add_teams_scoreconfigs(c["competition_object"].compid)
	return HttpResponseRedirect("/admin/competitions/%s/services/" % competition)

# Inject related configuration modules
def injects_list(request, competition = None):
	"""
	Lists the injects in the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c["injects"] = Inject.objects.filter(compid = c["competition_object"].compid)
	return render_to_response('CompConfig/injects_list.html', c)

def injects_edit(request, competition = None, ijctid = None):
	"""
	Edit the inject in the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["action"] = "edit"
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c.update(csrf(request))
	if request.method != "POST":
		ijct_obj = Inject.objects.filter(compid = c["competition_object"].compid, ijctid = int(ijctid))
		c["ijctid"] = ijct_obj[0].ijctid
		c["form"] = {"inject": CreateInjectForm(initial = ijct_obj.values()[0])}
		return render_to_response('CompConfig/injects_create-edit.html', c)
	# Note this will only work when there are no lists
	tmp_dict = request.POST.copy().dict()
	tmp_dict.pop('csrfmiddlewaretoken', None)
	ijct_obj = Inject.objects.filter(compid = c["competition_object"].compid, ijctid = int(ijctid))
	ijct_obj.update(**tmp_dict)
	return HttpResponseRedirect('/admin/competitions/%s/injects/' % competition)

def injects_delete(request, competition = None, ijctid = None):
	"""
	Deletes the inject from the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	comp_obj = Competition.objects.get(compurl = competition)
	# Delete any responses to the inject (TODO: this doesn't delete uploaded files)
	response_objs = InjectResponse.objects.filter(compid = comp_obj.compid, ijctid = int(ijctid))
	for i in response_objs:
		i.delete()
	# Deletes the inject itself
	ijct_obj = Inject.objects.filter(compid = comp_obj.compid, ijctid = int(ijctid))
	ijct_obj.delete()
	return HttpResponseRedirect("/admin/competitions/%s/injects/" % competition)

def injects_create(request, competition = None):
	"""
	Create injects in the competition
	"""
	c = {}
	c["messages"] = UserMessages()
	c = getAuthValues(request, c)
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["action"] = "create"
	c["competition_object"] = Competition.objects.get(compurl = competition)
	c.update(csrf(request))
	# Just displays the form if we're not handling any input
	if request.method != "POST":
		c["form"] = {"inject": CreateInjectForm()}
		return render_to_response('CompConfig/injects_create-edit.html', c)
	form_dict = request.POST.copy()
	form_dict["compid"] = c["competition_object"].compid
	ijct_obj = CreateInjectForm(form_dict)
	if not ijct_obj.is_valid():
		c["messages"].new_info("Invalid field data in inject form: %s" % ijct_obj.errors, 1001)
		return render_to_response('CompConfig/injects_create-edit.html', c)
	ijct_obj.save()
	return HttpResponseRedirect("/admin/competitions/%s/injects/" % competition)
