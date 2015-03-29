from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.core.files.uploadedfile import UploadedFile
from django.forms import NumberInput
from django.forms import TextInput
from forms import AdminLoginForm
from forms import CreateTeamForm
from forms import CreateInjectForm
from forms import CreateServiceForm
from forms import CompetitionSettingsGeneralForm
from forms import CompetitionSettingsScoringForm
from forms import CompetitionSettingsServiceForm
from forms import CompetitionSettingsTeamForm
from models import InjectResponse
from models import Competition
from models import ServiceModule
from models import Service
from models import Inject
from models import Score
from models import Team
from models import Document
from utils import UserMessages
from utils import getAuthValues
from utils import buildTeamServiceConfigDict
from utils import buildTeamServiceConfigForms
from utils import buildTeamServiceDependencyList
from utils import save_document
from django.utils import timezone
from cssefwebfront.tasks import run_comp
import settings
import json
from settings import logger

API_URL="http://127.0.0.1/api/v1/"

# General competition configuration modules
def summary(request, organization, competition):
	"""
	Displays general competitions configurations form
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	current_url = request.build_absolute_uri()
	if request.build_absolute_uri()[-8:] != "summary/":
		return HttpResponseRedirect(current_url + "summary/")
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	return render_to_response('CompConfig/summary.html', c)

def settings(request, organization, competition):
	"""
	Displays competitions details form
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c.update(csrf(request))
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	form_initial = Competition.objects.filter(compid = c['comp_obj'].compid).values()[0]
	c["forms"] = {
		"general_settings": CompetitionSettingsGeneralForm(initial = form_initial),
		"scoring_settings": CompetitionSettingsScoringForm(initial = form_initial),
		"service_settings": CompetitionSettingsServiceForm(initial = form_initial),
		"team_settings": CompetitionSettingsTeamForm(initial = form_initial)
	}
	if request.POST:
		forms_list = [	CompetitionSettingsGeneralForm,
						CompetitionSettingsScoringForm,
						CompetitionSettingsServiceForm,
						CompetitionSettingsTeamForm]
		f = forms_list[int(request.POST['form_num'])](request.POST)
		if f.is_valid():
			comp_obj = Competition.objects.filter(compid = c['comp_obj'].compid)
			clean_copy = f.cleaned_data
			for i in clean_copy:
				if clean_copy[i] == u'':
					clean_copy[i] = None
			comp_obj.update(**clean_copy)
			# Schedules the job to start the scoring engine
			#sec_until_start = (comp_obj[0].datetime_start - timezone.now()).seconds
			#result = run_comp.apply_async((comp_obj[0].compid,), countdown = int(sec_until_start))
			#logger.debug('Scheduled competition: Seconds until start: %s, Event UUID: %s' % (str(sec_until_start), str(result.id)))
		else:
			logger.error("is not valid")
		return HttpResponseRedirect('/admin/competitions/%s/settings/' % c["comp_obj"].compurl)
	return render_to_response('CompConfig/settings.html', c)

# Team related configuration modules
def listTeams(request, organization, competition):
	"""
	Lists the teams in the competition
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	c["teams"] = Team.objects.filter(compid = c["comp_obj"].compid)
	return render_to_response('CompConfig/teams_list.html', c)

def editTeam(request, organization, competition, teamId = None):
	"""
	Edit the team in the competition
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["action"] = "edit"
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	c.update(csrf(request))
	if request.method != "POST":
		team_obj = Team.objects.filter(compid = c["comp_obj"].compid, teamId = int(teamId))
		c["teamId"] = team_obj[0].teamId
		c["form"] = CreateTeamForm(initial = team_obj.values()[0])
		c["service_configs_list"] = buildTeamServiceConfigForms(c["comp_obj"].compid, team_obj[0].score_configs)
		return render_to_response('CompConfig/teams_create-edit.html', c)
	form_dict = request.POST.copy().dict()
	form_dict.pop('csrfmiddlewaretoken', None)
	form_dict["compid"] = c["comp_obj"].compid
	form_dict["score_configs"] = buildTeamServiceConfigDict(c["comp_obj"].compid, form_dict)
	# Clean network address
	if form_dict['networkaddr'][-1] == ".":
		form_dict['networkaddr'] = form_dict['networkaddr'][:-1]
	if form_dict['networkaddr'][0] == ".":
		form_dict['networkaddr'] = form_dict['networkaddr'][1:]
	team_obj = Team.objects.filter(compid = c["comp_obj"].compid, teamId = int(teamId))
	team_obj.update(**form_dict)
	return HttpResponseRedirect('/admin/competitions/%s/teams/' % competition)

