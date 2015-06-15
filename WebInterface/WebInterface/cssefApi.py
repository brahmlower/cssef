from WebInterface.settings import SCORING_ENGINE_API_URL
from urllib import urlencode
import urllib2
import json
import requests

def request(page):
	url = SCORING_ENGINE_API_URL + page
	return urllib2.urlopen(url)

def delete(page):
	url = SCORING_ENGINE_API_URL + page
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	request = urllib2.Request(url, None)
	request.get_method = lambda: 'DELETE'
	return urllib2.urlopen(request)

def post(page, unencodedData, files = None):
	url = SCORING_ENGINE_API_URL + page
	if files:
		return requests.post(url, data = unencodedData, files=files)
	else:
		return requests.post(url, data = unencodedData)

def get(page):
	response = request(page)
	jsonString = response.read()
	return json.loads(jsonString)

def getOrganization(organizationUrl):
	# TODO: This should eventually use GET queries instead of searching the whole list
	results = get('organizations.json')
	for i in results:
		if i['url'] == organizationUrl:
			return i

def getCompetition(organizationId, competitionUrl):
	# TODO: This should eventually use GET queries instead of searching the whole list
	results = get('competitions.json')
	for i in results:
		if i['url'] == competitionUrl and i['organization'] == organizationId:
			return i

def getServices(competitionId):
	return get('competitions/%s/services.json' % competitionId)

def getTeams(competitionId):
	return get('competitions/%s/teams.json' % competitionId)

def getInjects(competitionId):
	return get('competitions/%s/injects.json' % competitionId)

def getPlugins():
	return get('plugins.json')

def getService(competitionId, serviceId):
	if serviceId:
		return get('competitions/%s/teams/%s.json' % (competitionId, serviceId))

def getTeam(competitionId, teamId):
	if teamId:
		return get('competitions/%s/teams/%s.json' % (competitionId, teamId))

def getInject(competitionId, injectId):
	if injectId:
		return get('competitions/%s/injects/%s.json' % (competitionId, injectId))

def getPlugin(pluginId):
	return get('plugins/%s.json' % pluginId)
