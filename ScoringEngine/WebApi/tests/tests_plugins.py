from rest_framework.test import APITestCase
from rest_framework import status
from django.test import TestCase
from django.test import Client
import exampleData
import utils

class PluginsList(APITestCase):
	def setUp(self):
		self.uri = '/plugins.json'

	def testHttp405Response(self):
		response = self.client.put(self.uri, {})
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPost(self):
		utils.createPlugin(self)

class PluginDetails(APITestCase):
	def setUp(self):
		plugin = utils.createPlugin(self)
		self.uri = '/plugins/%s.json' % (plugin['pluginId'])

	def testHttp405Response(self):
		utils.put(self, self.uri, {}, status_code = status.HTTP_405_METHOD_NOT_ALLOWED)

	def testGet(self):
		utils.get(self, self.uri)

	def testPatch(self):
		data = {"name": "This is a new name"}
		utils.patch(self, self.uri, data)

	def testDelete(self):
		utils.delete(self, self.uri)

	def testInvalid(self):
		uri = '/plugins/9000.json'
		utils.get(self, uri, status_code = status.HTTP_404_NOT_FOUND)