import os
import re
import sys
import stat
import yaml
from jsonrpcclient.http_server import HTTPServer

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
		self.raw_endpoint_cache_time = '12h'

		# Ensure user data directory exists
		if not os.path.exists(self.userDataDir):
			os.makedirs(self.userDataDir)

	@property
	def server_url(self):
		return "http://%s:%s%s" % (self.rpc_hostname, self.rpc_port, self.rpc_base_uri)

	@server_url.setter
	def server_url(self, value):
		# TODO: Finish implementing this :)
		pass

	@property
	def endpoint_cache_time(self):
		return self.raw_endpoint_cache_time

	@endpoint_cache_time.setter
	def endpoint_cache_time(self, value):
		try:
			self.raw_endpoint_cache_time = int(value)
		except ValueError:
			pass
		self.raw_endpoint_cache_time = self.parseTimeNotation(value)

	def parseTimeNotation(self, value):
		valueNotationList = [
                    {"value": 1, "alias": ["s", "second", "seconds"]},
                    {"value": 60, "alias": ["m", "minute", "minutes"]},
                    {"value": 3600, "alias": ["h", "hour", "hours"]},
                    {"value": 86400, "alias": ["d", "day", "days"]}]
		strings = filter(None, re.split('(\d+)', value))
		timeValue = strings[0]
		timeMetric = strings[1]
		for i in valueNotationList:
			if timeMetric in i['alias']:
				return i['value'] * timeValue
		# Reaching this point means the metric is not a known alias
		raise ValueError

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

	def loadTokenFile(self):
		"""Load token from a file

		This will try to load the token from the token cache file. If
		successful, it will save the token it finds in the `token` attribute
		for use while sending requests to the server.

		Returns:
			bool: True if token was successfully loaded, otherwise False.
		"""
		# Make sure the file exists
		if not os.path.isfile(self.token_file):
			sys.stderr.write("[WARNING] Token file not found. Cannot use token authentication.\n")
			sys.stderr.flush()
			return False
		# Now make sure that only we have access to it
		filePermissions = os.stat(self.token_file).st_mode
		permissionsDenied = [stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP,
                        stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH]
		for i in permissionsDenied:
			if bool(filePermissions & i):
				sys.stderr.write("Token file may not have any permissions for group or other.\n")
				sys.stderr.flush()
				return False
		# Now actually read in the file
		token = open(self.token_file, 'r').read()
		if len(token) > 0:
			self.token = token
			return True
		else:
			if self.verbose:
				print "[LOGGING] Token file empty. Cannot use token authentication."

	def establishApiConnection(self):
		"""Establishes a connection to the celery server

		This sets the attribute `apiConn` to an open connection to the Celery
		server, based on the settings. This connection can be provided to a
		`CeleryEndpoint` to execute a task
		"""
		self.serverConnection = HTTPServer(self.server_url)
