from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from django.core.context_processors import csrf
from django.core.files.uploadedfile import UploadedFile
from django.forms import NumberInput
from django.forms import TextInput
from django.utils import timezone
from WebInterface.forms import CreateInject
from WebInterface.forms import CreateTeam
from WebInterface.forms import CreateService
from WebInterface.forms import CompetitionSettings
from WebInterface import cssefApi
import json

def summary(request, organizationUrl, competitionUrl):
	context = {}
	context['organization'] = cssefApi.getOrganization(organizationUrl)
	context['competition'] = cssefApi.getCompetition(context['organization']['organizationId'], competitionUrl)
	return render_to_response('competition/summary.html', context)

def settings(request, organizationUrl, competitionUrl):
	context = RequestContext(request)
	organization = cssefApi.getOrganization(organizationUrl)
	competition = cssefApi.getCompetition(organization['organizationId'], competitionUrl)
	context.push({'organization': organization})
	context.push({'competition': competition})
	if not request.method == 'POST':
		context.push({'form': CompetitionSettings(initial = competition)})
		return render_to_response('competition/settings.html', context)
	formData = CompetitionSettings(request.POST)
	if not formData.is_valid():
		print formData.errors
		return render_to_response('competition/settings.html', context)
	formData.cleaned_data['competitionId'] = competition['competitionId']
	formData.cleaned_data['organization'] = organization['organizationId']
	response = cssefApi.post('competitions/%s.json' % competition['competitionId'], formData.cleaned_data)
	return HttpResponseRedirect('/organization/%s/competitions/%s/settings/' % (organization['url'], competition['url']))

def listTeams(request, organizationUrl, competitionUrl):
	context = RequestContext(request)
	context.push({'organization': cssefApi.getOrganization(organizationUrl)})
	context.push({'competition': cssefApi.getCompetition(context['organization']['organizationId'], competitionUrl)})
	context.push({'teams': cssefApi.getTeams(context['competition']['competitionId'])})
	return render_to_response('competition/listTeams.html', context)

def createEditTeam(request, organizationUrl, competitionUrl, teamId = None):
	context = RequestContext(request)
	organization = cssefApi.getOrganization(organizationUrl)
	competition = cssefApi.getCompetition(organization['organizationId'], competitionUrl)
	if not request.method == 'POST':
		context.push({'organization': organization})
		context.push({'competition': competition})
		context.push({'action': 'create'})
		context.push({'form': CreateTeam(competitionId = competition['competitionId'], teamId = teamId)})
		return render_to_response('competition/createEditTeam.html', context)
	formData = CreateTeam(request.POST)
	if not formData.is_valid():
		return render_to_response('competition/createEditTeam.html', context)
	formData.cleaned_data['competitionId'] = competition['competitionId']
	response = cssefApi.post('competitions/%s/teams.json' % competition['competitionId'], formData.cleaned_data)
	return HttpResponseRedirect('/organization/%s/competitions/%s/teams/' % (organization['url'], competition['url']))

def listServices(request, organizationUrl, competitionUrl):
	context = RequestContext(request)
	organization = cssefApi.getOrganization(organizationUrl)
	competition = cssefApi.getCompetition(organization['organizationId'], competitionUrl)
	context.push({'organization': organization})
	context.push({'competition': competition})
	context.push({'pluginsAvailable': len(cssefApi.get('plugins.json')) > 0})
	context.push({'services': cssefApi.getServices(competition['competitionId'])})
	return render_to_response('competition/listServices.html', context)

def createEditService(request, organizationUrl, competitionUrl, serviceId = None):
	context = RequestContext(request)
	organization = cssefApi.getOrganization(organizationUrl)
	competition = cssefApi.getCompetition(organization['organizationId'], competitionUrl)
	if not request.method == 'POST':
		context.push({'organization': organization})
		context.push({'competition': competition})
		context.push({'action': 'create'})
		context.push({'form': CreateService(competitionId = context['competition']['competitionId'], serviceId = serviceId)})
		return render_to_response('competition/createEditService.html', context)
	formData = CreateService(request.POST)
	if not formData.is_valid():
		return render_to_response('competition/createEditService.html', context)
	formData.cleaned_data['competitionId'] = competition['competitionId']
	response = cssefApi.post('competitions/%s/services.json' % competition['competitionId'], formData.cleaned_data)
	return HttpResponseRedirect('/organization/%s/competitions/%s/services/' % (organization['url'], competition['url']))

def listInjects(request, organizationUrl, competitionUrl):
	context = RequestContext(request)
	context.push({'organization': cssefApi.getOrganization(organizationUrl)})
	context.push({'competition': cssefApi.getCompetition(context['organization']['organizationId'], competitionUrl)})
	context.push({'injects': cssefApi.getInjects(context['competition']['competitionId'])})
	return render_to_response('competition/listInjects.html', context)

def createEditInject(request, organizationUrl, competitionUrl, injectId = None):
	context = RequestContext(request)
	organization = cssefApi.getOrganization(organizationUrl)
	competition = cssefApi.getCompetition(organization['organizationId'], competitionUrl)
	if not request.method == 'POST':
		context.push({'organization': organization})
		context.push({'competition': competition})
		context.push({'action': 'create'})
		context.push({'form': CreateInject(competitionId = context['competition']['competitionId'], injectId = injectId)})
		return render_to_response('competition/createEditInject.html', context)
	formData = CreateInject(request.POST)
	if not formData.is_valid():
		return render_to_response('competition/createEditInject.html', context)
	formData.cleaned_data['competitionId'] = competition['competitionId']
	response = cssefApi.post('competitions/%s/injects.json' % competition['competitionId'], formData.cleaned_data)
	return HttpResponseRedirect('/organization/%s/competitions/%s/injects/' % (organization['url'], competition['url']))
