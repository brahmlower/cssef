from datetime import datetime
from WebInterface.context import BaseContext
from WebInterface.context import FormContext
from WebInterface.utils import makeApiRequest
from WebInterface.modules.competition.forms import CreateCompetitionForm
from WebInterface.modules.competition.forms import CreateInjectForm
from WebInterface.modules.competition.forms import CreateTeamForm
from WebInterface.modules.competition.forms import CompetitionSettingsForm
from WebInterface.modules.organization.context import OrganizationContext
from WebInterface.modules.organization.context import OrganizationFormContext
from cssefclient.cssefclient import CompetitionGet as ApiCompetitionGet
from cssefclient.cssefclient import CompetitionAdd as ApiCompetitionAdd
from cssefclient.cssefclient import CompetitionSet as ApiCompetitionSet
from cssefclient.cssefclient import CompetitionTeamGet as ApiTeamGet
from cssefclient.cssefclient import CompetitionInjectAdd as ApiInjectAdd
from cssefclient.cssefclient import CompetitionInjectGet as ApiInjectGet
from cssefclient.cssefclient import CompetitionInjectSet as ApiInjectSet

class CompetitionContext(BaseContext):
	def __init__(self, request, competitionUrl = None):
		super(CompetitionContext, self).__init__(request)
		apiReturn = makeApiRequest(ApiCompetitionGet, {'url': competitionUrl})
		self.competition = apiReturn['content'][0]

	def getContext(self):
		super(CompetitionContext, self).getContext()
		self.context.push({'competition': self.competition})
		return self.context

class CompetitionFormContext(FormContext):
	def __init__(self, request, competitionUrl = None):
		super(CompetitionFormContext, self).__init__(request)
		apiReturn = makeApiRequest(ApiCompetitionGet, {'url': competitionUrl})
		self.competition = apiReturn['content'][0]

	def getContext(self):
		super(CompetitionFormContext, self).getContext()
		self.context.push({'competition': self.competition})
		return self.context

# ==================================================
# Management Context Classes
# ==================================================
class SummaryCompetitionContext(OrganizationContext):
	def __init__(self, request, organizationUrl):
		super(SummaryCompetitionContext, self).__init__(request, organizationUrl)

class ListCompetitionContext(OrganizationContext):
	def __init__(self, request, organizationUrl = None):
		super(ListCompetitionContext, self).__init__(request, organizationUrl)
		self.httpMethodActions['GET'] = self.apiOnGet

	def apiOnGet(self):
		apiReturn = makeApiRequest(ApiCompetitionGet, {'organization': self.organization['id']})
		self.translateApiReturn(apiReturn)

class CreateCompetitionContext(OrganizationFormContext):
	def __init__(self, request, organizationUrl = None):
		super(CreateCompetitionContext, self).__init__(request, organizationUrl)
		self.action = self.CREATE
		self.form = CreateCompetitionForm
		self.httpMethodActions['POST'] = self.apiOnPost

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		self.formData['organization'] = self.organization['id']
		output = makeApiRequest(ApiCompetitionAdd, self.formData)
		self.translateApiReturn(output)

# ==================================================
# WhiteTeam Context Classes - General
# ==================================================
class WhiteteamSummaryContext(CompetitionContext):
	def __init__(self, request, competitionUrl = None):
		super(WhiteteamSummaryContext, self).__init__(request, competitionUrl)

class WhiteteamSettingsContext(CompetitionFormContext):
	def __init__(self, request, competitionUrl = None):
		super(WhiteteamSettingsContext, self).__init__(request, competitionUrl)
		self.action = self.EDIT
		self.form = CompetitionSettingsForm
		self.httpMethodActions['GET'] = self.apiOnGet
		self.httpMethodActions['POST'] = self.apiOnPost

	def apiOnGet(self):
		output = makeApiRequest(ApiCompetitionGet, {'pkid': self.competition['id']})
		self.translateApiReturn(output)
		self.form = self.form(initial = output['content'][0])

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		self.formData['pkid'] = self.competition['id']
		output = makeApiRequest(ApiCompetitionSet, self.formData)
		self.translateApiReturn(output)
		self.form = self.form(initial = output['content'][0])

