from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib import auth
from django.core.context_processors import csrf
from WebInterface.forms import LoginOrganizationUser
from WebInterface.forms import CreateCompetition
from WebInterface.settings import SCORING_ENGINE_API_URL
from urllib import urlencode
import urllib2
import json


def apiPost(page, unencodedData):
	url = SCORING_ENGINE_API_URL + page
	data = urlencode(unencodedData)
	return urllib2.urlopen(url, data)

def apiGet(page):
	url = SCORING_ENGINE_API_URL + page
	return urllib2.urlopen(url)

def apiQuery(page):
	response = apiGet(page)
	jsonString = response.read()
	return json.loads(jsonString)

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

def getOrganization(organizationUrl):
	# TODO: This should eventually use GET queries instead of searching the whole list
	results = apiQuery('organizations.json')
	for i in results:
		if i['url'] == organizationUrl:
			return i

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/")

def home(request, organizationUrl):
	context = {}
	context['organization'] = getOrganization(organizationUrl)
	return render_to_response('organization/home.html', context)

def members(request, organizationUrl):
	context = {}
	context['organization'] = getOrganization(organizationUrl)
	context['members'] = []
	users = apiQuery('users.json')
	members = []
	for i in users:
		if i['organization'] == context['organization']['organizationId']:
			context['members'].append(i)
	return render_to_response('organization/members.html', context)

def listCompetitions(request, organizationUrl):
	"""
	Displays list of competitions, add and remove competition options
	"""
	queryUrl = SCORING_ENGINE_API_URL + "competitions.json"
	jsonString = urllib2.urlopen(queryUrl).read()
	competitions = json.loads(jsonString)
	context = {}
	context['competitions'] = []
	context['organization'] = getOrganization(organizationUrl)
	for i in apiQuery('competitions.json'):
		if i['organization'] == context['organization']['organizationId']:
			context['competitions'].append(i)
	return render_to_response('organization/listCompetitions.html', context)

def createCompetition(request, organizationUrl, competition=None):
	"""
	Creates a new competition
	"""
	context = {}
	context.update(csrf(request))
	context['organization'] = getOrganization(organizationUrl)
	context["form"] = CreateCompetition()
	if request.method != "POST":
		return render_to_response('organization/createCompetition.html', context)
	formData = CreateCompetition(request.POST)
	if not formData.is_valid():
		return render_to_response('organization/createCompetition.html', context)
	formData.cleaned_data['organization'] = context['organization']['organizationId']
	response = apiPost('competitions.json', formData.cleaned_data)
	return HttpResponseRedirect('/organization/%s/competitions/' % context['organization']['url'])

def settings(request, organizationUrl):
	context = {}
	context['organization'] = getOrganization(organizationUrl)
	return render_to_response('organization/settings.html', context)
