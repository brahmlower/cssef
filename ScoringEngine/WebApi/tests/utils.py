from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.test import Client
import json
import exampleData

def createUser(instance):
	url = '/users.json'
	response = post(instance, url, exampleData.user)
	return json.loads(response.content)

def createOrganization(instance):
	url = '/organizations.json'
	response = post(instance, url, exampleData.organization)
	return json.loads(response.content)

def createCompetition(instance):
	url = '/competitions.json'
	response = post(instance, url, exampleData.competitionMin)
	return json.loads(response.content)

def createInject(instance):
	url = '/competitions/1/injects.json'
	response = post(instance, url, exampleData.inject)
	return json.loads(response.content)

def createScore(instance):
    url = '/competitions/1/scores.json'
    response = post(instance, url, exampleData.score)
    return json.loads(response.content)

def createIncidentResponse(instance):
    url = '/competitions/1/incidentresponses.json'
    response = post(instance, url, exampleData.incidentResponse)
    return json.loads(response.content)

def createTeam(instance):
    url = '/competitions/1/teams.json'
    response = post(instance, url, exampleData.team)
    return json.loads(response.content)

def createService(instance):
    url = '/competitions/1/services.json'
    response = post(instance, url, exampleData.service)
    return json.loads(response.content)

def createPlugin(instance):
    url = '/plugins.json'
    temporary_file = open('testfile.txt','rw')
    postData = exampleData.plugin
    postData['testfile.txt'] = temporary_file
    response = post(instance, url, exampleData.plugin, postFormat = 'multipart/form-data')
    return json.loads(response.content)

def get(instance, url, status_code = status.HTTP_200_OK, content = None):
	response = instance.client.get(url)
	instance.assertEqual(response.status_code, status_code)
	if content:
		instance.assertEqual(response.content, content)
	return response

def put(instance, url, data, status_code = status.HTTP_200_OK, content = None):
	response = instance.client.put(url, data)
	instance.assertEqual(response.status_code, status_code)
	if content:
		print content
		instance.assertEqual(response.content, content)
	return response

def post(instance, url, data, status_code = status.HTTP_201_CREATED, content = None, postFormat = None):
	client = Client()
	if postFormat:
		response = client.post(url, data, format = postFormat)
	else:
		response = client.post(url, data)
	instance.assertEqual(response.status_code, status_code)
	if content:
		instance.assertEqual(response.content, content)
	return response

def patch(instance, url, data, status_code = status.HTTP_202_ACCEPTED, content = None):
	response = instance.client.patch(url, data, format='json')
	instance.assertEqual(response.status_code, status_code)
	if content:
		instance.assertEqual(responses.content, content)
	return response

def delete(instance, url, status_code = status.HTTP_204_NO_CONTENT):
	response = instance.client.delete(url)
	instance.assertEqual(response.status_code, status_code)
	return response
