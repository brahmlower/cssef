from django.template import RequestContext
from WebInterface.forms import CreateCompetition
from WebInterface.forms import CreateOrganization
from WebInterface.forms import CreateUser
from WebInterface.forms import CreatePlugin
from WebInterface import cssefApi

class ContextFactory():
	ACTION_EDIT = 'edit'
	ACTION_CREATE = 'create'
	def __init__(self, request, objectId = None):
		self.request = request
		self.data = None
		if not objectId:
			self.objectId = None
			self.action = ContextFactory.ACTION_CREATE
		else:
			self.objectId = str(objectId)
			self.action = ContextFactory.ACTION_EDIT
		self.context = RequestContext(request)
		self.context.push({'action': self.action})

	def __getitem__(self, item):
		return self.context[item]

	def populateForm(self, form, apiUrl, idFieldName):
		if self.objectId:
			self.context.push({idFieldName: self.objectId})
			self.data = cssefApi.get(apiUrl % self.objectId)
		self.context.push({'form': form(initial = self.data)})

	def push(self, dictionary):
		self.context.push(dictionary)

	def Competition(self):
		self.populateForm(CreateCompetition, 'competition/%s.json', 'competitionId')
		return self.context

	def Organization(self):
		self.populateForm(CreateOrganization, 'organizations/%s.json', 'organizationId')
		return self.context

	def User(self):
		self.populateForm(CreateUser, 'users/%s.json', 'userId')
		return self.context

	def Plugin(self):
		self.populateForm(CreatePlugin, 'plugins/%s.json', 'pluginId')
		return self.context

	def General(self):
		return self.context

	def setCompetition(self):
		organization = cssefApi.getOrganization(organizationUrl)
		competition = cssefApi.getCompetition(organization['organizationId'], competitionUrl)
		self.context.push({'organization': organization, 'competition': competition})

	def CreateInject(self):
		pass