from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
from django.core.context_processors import csrf
#from forms import CompetitionSettingsGeneralForm
#from forms import AdminLoginForm
#from forms import CreateTeamForm
#from forms import TestServiceForm
#from forms import CreateServiceForm
#from forms import CreateServiceModuleForm
from WebInterface.settings import SCORING_ENGINE_API_URL
from urllib2 import urlopen
import json

def home(request, organization):
	context = {}
	context['organization'] = organization
	return render_to_response('organization/home.html', context)

def members(request, organization):
	context = {}
	context['organization'] = organization
	return render_to_response('organization/members.html', context)

def listCompetitions(request, organization):
	"""
	Displays list of competitions, add and remove competition options
	"""
	queryUrl = SCORING_ENGINE_API_URL + "competitions.json"
	jsonString = urlopen(queryUrl).read()
	competitions = json.loads(jsonString)
	context = {}
	context['competitions'] = competitions
	context['organization'] = organization
	return render_to_response('organization/listCompetitions.html', context)

def createCompetition(request, organization, competition=None):
	"""
	Creates a new competition
	"""
	# Checks if the user is submitting the form, or requesting the form
	if request.method != "POST":
		context = {}
		context['organization'] = organization
		context.update(csrf(request))
		#c["form"] = CompetitionSettingsGeneralForm()
		return render_to_response('organization/createCompetition.html', context)
	#form_comp = CompetitionSettingsGeneralForm(request.POST)
	# Checks that submitted form data is valid
	if not form_comp.is_valid():
		print form_comp.errors
		return render(request, 'organization/createCompetition.html', context)
	# Create the new competition
	#Competition(**form_comp.cleaned_data).save()
	return HttpResponseRedirect('/admin/competitions/')

def settings(request, organization):
	context = {}
	context['organization'] = organization
	return render_to_response('organization/settings.html', context)
