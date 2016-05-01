from WebInterface.context import BaseContext
from WebInterface.context import FormContext
from WebInterface.utils import makeApiRequest
from WebInterface.modules.administrator.forms import CreateOrganizationForm
from WebInterface.modules.administrator.forms import DeleteOrganizationForm
from WebInterface.modules.administrator.forms import CreateUserForm
from WebInterface.modules.administrator.forms import DeleteUserForm

###################################################
# Administrator context generators
###################################################
class HomeContext(BaseContext):
	def __init__(self, request):
		super(HomeContext, self).__init__(request)
		self.httpMethodActions['GET'] = self.apiOnGet

	def apiOnGet(self):
		pass

class SiteConfigsContext(BaseContext):
	def __init__(self, request):
		super(HomeContext, self).__init__(request)
		self.httpMethodActions['GET'] = self.apiOnGet

	def apiOnGet(self):
		pass

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
		output = makeApiRequest('organizationget', {'pkid': self.pkid})
		self.translateApiReturn(output)
		self.form = self.form(initial = output['content'][0])

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		self.formData['pkid'] = self.pkid
		output = makeApiRequest('organizationset', self.formData)
		self.translateApiReturn(output)
		if output['value'] == 0:
			self.form = self.form(initial = output['content'][0])
		else:
			self.form = self.form(initial = self.formData)

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
		output = makeApiRequest('organizationadd', self.formData)
		self.translateApiReturn(output)

class ListOrganizationContext(BaseContext):
	def __init__(self, request):
		super(ListOrganizationContext, self).__init__(request)
		self.forms = {
			'form_delete': DeleteOrganizationForm(),
			'form_create': CreateOrganizationForm()
		}
		self.httpMethodActions['GET'] = self.apiOnGet

	def apiOnGet(self):
		output = makeApiRequest('organizationget', {})
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
		output = makeApiRequest('userget', {'pkid': self.pkid})
		self.translateApiReturn(output)
		self.form = self.form(initial = output['content'][0])

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		self.formData['pkid'] = self.pkid
		output = makeApiRequest('serSet', self.formData)
		self.translateApiReturn(output)
		if output['value'] == 0:
			self.form = self.form(initial = output['content'][0])
		else:
			# There's an error here, but fill the form with the data
			# that was provided when the form was posted
			self.form = self.form(initial = self.formData)

	def getContext(self):
		super(EditUserContext, self).getContext()
		self.context.push({'objectId': self.pkid})
		return self.context

class CreateUserContext(FormContext):
	def __init__(self, request):
		super(CreateUserContext, self).__init__(request)
		self.action = self.CREATE
		self.form = CreateUserForm
		self.httpMethodActions['POST'] = self.apiOnPost

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		output = makeApiRequest('useradd', self.formData)
		self.translateApiReturn(output)

class ListUserContext(BaseContext):
	def __init__(self, request):
		super(ListUserContext, self).__init__(request)
		self.forms = {
			'form_delete': DeleteUserForm(),
			'form_create': CreateUserForm()
		}
		self.httpMethodActions['GET'] = self.apiOnGet

	def apiOnGet(self):
		output = makeApiRequest('userget', {})
		self.translateApiReturn(output)

class DeleteUserContext(FormContext):
	def __init__(self, request):
		super(DeleteUserContext, self).__init__(request)
		self.action = self.DELETE
		self.form = DeleteUserForm
		self.httpMethodActions['POST'] = self.apiOnPost

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		output = makeApiRequest('userdel', self.formData)
		self.translateApiReturn(output)

###################################################
# Site Configs context generators
###################################################
class EditSiteConfigContext(FormContext):
	pass

###################################################
# Scoring Engine context generators
###################################################
class EditScoringEngineContext(BaseContext):
	pass

class CreateScoringEngineContext(BaseContext):
	pass

class ListScoringEnginesContext(BaseContext):
	def __init__(self, request):
		super(ListScoringEnginesContext, self).__init__(request)
		self.httpMethodActions['GET'] = self.apiOnGet

	def apiOnGet(self):
		output = makeApiRequest('scoringengineget', {})
		self.translateApiReturn(output)

class DeleteScoringEngineContext(BaseContext):
	pass