def deleteTeam(request, organization, competition, teamId = None):
	"""
	Delete the team from the competition
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	comp_obj = Competition.objects.get(compurl = competition)
	team_obj = Team.objects.get(compid=comp_obj.compid, teamId=int(teamId))
	team_obj.delete()
	return HttpResponseRedirect("/admin/competitions/%s/teams/" % competition)

def createTeam(request, organization, competition):
	"""
	Create the team in the competition
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["action"] = "create"
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	c.update(csrf(request))
	if request.method != "POST":
		c['form'] = buildTeamServiceConfigForms(c["comp_obj"].compid, CreateTeamForm())
		c["depend_list"] = buildTeamServiceDependencyList(c["comp_obj"].compid)
		return render_to_response('CompConfig/teams_create-edit.html', c)
	form_dict = request.POST.copy()
	form_dict["compid"] = c["comp_obj"].compid
	form_dict["score_configs"] = buildTeamServiceConfigDict(c["comp_obj"].compid, form_dict)
	# Clean network address
	if form_dict['networkaddr'][-1] == ".":
		form_dict['networkaddr'] = form_dict['networkaddr'][:-1]
	if form_dict['networkaddr'][0] == ".":
		form_dict['networkaddr'] = form_dict['networkaddr'][1:]
	team = CreateTeamForm(form_dict)
	if not team.is_valid():
		c['form'] = buildTeamServiceConfigForms(c["comp_obj"].compid, CreateTeamForm(), form_dict)
		return render_to_response('CompConfig/teams_create-edit.html', c)
	team.save()
	return HttpResponseRedirect("/admin/competitions/%s/teams/" % competition)

# Service related configuration modules
def listServices(request, organization, competition):
	"""
	Lists the services in the competition
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	c["service_list"] = Service.objects.filter(compid = c["comp_obj"].compid)
	c["available_modules"] = bool(len(ServiceModule.objects.all()))
	return render_to_response('CompConfig/services_list.html', c)

def editService(request, organization, competition, serviceId = None):
	"""
	Edits the service in the competitions
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["action"] = "edit"
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	c.update(csrf(request))
	if request.method != "POST":
		serv_obj = Service.objects.filter(compid = c["comp_obj"].compid, serviceId = int(serviceId))
		c["serviceId"] = serv_obj[0].serviceId
		initial_dict = serv_obj.values()[0]
		initial_dict["connectip"] = int(initial_dict["connectip"])
		initial_dict["servicemodule"] = serv_obj[0].servicemodule.servmdulid
		c["form"] = CreateServiceForm(initial = initial_dict)
		return render_to_response('CompConfig/services_create-edit.html', c)
	# TODO: This part is super gross. I should improve efficiency at some point
	form_dict = request.POST.copy().dict()
	form_dict.pop('csrfmiddlewaretoken', None)
	# Set network connection display
	if int(form_dict["connectip"]) == 1:
		form_dict["connect_display"] = "IP Address"
		form_dict["connectip"] = True
	else:
		form_dict["connect_display"] = "Domain Name"
		form_dict["connectip"] = False
	# Clean machine address value
	if form_dict['networkloc'][0] == ".":
		form_dict['networkloc'] = form_dict['networkloc'][1:]
	if form_dict['networkloc'][-1] == ".":
		form_dict['networkloc'] = form_dict['networkloc'][:-1]
	serv_obj = Service.objects.filter(compid = c["comp_obj"].compid, serviceId = int(serviceId))
	serv_obj.update(**form_dict)
	return HttpResponseRedirect('/admin/competitions/%s/services/' % competition)

def deleteService(request, organization, competition, serviceId = None):
	"""
	Deletes the service from the competition
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	comp_obj = Competition.objects.get(compurl = competition)
	serv_obj = Service.objects.get(compid = comp_obj.compid, serviceId = int(serviceId))
	serv_obj.delete()
	return HttpResponseRedirect("/admin/competitions/%s/services/" % competition)

def createService(request, organization, competition):
	"""
	Create services in the competition
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	if not bool(len(ServiceModule.objects.all())):
		return HttpResponseRedirect("/admin/competitions/%s/services/" % c["comp_obj"].compurl)
	if request.method != "POST":
		# Serve empty form without acting on any data
		c.update(csrf(request))
		c["form"] = CreateServiceForm()
		c["action"] = "create"
		return render_to_response('CompConfig/services_create-edit.html', c)
	# Prepare post data for validation
	form_dict = request.POST.copy().dict()
	serv_form = CreateServiceForm(form_dict)
	if not serv_form.is_valid():
		print serv_form.errors
		return render_to_response('CompConfig/services_create-edit.html', c)
	# Now prepare post data for service object instantiation
	form_dict.pop('csrfmiddlewaretoken', None)
	form_dict["compid"] = c["comp_obj"].compid
	form_dict["servicemodule"] = ServiceModule.objects.get(servmdulid = form_dict["servicemodule"])
	# Set network connection display
	if int(form_dict["connectip"]) == 1:
		form_dict['connectip'] = True
		form_dict["connect_display"] = "IP Address"
	else:
		form_dict['connectip'] = False
		form_dict["connect_display"] = "Domain Name"
	# Clean machine address value
	if form_dict['connectip'] and form_dict['networkloc'][0] == ".":
		form_dict['networkloc'] = form_dict['networkloc'][1:]
	elif not form_dict['connectip'] and form_dict['networkloc'][-1] == ".":
		form_dict['networkloc'] = form_dict['networkloc'][:-1]
	serv_obj = Service(**form_dict)
	serv_obj.save()
	return HttpResponseRedirect("/admin/competitions/%s/services/" % competition)

