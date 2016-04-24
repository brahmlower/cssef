import os
import re
import ast
import sys
import yaml
import time
from jsonrpcclient.http_server import HTTPServer
from cssefclient.tasks import RenewToken
from cssefclient.tasks import AvailableEndpoints
from cssefclient.utils import parseTimeNotation
from cssefclient.utils import loadTokenFile

class CssefClient(object):
	def __init__(self):
		self.config = Configuration()
		self.endpoints = None
		self.server = None

	def connect(self):
		"""Establishes a connection to the celery server

		This sets the attribute `apiConn` to an open connection to the Celery
		server, based on the settings. This connection can be provided to a
		`CeleryEndpoint` to execute a task
		"""
		self.server = HTTPServer(self.config.server_url)

	def loadEndpoints(self):
		endpoint_loader = EndpointsLoader(self.config)
		endpoint_loader.determineSource()
		self.endpoints = endpoint_loader.load()

	def loadToken(self):
		# If we're not supposed to do this, then dont do it
		if not self.config.token_auth_enabled:
			return False
		# Read the token from the file
		token = loadTokenFile(self.config.token_file)
		if token:
			self.config.token = token
		# Renew the token if it's enabled
		if self.config.token_renewal_enabled:
			return RenewToken(self.config).execute()

	def callEndpoint(self, command, args):
		"CALLING THE ENDPOINT NOW"

class Configuration(object):
	"""Contains and loads configuration values

	There is one attribute for each configuration that can be set.
	Configurations can be loaded from a file or dictionary. When loading
	configurations, any hyphens wihtin key values will be converted to
	underscores so that the attribute can be set.
	"""
	def __init__(self):
		# Super global configs
		self.globalConfigPath = "/etc/cssef/cssef.yml"
		self.userDataDir = os.path.expanduser("~/.cssef/")
		self.configPath = self.userDataDir + "cssef.yml"
		self.serverConnection = None
		# General configurations
		self.verbose = False
		self.organization = None
		self.username = None
		self.password = None
		self.task_timeout = 5
		self.admin_token = None
		# Default values for the client configuration
		self.rpc_hostname = "localhost"
		self.rpc_port = "5000"
		self.rpc_base_uri = "/"
		# Token configurations
		self.token_auth_enabled = True
		self.token = None
		self.token_file = self.userDataDir + "token"
		self.token_renewal_enabled = True
		# Endpoint caching
		self.endpoint_cache_enabled = True
		self.force_endpoint_cache = False
		self.force_endpoint_server = False
		self.endpoint_cache_file = self.userDataDir + "endpoint-cache"
		self.raw_endpoint_cache_time = '3600'

	@property
	def server_url(self):
		return "http://%s:%s%s" % (self.rpc_hostname, self.rpc_port, self.rpc_base_uri)

	@property
	def endpoint_cache_time(self):
		return self.raw_endpoint_cache_time

	@endpoint_cache_time.setter
	def endpoint_cache_time(self, value):
		try:
			self.raw_endpoint_cache_time = int(value)
		except ValueError:
			pass
		self.raw_endpoint_cache_time = parseTimeNotation(value)


	def loadConfigFile(self, configPath):
		"""Load configuration from a file

		This will read a yaml configuration file. The yaml file is converted
		to a dictionary object, which is just passed to `loadConfigDict`.

		Args:
			configPath (str): A filepath to the yaml config file

		Returns:
			None
		"""
		try:
			configDict = yaml.load(open(configPath, 'r'))
		except IOError:
			print "[WARNING] Failed to load config file at '%s'." % configPath
			return
		if configDict:
			self.loadConfigDict(configDict)

	def loadConfigDict(self, configDict):
		"""Load configurations from a dictionary

		This will convert strings with hyphens (-) to underscores (_) that way
		attributes can be added. Underscores are not used in the config files
		because I think they look ugly. That's my only reasoning - deal with
		it. Any key within the dictionary that is not an attribute of the
		class will be ignored (this will be logged).

		Args:
			configDict (dict): A dictionary containing configurations and
				values

		Returns:
			None
		"""
		# We want to make sure verbose is set first if it's provided
		if "verbose" in configDict:
			setattr(self, "verbose", bool(configDict.pop("verbose")))
			if self.verbose:
				print "[LOGGING] Configuration 'verbose' set to 'True'."
		for i in configDict:
			if hasattr(self, i.replace('-', '_')):
				# Set the attribute
				setting = i.replace('-', '_')
				value = configDict[i]
				# This is a hacky way of handling booleans: Check if the value is a string
				# and if the string is either 'true' or 'false'. If so, we're probably trying
				# to set a boolean, so we cast it to a boolean
				if type(value) is str and value.lower() in ['true', 'false']:
					value = value.lower() == 'true'
				setattr(self, setting, value)
				if self.verbose:
					print "[LOGGING] Configuration '%s' set to '%s'." % (i, value)
			elif type(configDict[i]) == dict:
				# This is a dictionary and may contain additional values
				self.loadConfigDict(configDict[i])
			else:
				# We don't care about it. Just skip it!
				# if self.verbose:
				print "[WARNING] Ignoring invalid setting '%s'." % i

class EndpointsLoader(object):
	def __init__(self, config):
		self.config = config
		self.endpoints = None
		self.fromCache = False

	def load(self):
		if self.fromCache:
			output = self.loadFromFile()
			if not output:
				# Raise an error since we failed to load the endpoints
				raise Exception
			self.endpoints = output.content
		else:
			output = self.loadFromServer()
			if not output:
				# Raise an error since we failed to load the endpoints
				raise Exception
			self.endpoints = output.content
			self.updateCache()
		return self.endpoints

	def determineSource(self):
		# Are we even caching?
		if not self.config.endpoint_cache_enabled:
			self.fromCache = False
			return
		# consider forced sources first
		if self.config.force_endpoint_cache:
			self.fromCache = True
			return
		if self.config.force_endpoint_server:
			self.fromCache = False
			return
		# Endpoint caching is enabled, but the source hasn't been forced
		# so we need to figure out if we should pull from the cache or not
		try:
			cacheLastModTime = os.stat(self.config.endpoint_cache_file).st_mtime
		except OSError:
			# Failed to read from the file, load from server
			print "Failed to read cache file: %s" % self.config.endpoint_cache_file
			# TODO: Libraries shouldn't print! (I thought this was a library, not a printing press! :P)
			self.fromCache = False
			return
		timeDelta = time.time() - cacheLastModTime
		# If it has been longer since the cache was updated than is
		# configured, then we need to load from server
		if timeDelta >= self.config.raw_endpoint_cache_time:
			self.fromCache = False
		self.fromCache = True

	def loadFromServer(self):
		"""Retrieves the available endpoints from the server.
		"""
		output = AvailableEndpoints(self.config).execute()
		return output

	def loadFromFile(self):
		"""Retrieves the available endpoints from the cache
		"""
		fileContent = open(self.config.endpoint_cache_file, 'r').read()
		# This will throw an error if the content of file cannot be literally
		# evaluated. This is good for here, but should be caught in the
		# cli tool
		self.endpoints = ast.literal_eval(fileContent)

	def updateCache(self):
		"""Writes the received endpoints to the cache file
		"""
		if not self.endpoints:
			# The endpoints are not actually endpoints. Don't write over
			# possibly valid endpoints already in the cache
			return
		wfile = open(self.config.endpoint_cache_file, 'w')
		wfile.write(str(self.endpoints))
		wfile.close()