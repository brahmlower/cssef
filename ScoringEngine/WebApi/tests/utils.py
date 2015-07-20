from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.test import Client
import json
import exampleData

def createCompetition(instance):
	url = '/competitions.json'
	return submitPostData(url, exampleData.competitionMin, instance)

def createInject(instance):
	url = '/competitions/1/injects.json'
	return submitPostData(url, exampleData.inject, instance)

def createScore(instance):
    url = '/competitions/1/scores.json'
    return submitPostData(url, exampleData.score, instance)

def createIncidentResponse(instance):
    url = '/competitions/1/incidentresponses.json'
    return submitPostData(url, exampleData.incidentResponse, instance)

def createTeam(instance):
    url = '/competitions/1/teams.json'
    return submitPostData(url, exampleData.team, instance)

def createService(instance):
    url = '/competitions/1/services.json'
    return submitPostData(url, exampleData.service, instance)

def createPlugin(instance):
    url = '/plugins.json'
    temporary_file = open('testfile.txt','w')
    fileDict = {'testfile.txt': temporary_file}
    #return submitPostData(url, exampleData.plugin, instance)
    return post(instance, url, exampleData.plugin, files = fileDict, postFormat = 'multipart')

def submitPostData(url, data, instance = None, postFormat = None):
	client = Client()
	response = client.post(url, data)
	if instance:
		instance.assertEqual(response.status_code, status.HTTP_201_CREATED)
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

def post(instance, url, data, status_code = status.HTTP_201_CREATED, content = None, files = None, postFormat = None):
	client = Client()
	if postFormat and files:
		response = client.post(url, data, files = files, format = postFormat)
	elif postFormat:
		response = client.post(url, data, format = postFormat)
	else:
		response = client.post(url, data)
		#response = instance.client.post(url, data)#, format='json')
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

def getInvalid(instance, url, status_code = status.HTTP_404_NOT_FOUND):
	response = instance.client.get(url)
	instance.assertEqual(response.content, '')
	instance.assertEqual(response.status_code, status_code)
	return response
