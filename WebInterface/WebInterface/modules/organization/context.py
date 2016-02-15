from WebInterface.utils import makeApiRequest
from WebInterface.context import BaseContext
from WebInterface.context import FormContext
from WebInterface.modules.competition.forms import CreateCompetitionForm

class OrganizationContext(BaseContext):
	def __init__(self, request, organizationId = None):
		super(OrganizationContext, self).__init__(request)
		apiReturn = makeApiRequest('organizationGet', {'pkid': organizationId})
		self.organization = apiReturn['content'][0]

	def getContext(self):
		super(OrganizationContext, self).getContext()
		self.context.push({'organization': self.organization})
		return self.context

class OrganizationFormContext(FormContext):
	def __init__(self, request, organizationId = None):
		super(OrganizationFormContext, self).__init__(request)
		apiReturn = makeApiRequest('organizationGet', {'pkid': organizationId})
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
		apiReturn = makeApiRequest('userGet', {'organization': self.organization['id']})
		self.translateApiReturn(apiReturn)

	def getContext(self):
		super(ListMemberContext, self).getContext()
		self.context.push({'members': self.apiData})
		return self.context

# class ListCompetitionContext(OrganizationContext):
# 	def __init__(self, request, organizationUrl = None):
# 		super(ListCompetitionContext, self).__init__(request, organizationUrl)
# 		self.httpMethodActions['GET'] = self.apiOnGet

# 	def apiOnGet(self):
# 		apiReturn = makeApiRequest(ApiCompetitionGet, {'organization': self.organization['id']})
# 		self.translateApiReturn(apiReturn)

# class CreateCompetitionContext(OrganizationFormContext):
# 	def __init__(self, request, organizationUrl = None):
# 		super(CreateCompetitionContext, self).__init__(request, organizationUrl)
# 		self.action = self.CREATE
# 		self.form = CreateCompetitionForm
# 		self.httpMethodActions['POST'] = self.apiOnPost

# 	def apiOnPost(self):
# 		if not self.validateFormData():
# 			return False
# 		output = makeApiRequest(ApiCompetitionAdd, self.formData)
# 		self.translateApiReturn(output)

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