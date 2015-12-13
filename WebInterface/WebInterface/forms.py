from django.forms import Form
from django.forms import ModelForm
from django.forms import TextInput
from django.forms import Textarea
from django.forms import CheckboxInput
from django.forms import NumberInput
from django.forms import Select
from django.forms import ChoiceField
from django.forms import FileField
from django.forms import ModelChoiceField
from django.forms import CharField
from django.forms import BooleanField
from django.forms import IntegerField
from django.forms import HiddenInput
from django.forms.widgets import PasswordInput
from django.utils import timezone

#from WebInterface.settings import SCORING_ENGINE_API_URL
from urllib2 import urlopen
import json

from WebInterface import cssefApi
#from WebInterface.utils import makeApiRequest
from WebInterface.client import OrganizationGet as ApiOrganizationGet
from WebInterface.client import getConn as getCeleryConnection
def makeApiRequest(apiEndpoint, argsDict, apiConnection = getCeleryConnection()):
	print 'Making api request to endpoint "%s" with arguments "%s"' % (apiEndpoint, argsDict)
	command = apiEndpoint(apiConnection)
	return command.execute(**argsDict)

def apiGet(page):
	url = SCORING_ENGINE_API_URL + page
	return urlopen(url)

def apiQuery(page):
	response = apiGet(page)
	jsonString = response.read()
	return json.loads(jsonString)

class DeleteObject(Form):
	objectId = IntegerField(widget = HiddenInput())
	def __init__(self, objectId):
		super(DeleteObject, self).__init__()
		self.fields['objectId'].initial = objectId

