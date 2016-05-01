import netaddr
from datetime import datetime
from WebInterface.context import BaseContext
from WebInterface.context import FormContext
from WebInterface.utils import makeApiRequest
from WebInterface.modules.competition.forms import CreateInjectForm
from WebInterface.modules.competition.forms import CreateTeamForm
from WebInterface.modules.competition.forms import CompetitionSettingsForm
from WebInterface.modules.organization.context import OrganizationContext
from WebInterface.modules.organization.context import OrganizationFormContext

class CompetitionContext(BaseContext):
	def __init__(self, request, competitionId = None):
		super(CompetitionContext, self).__init__(request)
		apiReturn = makeApiRequest('competitionget', {'pkid': competitionId})
		self.competition = apiReturn['content'][0]

	def getContext(self):
		super(CompetitionContext, self).getContext()
		self.context.push({'competition': self.competition})
		return self.context

class CompetitionFormContext(FormContext):
	def __init__(self, request, competitionId = None):
		super(CompetitionFormContext, self).__init__(request)
		apiReturn = makeApiRequest('competitionget', {'pkid': competitionId})
		self.competition = apiReturn['content'][0]

	def getContext(self):
		super(CompetitionFormContext, self).getContext()
		self.context.push({'competition': self.competition})
		return self.context

# ==================================================
# WhiteTeam Context Classes - General
# ==================================================
class WhiteteamSummaryContext(CompetitionContext):
	def __init__(self, request, competitionId = None):
		super(WhiteteamSummaryContext, self).__init__(request, competitionId)

class WhiteteamSettingsContext(CompetitionFormContext):
	def __init__(self, request, competitionId = None):
		super(WhiteteamSettingsContext, self).__init__(request, competitionId)
		self.action = self.EDIT
		self.form = CompetitionSettingsForm
		self.httpMethodActions['GET'] = self.apiOnGet
		self.httpMethodActions['POST'] = self.apiOnPost

	def apiOnGet(self):
		apiReturn = makeApiRequest('competitionget', {'pkid': self.competition['id']})
		self.translateApiReturn(apiReturn)
		self.form = self.form(initial = apiReturn['content'][0])

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		self.formData['pkid'] = self.competition['id']
		apiReturn = makeApiRequest('competitionset', self.formData)
		self.translateApiReturn(apiReturn)
		self.form = self.form(initial = apiReturn['content'][0])

# ==================================================
# WhiteTeam Context Classes - Team
# ==================================================
class TeamListContext(CompetitionContext):
	def __init__(self, request, competitionId = None):
		super(TeamListContext, self).__init__(request, competitionId)
		self.httpMethodActions['GET'] = self.apiOnGet

	def apiOnGet(self):
		apiReturn = makeApiRequest('teamget', {'competition': self.competition['id']})
		self.translateApiReturn(apiReturn)

class TeamEditContext(CompetitionFormContext):
	def __init__(self, request, competitionId, pkid):
		super(TeamEditContext, self).__init__(request, competitionId)
		self.action = self.EDIT
		self.pkid = pkid
		self.form = CreateTeamForm
		self.httpMethodActions['GET'] = self.apiOnGet
		self.httpMethodActions['POST'] = self.apiOnPost

	def apiOnGet(self):
		apiReturn = makeApiRequest('teamget', {'pkid': self.pkid})
		self.translateApiReturn(apiReturn)
		self.form = self.form(initial = apiReturn['content'][0])

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		# Make sure the passwords match - return False if not
		if self.formData['password'] != self.formData['passwordConf']:
			# Passwords do not match
			self.returnValue = 1
			self.errors = "Password values do not match."
			self.form = self.form(initial = self.formData)
			return False
		else:
			self.formData.pop('passwordConf', None)
		# Make sure the CIDR is valid - return False if not
		try:
			ip = netaddr.IPNetwork(self.formData['networkCidr'])
		except netaddr.core.AddrFormatError:
			self.returnValue = 1
			self.errors = "Network CIDR is invalid."
			self.form = self.form(initial = self.formData)
			return False
		self.formData['pkid'] = self.pkid
		apiReturn = makeApiRequest('teamset', self.formData)
		self.translateApiReturn(apiReturn)
		if self.returnValue != 0:
			self.form = self.form(initial = self.formData)
		else:
			self.form = self.form(initial = apiReturn['content'][0])

class TeamCreateContext(CompetitionFormContext):
	def __init__(self, request, competitionId = None):
		super(TeamCreateContext, self).__init__(request, competitionId)
		self.action = self.CREATE
		self.form = CreateTeamForm
		self.httpMethodActions['POST'] = self.apiOnPost

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		# Make sure the passwords match - return False if not
		if self.formData['password'] != self.formData['passwordConf']:
			# Passwords do not match
			self.returnValue = 1
			self.errors = "Password values do not match."
			self.form = self.form(initial = self.formData)
			return False
		else:
			self.formData.pop('passwordConf', None)
		# Make sure the CIDR is valid - return False if not
		try:
			ip = netaddr.IPNetwork(self.formData['networkCidr'])
		except netaddr.core.AddrFormatError:
			self.returnValue = 1
			self.errors = "Network CIDR is invalid."
			self.form = self.form(initial = self.formData)
			return False
		self.formData['competition'] = self.competition['id']
		apiReturn = makeApiRequest('teamadd', self.formData)
		self.translateApiReturn(apiReturn)

# ==================================================
# WhiteTeam Context Classes - Inject
# ==================================================
class InjectListContext(CompetitionContext):
	def __init__(self, request, competitionId = None):
		super(InjectListContext, self).__init__(request, competitionId)
		self.httpMethodActions['GET'] = self.apiOnGet

	def apiOnGet(self):
		apiReturn = makeApiRequest('injectget', {'competition': self.competition['id']})
		self.translateApiReturn(apiReturn)

class InjectEditContext(CompetitionFormContext):
	def __init__(self, request, competitionId = None, pkid = None):
		super(InjectEditContext, self).__init__(request, competitionId)
		self.action = self.EDIT
		self.pkid = pkid
		self.form = CreateInjectForm
		self.httpMethodActions['GET'] = self.apiOnGet
		self.httpMethodActions['POST'] = self.apiOnPost

	def apiOnGet(self):
		apiReturn = makeApiRequest('injectget', {'pkid': self.pkid})
		self.translateApiReturn(apiReturn)
		self.form = self.form(initial = apiReturn['content'][0])

	def apiOnPost(self):
		if not self.validateFormData():
			return False
		self.formData['pkid'] = self.pkid
		for i in ['datetimeDelivery', 'datetimeResponseDue', 'datetimeResponseClose']:
			if self.formData[i] != '':
				self.formData[i] = datetime.strptime(self.formData[i], "%Y-%m-%d %H:%M:%S")
			else:
				self.formData.pop(i, None)
		apiReturn = makeApiRequest('injectset', self.formData)
		self.translateApiReturn(apiReturn)
		if self.returnValue != 0:
			self.form = self.form(initial = self.formData)
		else:
			self.form = self.form(initial = apiReturn['content'][0])

class InjectCreateContext(CompetitionFormContext):
	def __init__(self, request, competitionId = None):
		super(InjectCreateContext, self).__init__(request, competitionId)
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
		apiReturn = makeApiRequest('injectadd', self.formData)
		self.translateApiReturn(apiReturn)