# Inject related configuration modules
def listInjects(request, organization, competition):
	"""
	Lists the injects in the competition
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	c["inject_list"] = []
	for i in Inject.objects.filter(compid = c["comp_obj"].compid):
		c["inject_list"].append({
			"inject": i,
			"files": Document.objects.filter(inject = i)
		})
	return render_to_response('CompConfig/injects_list.html', c)

def editInject(request, organization, competition, injectId = None):
	"""
	Edit the inject in the competition
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["action"] = "edit"
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	c.update(csrf(request))
	if request.method != "POST":
		# Have to use filter here, otherwise we get 'Inject object is not iterable' errors
		ijct_obj = Inject.objects.filter(compid = c["comp_obj"].compid, injectId = int(injectId))
		c["injectId"] = ijct_obj[0].injectId
		c["form"] = CreateInjectForm(initial = ijct_obj.values()[0])
		return render_to_response('CompConfig/injects_create-edit.html', c)
	# Note this will only work when there are no lists
	form_dict = request.POST.copy().dict()
	form_dict.pop('csrfmiddlewaretoken', None)
	form_dict.pop('docfile', None)
	if 'require_response' in form_dict:
		form_dict['require_response'] = True
	else:
		form_dict['require_response'] = False
		form_dict['dt_response_due'] = None
		form_dict['dt_response_close'] = None
	ijct_obj = Inject.objects.filter(compid = c["comp_obj"].compid, injectId = int(injectId))
	ijct_obj.update(**form_dict)
	# Was there a file? If so, save it!
	if 'docfile' in request.FILES:
		save_document(request.FILES['docfile'], settings.CONTENT_INJECT_PATH, ijct_obj)
	return HttpResponseRedirect('/admin/competitions/%s/injects/' % competition)

def deleteInject(request, organization, competition, injectId = None):
	"""
	Deletes the inject from the competition
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	comp_obj = Competition.objects.get(compurl = competition)
	# Delete any responses to the inject (TODO: this doesn't delete uploaded files)
	response_objs = InjectResponse.objects.filter(compid = comp_obj.compid, injectId = int(injectId))
	for i in response_objs:
		i.delete()
	# Deletes the inject itself
	ijct_obj = Inject.objects.filter(compid = comp_obj.compid, injectId = int(injectId))
	ijct_obj.delete()
	return HttpResponseRedirect("/admin/competitions/%s/injects/" % competition)

def createInject(request, organization, competition):
	"""
	Create injects in the competition
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["action"] = "create"
	c["comp_obj"] = Competition.objects.get(compurl = competition)
	c.update(csrf(request))
	# Just displays the form if we're not handling any input
	if request.method != "POST":
		c["form"] = CreateInjectForm()
		return render_to_response('CompConfig/injects_create-edit.html', c)
	form_dict = request.POST.copy().dict()
	form_dict["compid"] = c["comp_obj"].compid
	form_dict.pop('csrfmiddlewaretoken', None)
	form_dict.pop('docfile', None)
	if 'require_response' in form_dict:
		form_dict['require_response'] = True
	else:
		form_dict['require_response'] = False
		form_dict['dt_response_due'] = None
		form_dict['dt_response_close'] = None
	form_obj = CreateInjectForm(form_dict)
	if not form_obj.is_valid():
		#c["messages"].new_info("Invalid field data in inject form: %s" % form_obj.errors, 1001)
		return render_to_response('CompConfig/injects_create-edit.html', c)
	# Start saving the inject!
	print form_dict
	ijct_obj = Inject(**form_dict)
	ijct_obj.save()
	# Was there a file? If so, save it!
	if 'docfile' in request.FILES:
		save_document(request.FILES['docfile'], settings.CONTENT_INJECT_PATH, ijct_obj)
	return HttpResponseRedirect("/admin/competitions/%s/injects/" % competition)
