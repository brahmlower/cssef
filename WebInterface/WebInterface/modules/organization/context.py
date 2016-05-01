from WebInterface.utils import makeApiRequest
from WebInterface.context import BaseContext
from WebInterface.context import FormContext
from WebInterface.modules.organization.forms import DeletePluginCompForm
from WebInterface.modules.organization.forms import CreatePluginCompForm

class OrganizationContext(BaseContext):
	def __init__(self, request, organizationId = None):
		super(OrganizationContext, self).__init__(request)
		apiReturn = makeApiRequest('organizationget', {'pkid': organizationId})
		self.organization = apiReturn['content'][0]

	def getContext(self):
		super(OrganizationContext, self).getContext()
		self.context.push({'organization': self.organization})
		return self.context

class OrganizationFormContext(FormContext):
	def __init__(self, request, organizationId):
		super(OrganizationFormContext, self).__init__(request)
		apiReturn = makeApiRequest('organizationget', {'pkid': organizationId})
		self.organization = apiReturn['content'][0]

	def getContext(self):
		super(OrganizationFormContext, self).getContext()
		self.context.push({'organization': self.organization})
		return self.context

class ListMemberContext(OrganizationContext):
	def __init__(self, request, organizationId = None):
		super(ListMemberContext, self).__init__(request, organizationId)
		self.httpMethodActions['GET'] = self.apiOnGet

	def apiOnGet(self):
		apiReturn = makeApiRequest('userget', {'organization': self.organization['id']})
		self.translateApiReturn(apiReturn)

	def getContext(self):
		super(ListMemberContext, self).getContext()
		self.context.push({'members': self.apiData})
		return self.context

class CompPluginListContext(OrganizationContext):
	def __init__(self, request, organizationId, plugin_name):
		super(CompPluginListContext, self).__init__(request, organizationId)
		self.forms = {
			'form_delete': DeletePluginCompForm(),
			'form_create': CreatePluginCompForm()
		}
		self.httpMethodActions['GET'] = self.apiOnGet

	def apiOnGet(self):
		apiReturn = makeApiRequest('competitionget', {'organization': self.organization['id']})
		self.translateApiReturn(apiReturn)

	def getContext(self):
		super(CompPluginListContext, self).getContext()
		self.context.push({'members': self.apiData})
		return self.context

class CompPluginCreateContext(OrganizationFormContext):
	def __init__(self, request, organizationId):
		super(CompPluginCreateContext, self).__init__(request, organizationId)
		self.action = self.CREATE
		self.form = CreatePluginCompForm
		self.httpMethodActions['POST'] = self.apiOnPost

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		self.formData['organization'] = self.organization['id']
		output = makeApiRequest('competitionadd', self.formData)
		self.translateApiReturn(output)

class OrganizationSettingsContext(OrganizationContext):
	def __init__(self, request, organizationId = None):
		super(OrganizationSettingsContext, self).__init__(request, organizationId)
# class OrganizationSettingsContext(OrganizationFormContext):
# 	def __init__(self, request, organizationUrl = None):
# 		super(OrganizationSettingsContext, self).__init__(request, organizationUrl)
# 		self.action = self.CREATE
# 		self.form = EditSettingsForm
# 		self.httpMethodActions['POST'] = self.apiOnPost

# 	def apiOnPost(self):
# 		if not self.validateFormData():
# 			return False
# 		output = makeApiRequest(ApiOrganizationSettings, self.formData)
# 		self.translateApiReturn(output)