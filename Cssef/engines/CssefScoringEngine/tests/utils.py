from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.test import Client
import json
import exampleData

def createService(instance, **kwargs):
	uri = kwargs.pop('uri', None)
	if not uri:
		uri = '/competitions/%s/services.json' % kwargs.get('competitionId', '1')
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
