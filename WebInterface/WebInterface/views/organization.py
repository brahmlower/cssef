from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
from django.core.context_processors import csrf
from WebInterface.forms import LoginOrganizationUser
from WebInterface.forms import CreateCompetition
from WebInterface.settings import SCORING_ENGINE_API_URL
from WebInterface import cssefApi


def login(request):
	context = {}
	context["form"] = LoginOrganizationUser()
	context.update(csrf(request))
	# Checks if the user is submitting the form, or requesting the form
	if request.method != "POST":
		return render_to_response('organization/login.html', context)
	username = request.POST.get('username')
	password = request.POST.get('password')
	# TODO: The following line can throw a MultiValueDictKeyError
	admin = auth.authenticate(username = username, password = password)
	if admin == None:
		return render_to_response('organization/login.html', context)
	# Checks that the submitted form data is valid
	auth.login(request, admin)
	organizationName = 'testingorg'
	return HttpResponseRedirect("/organization/%s/home" % organizationName)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/")

def home(request, organizationUrl):
	context = {}
	context['organization'] = cssefApi.getOrganization(organizationUrl)
	return render_to_response('organization/home.html', context)

def members(request, organizationUrl):
	context = {}
	context['organization'] = cssefApi.getOrganization(organizationUrl)
	context['members'] = []
	users = cssefApi.get('users.json')
	members = []
	for i in users:
		if i['organization'] == context['organization']['organizationId']:
			context['members'].append(i)
	return render_to_response('organization/members.html', context)

def listCompetitions(request, organizationUrl):
	context = {}
	context['competitions'] = []
	context['organization'] = cssefApi.getOrganization(organizationUrl)
	for i in cssefApi.get('competitions.json'):
		if i['organization'] == context['organization']['organizationId']:
			context['competitions'].append(i)
	return render_to_response('organization/listCompetitions.html', context)

def createCompetition(request, organizationUrl, competition=None):
	context = {}
	context.update(csrf(request))
	context['organization'] = cssefApi.getOrganization(organizationUrl)
	context["form"] = CreateCompetition()
	if request.method != "POST":
		return render_to_response('organization/createCompetition.html', context)
	formData = CreateCompetition(request.POST)
	if not formData.is_valid():
		return render_to_response('organization/createCompetition.html', context)
	formData.cleaned_data['organization'] = context['organization']['organizationId']
	response = cssefApi.post('competitions.json', formData.cleaned_data)
	return HttpResponseRedirect('/organization/%s/competitions/' % context['organization']['url'])

def settings(request, organizationUrl):
	context = {}
	context['organization'] = cssefApi.getOrganization(organizationUrl)
	return render_to_response('organization/settings.html', context)
