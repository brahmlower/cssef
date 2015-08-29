from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.test import Client
import json
import exampleData

# def createObject(instance, uri, examplePostData, **kwargs):
# 	uri = kwargs.pop('uri', None)
# 	if not uri:
# 		uri = '/organizations.json'
# 	postData = exampleData.organization
# 	postData.update(kwargs)
# 	response = post(instance, uri, postData)
# 	return json.loads(response.content)

# def createUser(instance, **kwargs):
# 	uri = kwargs.pop('uri', None)
# 	if not uri:
# 		uri = '/organizations.json'
# 	return createObject(instance, uri, exampleData, **kwargs)

def createUser(instance, **kwargs):
	uri = kwargs.pop('uri', None)
	status_code = kwargs.pop('status_code', None)
	if not uri:
		uri = '/organizations/%s/members.json' % kwargs.get('organizationId', '')
	postData = exampleData.user
	postData.update(kwargs)
	if status_code:
		response = post(instance, uri, postData, status_code = status_code)
	else:
		response = post(instance, uri, postData)
	return json.loads(response.content)

def createOrganization(instance, **kwargs):
	uri = kwargs.pop('uri', None)
	status_code = kwargs.pop('status_code', None)
	if not uri:
		uri = '/organizations.json'
	postData = exampleData.organization
	postData.update(kwargs)
	if status_code:
		response = post(instance, uri, postData, status_code = status_code)
	else:
		response = post(instance, uri, postData)
	return json.loads(response.content)

def createCompetition(instance, **kwargs):
	uri = kwargs.pop('uri', None)
	status_code = kwargs.pop('status_code', None)
	if not uri:
		uri = '/organizations/%s/competitions.json' % kwargs.get('organization', '')
	postData = exampleData.competitionMin
	postData.update(kwargs)
	if status_code:
		response = post(instance, uri, postData, status_code = status_code)
	else:
		response = post(instance, uri, postData)
	return json.loads(response.content)

def createInject(instance, **kwargs):
	uri = kwargs.pop('uri', None)
	if not uri:
		uri = '/competitions/%s/injects.json' % kwargs.get('competitionId', '1')#str(competitionId)
	postData = exampleData.inject
	postData.update(kwargs)
	response = post(instance, uri, postData)
	return json.loads(response.content)

def createInjectResponse(instance, **kwargs):
	uri = kwargs.pop('uri', None)
	if not uri:
		uri = '/competitions/%s/injectresponses.json' % kwargs.get('competitionId', '1')#str(competitionId)
	postData = exampleData.injectResponse
	postData.update(kwargs)
	response = post(instance, uri, postData)
	return json.loads(response.content)

def createScore(instance, **kwargs):
	uri = kwargs.pop('uri', None)
	if not uri:
		uri = '/competitions/%s/scores.json' % kwargs.get('competitionId', '1')#str(competitionId)
	postData = exampleData.score
	postData.update(kwargs)
	response = post(instance, uri, postData)
	return json.loads(response.content)

def createIncident(instance, **kwargs):
	uri = kwargs.pop('uri', None)
	if not uri:
		uri = '/competitions/%s/incidents.json' % kwargs.get('competitionId', '1')#str(competitionId)
	postData = exampleData.incident
	postData.update(kwargs)
	response = post(instance, uri, postData)
	return json.loads(response.content)

def createIncidentResponse(instance, **kwargs):
	uri = kwargs.pop('uri', None)
	if not uri:
		uri = '/competitions/%s/incidentresponses.json' % kwargs.get('competitionId', '1')#str(competitionId)
	postData = exampleData.incidentResponse
	postData.update(kwargs)
	response = post(instance, uri, postData)
	return json.loads(response.content)

def createTeam(instance, **kwargs):
	uri = kwargs.pop('uri', None)
	if not uri:
		uri = '/competitions/%s/teams.json' % kwargs.get('competitionId', '1')#str(competitionId)
	postData = exampleData.team
	postData.update(kwargs)
	response = post(instance, uri, postData)
	return json.loads(response.content)

def createService(instance, **kwargs):
	uri = kwargs.pop('uri', None)
	if not uri:
		uri = '/competitions/%s/services.json' % kwargs.get('competitionId', '1')#str(competitionId)
	postData = exampleData.service
	postData.update(kwargs)
	response = post(instance, uri, postData)
	return json.loads(response.content)

def createPlugin(instance):
	uri = '/plugins.json'
	temporary_file = open('testfile.txt', 'w+')
	postData = exampleData.plugin
	postData['testfile.txt'] = temporary_file
	response = post(instance, uri, exampleData.plugin, postFormat = 'multipart/form-data')
	return json.loads(response.content)

def get(instance, uri, status_code = status.HTTP_200_OK, content = None):
	response = instance.client.get(uri)
	instance.assertEqual(response.status_code, status_code)
	if content:
		instance.assertEqual(response.content, content)
	return response

def put(instance, uri, data, status_code = status.HTTP_200_OK, content = None):
	response = instance.client.put(uri, data)
	instance.assertEqual(response.status_code, status_code)
	if content:
		print content
		instance.assertEqual(response.content, content)
	return response

def post(instance, uri, data, status_code = status.HTTP_201_CREATED, content = None, postFormat = None):
	client = Client()
	if not data:
		print "RECEIVED NO POST DATA"
	if postFormat:
		response = client.post(uri, data, format = postFormat)
	else:
		response = client.post(uri, data)
	## The following two lines is for testing ##
	if response.status_code != status_code:
		print response.content
	instance.assertEqual(response.status_code, status_code)
	if content:
		instance.assertEqual(response.content, content)
	return response

def patch(instance, uri, data, status_code = status.HTTP_202_ACCEPTED, content = None):
	response = instance.client.patch(uri, data, format='json')
	instance.assertEqual(response.status_code, status_code)
	if content:
		instance.assertEqual(responses.content, content)
	return response

def delete(instance, uri, status_code = status.HTTP_204_NO_CONTENT):
	response = instance.client.delete(uri)
	instance.assertEqual(response.status_code, status_code)
	return response