class LoginSiteAdmin(Form):
	username = CharField(label = 'Username', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	password = CharField(label = 'Password', widget = PasswordInput(attrs={'class':'form-control', 'required': True}))

class LoginOrganizationUser(Form):
	username = CharField(label = 'Username', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	password = CharField(label = 'Password', widget = PasswordInput(attrs={'class':'form-control', 'required': True}))

class CreateOrganization(Form):
	name = CharField(
		label = 'Organization Name',
		widget = TextInput(attrs={'class':'form-control', 'required': True})
	)
	url = CharField(
		label = 'Organization URL',
		widget = TextInput(attrs={'class':'form-control', 'required': True})
	)
	description = CharField(
		label = 'Description',
		widget = TextInput(attrs={'class':'form-control'}),
		required = False
	)
	maxMembers = CharField(
		label = 'Maximum Members',
		widget = NumberInput(attrs={'class': 'form-control', 'required': True})
	)
	maxCompetitions = CharField(
		label = 'Maximum Competitions',
		widget = NumberInput(attrs={'class': 'form-control', 'required': True})
	)

class CreatePlugin(Form):
	name = CharField(label = 'Name', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	description = CharField(label = 'Description', widget = Textarea(attrs={'class':'form-control', 'required': True}))
	pluginFile = FileField(label = "File Upload", required = False)

class CreateUser(Form):
	def __init__(self, *args, **kwargs):
			super(CreateUser, self).__init__(*args, **kwargs)
			organizationChoices = []
			output = makeApiRequest(ApiOrganizationGet, {})
			for i in output['content']:
				organizationChoices.append((i['id'], i['name']))
			self.fields['organizationId'].choices = organizationChoices
	name = CharField(
		label = 'Name',
		widget = TextInput(attrs={'class':'form-control', 'required': True})
	)
	username = CharField(
		label = 'Username',
		widget = TextInput(attrs={'class':'form-control', 'required': True})
	)
	password = CharField(
		label = 'Password',
		widget = PasswordInput(attrs={'class':'form-control', 'required': True})
	)
	organizationId = ChoiceField(
		label = 'Organization',
		choices = [],
		widget = Select(attrs={'class':'form-control', 'required': True})
	)

class CreateCompetition(Form):
	name = CharField(label = 'Name', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	url = CharField(label = 'URL', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	descriptionFull = CharField(label = 'Description', widget = Textarea(attrs={'class':'form-control', 'required': True}))

class CreateInject(Form):
	def __init__(self, *args, **kwargs):
		competitionId = kwargs.pop('competitionId', None)
		injectId = kwargs.pop('injectId', None)
		kwargs.update(initial = cssefApi.getInject(competitionId, injectId))
		super(CreateInject, self).__init__(*args, **kwargs)
	requireResponse = BooleanField(label = 'Require Response', initial = True, required = False)
	manualDelivery = BooleanField(label = 'Deliver Manually', initial = True, required = False)
	datetimeDelivery = CharField(label = 'Delivery Date', widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}))
	datetimeResponseDue = CharField(label = 'Response Due Date', widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}))
	datetimeResponseClose = CharField(label = 'Response Close Date', widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}))
	title = CharField(label = 'Title', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	body = CharField(label = 'Body', widget = Textarea(attrs={'class':'form-control', 'required': True}))

class CreateTeam(Form):
	def __init__(self, *args, **kwargs):
		competitionId = kwargs.pop('competitionId', None)
		teamId = kwargs.pop('teamId', None)
		kwargs.update(initial = cssefApi.getTeam(competitionId, teamId))
		super(CreateTeam, self).__init__(*args, **kwargs)
	teamname = CharField(label = 'Team Name', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	loginname = CharField(label = 'Login Name', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	password = CharField(label = 'Password', widget = PasswordInput(attrs={'class':'form-control', 'required': True}))
	passwordConf = CharField(label = 'Confirm Password', widget = PasswordInput(attrs={'class':'form-control', 'required': True}))
	networkCidr = CharField(label = 'Team CIDR', widget = TextInput(attrs={'class':'form-control', 'required': True}))

class CreateService(Form):
	def __init__(self, *args, **kwargs):
		competitionId = kwargs.pop('competitionId', None)
		serviceId = kwargs.pop('serviceId', None)
		kwargs.update(initial = cssefApi.getService(competitionId, serviceId))
		super(CreateService, self).__init__(*args, **kwargs)
		# get a list of plugins
		self.fields['plugin'].choices = []
		for i in cssefApi.getPlugins():
			self.fields['plugin'].choices.append((i['pluginId'], i['name']))
	name = CharField(label = 'Name', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	description = CharField(label = 'Description', widget = Textarea(attrs={'class':'form-control', 'required': True}))
	plugin = ChoiceField(label = "Plugin", choices = [], widget = Select(attrs={'class':'form-control', 'required': True}))
	manualStart = BooleanField(label = 'Deliver Manually', initial = True, required = False)
	datetimeStart = CharField(label = 'Start Scoring Date', widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}))
	datetimeFinish = CharField(label = 'Stop Scoring Date', widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}))
	machineIp = CharField(label = 'Machine IP', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	machineFqdn = CharField(label = 'Machine FQND', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	defaultPort = CharField(label = 'Default Port', widget = NumberInput(attrs={'class':'form-control'}), required = False)
	points = CharField(label = 'Points', widget = NumberInput(attrs={'class':'form-control'}), required = False)

class CompetitionSettings(Form):
	name = CharField(label = 'Name', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	url = CharField(label = 'URL', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	descriptionShort = CharField(label = 'Short Description', widget = Textarea(attrs={'class':'form-control', 'required': True}))
	descriptionFull = CharField(label = 'Full Description', widget = Textarea(attrs={'class':'form-control', 'required': True}))
	datetimeDisplay = CharField(label = 'Datetime Viewable', widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}))
	autoStart = BooleanField(label = 'Start Automatically', initial = True, required = False)
	datetimeStart = CharField(label = 'Datetime Start', widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}))
	datetimeFinish = CharField(label = 'Datetime Finish', widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}))
	scoringEnabled = BooleanField(label = 'Enable Scoring', initial = True, required = False)
	scoringInterval = CharField(label = 'Scoring Interval (seconds)', widget = NumberInput(attrs={'class':'form-control'}), required = False)
	scoringIntervalUncertainty = CharField(label = 'Scoring Interval Uncertainty (seconds)', widget = NumberInput(attrs={'class':'form-control'}), required = False)
	scoringMethod = CharField(label = 'Scoring Method', widget = TextInput(attrs={'class':'form-control', 'required': True})) # TODO: This actually needs to be a choice field
	scoringSlaEnabled = BooleanField(label = 'Enable SLAs', initial = False, required = False)
	scoringSlaThreashold = CharField(label = 'SLA Violation Threashold', widget = NumberInput(attrs={'class':'form-control'}), required = False)
	scoringSlaPenalty = CharField(label = 'SLA Violation Penalty', widget = NumberInput(attrs={'class':'form-control'}), required = False)
	servicesEnabled = BooleanField(label = 'Enable Services', initial = True, required = False)
	teamsViewRankingEnabled = BooleanField(label = 'Teams can see Ranking Page(s)', initial = True, required = False)
	teamsViewScoreboardEnabled = BooleanField(label = 'Teams can see their scores', initial = True, required = False)
	teamsViewServiceStatisticsEnabled = BooleanField(label = 'Teams can see Service Statistics Page(s)', initial = True, required = False)
	teamsViewServiceStatusEnabled = BooleanField(label = 'Teams can see Service Status Page(s)', initial = True, required = False)
	teamsViewInjectsEnabled = BooleanField(label = 'Teams can see Inject Page(s)', initial = True, required = False)
	teamsViewIncidentResponseEnabled = BooleanField(label = 'Teams can see Incident Response Page(s)', initial = True, required = False)
