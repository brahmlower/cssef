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
from utils import buildServiceDependencyList
import settings

def listCompetitions(request):
	"""
	Displays list of competitions, add and remove competition options
	"""
	c = getAuthValues(request, {})
	if c["auth_name"] != "auth_team_white":
		return HttpResponseRedirect("/")
	c["competition_list"] = Competition.objects.all()
	return render_to_response('AdminConfig/competition_list.html', c)

def createCompetition(request, competition=None):
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

def deleteCompetition(request, competition = None):
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





