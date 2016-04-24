import os
import re
import sys
import stat

class CommandOutput(object):
	def __init__(self, value, message, content):
		self.value = value
		self.message = message
		# Cast the content to a list
		if type(content) == list:
			self.content = content
		elif type(content) == str:
			self.content = [content]
		else:
			raise ValueError
		# Get the keys of the content if it's a dict
		if len(self.content) > 0 and type(self.content[0]) == dict:
			self.tableHeaders = self.content[0].keys()
		else:
			self.tableHeaders = None

	def __nonzero__(self):
		return 0 == self.value

class RPCEndpoint(object):
	"""Base class to represent an endpoint task on the server.

	This class gets subclassed by other classes to define a specific
	task on the cssef server.
	"""
	def __init__(self, config, endpointName, args):
		"""
		Args:
			config (Configuration): The current configuration to use
			endpointName (str): The task name as defined by the rpc server
			args (list): Arguments that are available to the task

		Attributes:
			config (Configuration): The current configuration to use
			endpointName (str): The task name as defined by the rpc server
			args (list): Arguments that are available to the task
		"""
		self.config = config
		self.endpointName = endpointName
		self.args = args
		self.task = None

	@classmethod
	def fromDict(cls, config, inputDict):
		"""Creates a RPCEndpoint object from a dictionary

		Args:
			config (Configuration): The current configuration to use
			inputDict (dict): Dictionary containing necessary values to define
				the rpc endpoint

		Returns:
			An instance of RPCEndpoint that has been filled with the
			information defined in the provided dictionary is returned.

		Example:
			<todo>
		"""
		args = []
		instance = cls(config, inputDict['endpointName'], args)
		instance.name = inputDict['name']
		return instance

	def execute(self, **kwargs):
		"""Calls the rpc endpoint on the remote server

		Args:
			**kwargs: Keyword arguments to pass to the rpc endpoint on the
				server.

		Returns:
			CommandOutput: The task data is cast to a CommandOutput object if
			the task completed successfully. If the task experiences an
			unhandled error, it is caught and a CommandOutput object is
			created with values describing the encountered exception.
		"""
		if self.config.verbose:
			print "[LOGGING] Calling rpc with name '%s'."  % self.endpointName
		try:
			# This is a hint at a larger issue- If I don't cast this to an
			# integer, it is passed to send_task() and get() as a string
			# rather than an expected integer. This means all values read
			# from the configuration object are strings, which may be
			# problematic if a value MUST be an integer.
			#task_timeout = int(self.config.task_timeout)
			#self.task = self.config.apiConn.send_task(self.endpointName,
			#	args = args, kwargs = kwargs, expires = task_timeout)
			#result = self.task.get(timeout = task_timeout)
			result = self.config.serverConnection.request(self.endpointName, **kwargs)
			return CommandOutput(**result)
		except Exception as e:
			return CommandOutput(value=-1, content=[], message=[str(e)])

def loadTokenFile(token_file):
	"""Load token from a file

	This will try to load the token from the token cache file. If
	successful, it will save the token it finds in the `token` attribute
	for use while sending requests to the server.

	Returns:
		bool: True if token was successfully loaded, otherwise False.
	"""
	# Make sure the file exists
	if not os.path.isfile(token_file):
		sys.stderr.write("[WARNING] Token file not found. Cannot use token authentication.\n")
		sys.stderr.flush()
		return False
	# Now make sure that only we have access to it
	filePermissions = os.stat(token_file).st_mode
	permissionsDenied = [stat.S_IRGRP, stat.S_IWGRP, stat.S_IXGRP,
                    stat.S_IROTH, stat.S_IWOTH, stat.S_IXOTH]
	for i in permissionsDenied:
		if bool(filePermissions & i):
			sys.stderr.write("Token file may not have any permissions for group or other.\n")
			sys.stderr.flush()
			return False
	# Now actually read in the file
	token = open(token_file, 'r').read()
	if len(token) > 0:
		return token
	return False

def saveTokenFile(tokenFilePath, token):
	# Save the returned token
	if not os.path.exists(tokenFilePath):
		# The file doesn't exist yet, make it
		open(tokenFilePath, 'a').close()
	os.chmod(tokenFilePath, stat.S_IRUSR | stat.S_IWUSR)
	open(tokenFilePath, 'w').write(token)

def parseTimeNotation(value):
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
