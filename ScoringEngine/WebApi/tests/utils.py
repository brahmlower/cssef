from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.test import Client
import json
import exampleData

def createUser(instance, **kwargs):
	uri = kwargs.pop('uri', None)
	if not uri:
		uri = '/organizations/%s/members.json' % kwargs.get('organizationId', '')
	response = post(instance, uri, exampleData.user, **kwargs)
	return json.loads(response.content)

def createOrganization(instance):
	uri = '/organizations.json'
	response = post(instance, uri, exampleData.organization)
	return json.loads(response.content)

def createCompetition(instance, **kwargs):
	uri = kwargs.pop('uri', None)
	if not uri:
		uri = '/organizations/%s/competitions.json' % kwargs.get('organization', '')
	response = post(instance, uri, exampleData.competitionMin, **kwargs)
	return json.loads(response.content)

def createInject(instance, **kwargs):
	uri = '/competitions/%s/injects.json' % kwargs.get('competitionId', '1')#str(competitionId)
	response = post(instance, uri, exampleData.inject)
	return json.loads(response.content)

def createInjectResponse(instance, **kwargs):
	uri = '/competitions/%s/injectresponses.json' % kwargs.get('competitionId', '1')#str(competitionId)
	response = post(instance, uri, (exampleData.injectResponse).update(kwargs))
	return json.loads(response.content)

def createScore(instance, **kwargs):
	uri = '/competitions/%s/scores.json' % kwargs.get('competitionId', '1')#str(competitionId)
	response = post(instance, uri, exampleData.score, **kwargs)
	return json.loads(response.content)

def createIncident(instance, **kwargs):
	uri = '/competitions/%s/incidents.json' % kwargs.get('competitionId', '1')#str(competitionId)
	response = post(instance, uri, exampleData.incident)
	return json.loads(response.content)

def createIncidentResponse(instance, **kwargs):
	uri = '/competitions/%s/incidentresponses.json' % kwargs.get('competitionId', '1')#str(competitionId)
	response = post(instance, uri, (exampleData.incidentResponse).update(kwargs))
	return json.loads(response.content)

def createTeam(instance, competitionId = 1):
	uri = '/competitions/%s/teams.json' % str(competitionId)
	response = post(instance, uri, exampleData.team)
	return json.loads(response.content)

def createService(instance, competitionId = 1):
	uri = '/competitions/%s/services.json' % str(competitionId)
	response = post(instance, uri, exampleData.service)
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

def post(instance, uri, data, status_code = status.HTTP_201_CREATED, content = None, postFormat = None, **kwargs):
	client = Client()
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
