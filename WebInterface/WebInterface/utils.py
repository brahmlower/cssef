from django.template import RequestContext
from WebInterface.forms import CreateCompetition
from WebInterface.forms import CreateOrganization as CreateOrganizationForm
from WebInterface.forms import CreateUser as CreateUserForm
from WebInterface.forms import CreatePlugin
from WebInterface.client import getConn as getCeleryConnection
from WebInterface.client import OrganizationGet as ApiOrganizationGet
from WebInterface.client import OrganizationSet as ApiOrganizationSet
from WebInterface.client import OrganizationAdd as ApiOrganizationAdd
from WebInterface.client import OrganizationDel as ApiOrganizationDel
from WebInterface.client import UserAdd as ApiUserAdd
from WebInterface.client import UserDel as ApiUserDel
from WebInterface.client import UserSet as ApiUserSet
from WebInterface.client import UserGet as ApiUserGet

def makeApiRequest(apiEndpoint, argsDict, apiConnection = getCeleryConnection()):
	print 'Making api request to endpoint "%s" with arguments "%s"' % (apiEndpoint, argsDict)
	command = apiEndpoint(apiConnection)
	return command.execute(**argsDict)

class BaseContext(object):
	def __init__(self, request):
		self.debug = False
		self.returnValue = 0
		self.errors = []
		self.apiData = None
		self.request = request
		self.context = RequestContext(self.request)
		self.httpMethodActions = {}

	def isValid(self):
		return self.returnValue == 0

	def processContext(self):
		try:
			return self.httpMethodActions[self.request.method]()
		except KeyError:
			return None

	def translateApiReturn(self, output):
		self.returnValue = output['value']
		if type(output['message']) == list:
			self.errors = "\n".join(output['message'])
		else:
			self.error = output['message']
		self.apiData = output['content']

	def getContext(self):
		self.context.push({'debug': self.debug})
		self.context.push({'returnValue': self.returnValue})
		self.context.push({'errors': self.errors})
		self.context.push({'apiData': self.apiData})
		return self.context

class FormContext(BaseContext):
	CREATE = 'create'
	EDIT = 'edit'
	def __init__(self, request):
		super(FormContext, self).__init__(request)
		self.debug = True
		self.formData = None
		self.form = None

	def validateFormData(self):
		formData = self.form(self.request.POST)
		self.errors = formData.errors
		if self.errors:
			self.returnValue = 1
			self.form = self.form(initial = self.request.POST)
		self.formData = formData.cleaned_data
		return self.isValid()

	def getContext(self):
		super(FormContext, self).getContext()
		self.context.push({'action': self.action})
		self.context.push({'form': self.form})
		return self.context

###################################################
# Organization context generators
###################################################
class EditOrganizationContext(FormContext):
	def __init__(self, request, pkid = None):
		super(EditOrganizationContext, self).__init__(request)
		self.action = self.EDIT
		self.pkid = pkid
		self.form = CreateOrganizationForm
		self.httpMethodActions['GET'] = self.apiOnGet
		self.httpMethodActions['POST'] = self.apiOnPost

	def apiOnGet(self):
		output = makeApiRequest(ApiOrganizationGet, {'pkid': self.pkid})
		self.translateApiReturn(output)
		self.form = self.form(initial = output['content'][0])

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		self.formData['pkid'] = self.pkid
		output = makeApiRequest(ApiOrganizationSet, self.formData)
		self.translateApiReturn(output)
		self.form = self.form(initial = output['content'][0])

	def getContext(self):
		super(EditOrganizationContext, self).getContext()
		self.context.push({'objectId': self.pkid})
		return self.context

class CreateOrganizationContext(FormContext):
	def __init__(self, request):
		super(CreateOrganizationContext, self).__init__(request)
		self.action = self.CREATE
		self.form = CreateOrganizationForm
		self.httpMethodActions['POST'] = self.apiOnPost

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		output = makeApiRequest(ApiOrganizationAdd, self.formData)
		self.translateApiReturn(output)

class ListOrganizationContext(BaseContext):
	def __init__(self, request):
		super(ListOrganizationContext, self).__init__(request)
		self.httpMethodActions['GET'] = self.apiOnGet

	def apiOnGet(self):
		output = makeApiRequest(ApiOrganizationGet, {})
		self.translateApiReturn(output)

###################################################
# User context generators
###################################################
class EditUserContext(FormContext):
	def __init__(self, request, pkid = None):
		super(EditUserContext, self).__init__(request)
		self.action = self.EDIT
		self.pkid = pkid
		self.form = CreateUserForm
		self.httpMethodActions['GET'] = self.apiOnGet
		self.httpMethodActions['POST'] = self.apiOnPost

	def apiOnGet(self):
		output = makeApiRequest(self.request, ApiUserGet, {'pkid': self.pkid})
		self.translateApiReturn(output)
		self.form = self.form(initial = output['content'][0])

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		self.formData['pkid'] = self.pkid
		output = makeApiRequest(self.request, ApiUserSet, self.formData)
		self.translateApiReturn(output)
		self.form = self.form(initial = output['content'][0])

class CreateUserContext(FormContext):
	def __init__(self, request):
		super(CreateUserContext, self).__init__(request)
		self.action = self.CREATE
		self.form = CreateUserForm
		self.httpMethodActions['POST'] = self.apiOnPost

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		output = makeApiRequest(ApiUserAdd, self.formData)
		self.translateApiReturn(output)


class ListUserContext(BaseContext):
	def __init__(self, request):
		super(ListUserContext, self).__init__(request)
		self.httpMethodActions['GET'] = self.apiOnGet

	def apiOnGet(self):
		output = makeApiRequest(ApiUserGet, {})
		self.translateApiReturn(output)

###################################################
# Site Configs context generators
###################################################
class EditSiteConfigContext(FormContext):
	pass


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
		if self.objectId:
			self.push({'plugin': cssefApi.get('plugins/%s.json' % self.objectId)})
		return self.context

	def General(self):
		return self.context

	def setCompetition(self):
		organization = cssefApi.getOrganization(organizationUrl)
		competition = cssefApi.getCompetition(organization['organizationId'], competitionUrl)
		self.context.push({'organization': organization, 'competition': competition})

	def CreateInject(self):
		pass