import sys
from prettytable import PrettyTable
from time import sleep

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

	def display(self):
		if self.value != 0:
			sys.stderr.write("An error was encountered:\n")
			print self.message
			sys.stderr.write("\n".join(self.message)+"\n")
			sys.exit(self.value)
		if self.tableHeaders:
			# Its a dictionary list, make a table and print it
			outputTable = PrettyTable(self.tableHeaders)
			outputTable.padding_width = 1
			for i in self.content:
				outputTable.add_row(i.values())
			print outputTable
		else:
			# It's just a list of strings, print each one
			# TODO: Maybe I just shouldn't support this...
			for i in self.content:
				print i

class CeleryEndpoint(object):
	"""Base class to represent a celery task on the server.
	 
	This class gets subclassed by other classes to define a specific
	task on the cssef server.
	"""
	def __init__(self, config, celeryName, args):
		"""
		Args:
			config (Configuration): The current configuration to use
			celeryName (str): The task name as defined by the celery server
			args (list): Arguments that are available to the task

		Attributes:
			config (Configuration): The current configuration to use
			celeryName (str): The task name as defined by the celery server
			args (list): Arguments that are available to the task
		"""
		self.config = config
		self.celeryName = celeryName
		self.args = args
		self.task = None

	@classmethod
	def fromDict(cls, config, inputDict):
		"""Creates a CeleryEndpoint object from a dictionary

		Args:
			config (Configuration): The current configuration to use
			inputDict (dict): Dictionary containing necessary values to define
				the celery endpoint

		Returns:
			An instance of CeleryEndpoint that has been filled with the
			information defined in the provided dictionary is returned.

		Example:
			<todo>
		"""
		args = []
		instance = cls(config, inputDict['celeryName'], args)
		instance.name = inputDict['name']
		return instance

	def execute(self, *args, **kwargs):
		"""Calls the celery task on the remote server

		Args:
			*args: Arguments to pass to the celery task on the server.
			**kwargs: Keyword arguments to pass to the celery task on the
				server.

		Returns:
			CommandOutput: The task data is cast to a CommandOutput object if
			the task completed successfully. If the task experiences an
			unhandled error, it is caught and a CommandOutput object is
			created with values describing the encountered exception.
		"""
		try:
			# This is a hint at a larger issue- If I don't cast this to an
			# integer, it is passed to send_task() and get() as a string
			# rather than an expected integer. This means all values read
			# from the configuration object are strings, which may be
			# problematic if a value MUST be an integer.
			task_timeout = int(self.config.task_timeout)
			self.task = self.config.apiConn.send_task(self.celeryName,
				args = args, kwargs = kwargs, expires = task_timeout)
			return CommandOutput(**(self.task.get(timeout = task_timeout)))
		except Exception as e:
			return CommandOutput(value = -1, content = [], message = [str(e)])
