from WebInterface.context import BaseContext
from WebInterface.context import FormContext
from WebInterface.utils import makeApiRequest
from WebInterface.modules.administrator.forms import CreateOrganizationForm
from WebInterface.modules.administrator.forms import CreateUserForm
from cssefclient.cssefclient import OrganizationGet as ApiOrganizationGet
from cssefclient.cssefclient import OrganizationSet as ApiOrganizationSet
from cssefclient.cssefclient import OrganizationAdd as ApiOrganizationAdd
from cssefclient.cssefclient import OrganizationDel as ApiOrganizationDel
from cssefclient.cssefclient import UserAdd as ApiUserAdd
from cssefclient.cssefclient import UserDel as ApiUserDel
from cssefclient.cssefclient import UserSet as ApiUserSet
from cssefclient.cssefclient import UserGet as ApiUserGet

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
