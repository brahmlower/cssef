from WebInterface.settings import SCORING_ENGINE_API_URL
from urllib import urlencode
import urllib2
import json

def request(page):
	url = SCORING_ENGINE_API_URL + page
	return urllib2.urlopen(url)

def delete(page):
	url = SCORING_ENGINE_API_URL + page
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	request = urllib2.Request(url, None)
	request.get_method = lambda: 'DELETE'
	return urllib2.urlopen(request)

def post(page, unencodedData):
	url = SCORING_ENGINE_API_URL + page
	data = urlencode(unencodedData)
	return urllib2.urlopen(url, data)

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