# ==================================================
# WhiteTeam Context Classes - Team
# ==================================================
class TeamListContext(CompetitionContext):
	def __init__(self, request, competitionUrl = None):
		super(TeamListContext, self).__init__(request, competitionUrl)
		self.httpMethodActions['GET'] = self.apiOnGet

	def apiOnGet(self):
		apiReturn = makeApiRequest(ApiTeamGet, {'competition': self.competition['id']})
		self.translateApiReturn(apiReturn)

class TeamEditContext(CompetitionFormContext):
	def __init__(self, request, competitionUrl = None):
		super(TeamEditContext, self).__init__(request, competitionUrl)

class TeamCreateContext(CompetitionFormContext):
	def __init__(self, request, competitionUrl = None):
		super(TeamCreateContext, self).__init__(request, competitionUrl)
		self.action = self.CREATE
		self.form = CreateTeamForm
		self.httpMethodActions['POST'] = self.apiOnPost

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		output = makeApiRequest(ApiTeamAdd, self.formData)
		self.translateApiReturn(output)

# ==================================================
# WhiteTeam Context Classes - Inject
# ==================================================
class InjectListContext(CompetitionContext):
	def __init__(self, request, competitionUrl = None):
		super(InjectListContext, self).__init__(request, competitionUrl)
		self.httpMethodActions['GET'] = self.apiOnGet

	def apiOnGet(self):
		apiReturn = makeApiRequest(ApiInjectGet, {'competition': self.competition['id']})
		self.translateApiReturn(apiReturn)

class InjectEditContext(CompetitionFormContext):
	def __init__(self, request, competitionUrl = None, pkid = None):
		super(InjectEditContext, self).__init__(request, competitionUrl)
		self.action = self.EDIT
		self.pkid = pkid
		self.form = CreateInjectForm
		self.httpMethodActions['GET'] = self.apiOnGet
		self.httpMethodActions['POST'] = self.apiOnPost

	def apiOnGet(self):
		output = makeApiRequest(ApiInjectGet, {'pkid': self.pkid})
		self.translateApiReturn(output)
		self.form = self.form(initial = output['content'][0])

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		self.formData['pkid'] = self.pkid
		for i in ['datetimeDelivery', 'datetimeResponseDue', 'datetimeResponseClose']:
			if self.formData[i] != '':
				self.formData[i] = datetime.strptime(self.formData[i], "%Y-%m-%d %H:%M:%S")
			else:
				self.formData.pop(i, None)
		output = makeApiRequest(ApiInjectSet, self.formData)
		self.translateApiReturn(output)
		if self.returnValue != 0:
			self.form = self.form(initial = self.formData)
		else:
			self.form = self.form(initial = output['content'][0])

	# def getContext(self):
	# 	super(EditOrganizationContext, self).getContext()
	# 	self.context.push({'objectId': self.pkid})
	# 	return self.context


class InjectCreateContext(CompetitionFormContext):
	def __init__(self, request, competitionUrl = None):
		super(InjectCreateContext, self).__init__(request, competitionUrl)
		self.action = self.CREATE
		self.form = CreateInjectForm
		self.httpMethodActions['POST'] = self.apiOnPost

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		self.formData['competition'] = self.competition['id']
		for i in ['datetimeDelivery', 'datetimeResponseDue', 'datetimeResponseClose']:
			if self.formData[i] != '':
				self.formData[i] = datetime.strptime(self.formData[i], "%Y-%m-%d %H:%M:%S")
			else:
				self.formData.pop(i, None)
		output = makeApiRequest(ApiInjectAdd, self.formData)
		self.translateApiReturn(output)