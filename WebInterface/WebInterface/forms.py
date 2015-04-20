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

from WebInterface.settings import SCORING_ENGINE_API_URL
from urllib2 import urlopen
import json

from WebInterface import cssefApi

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
	name = CharField(label = 'Organization Name', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	url = CharField(label = 'Organization URL', widget = TextInput(attrs={'class':'form-control', 'required': True}))

class CreatePlugin(Form):
	name = CharField(label = 'Name', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	description = CharField(label = 'Description', widget = Textarea(attrs={'class':'form-control', 'required': True}))

class CreateUser(Form):
	def __init__(self, *args, **kwargs):
			super(CreateUser, self).__init__(*args, **kwargs)
			organizationChoices = []
			for i in apiQuery('organizations.json'):
				organizationChoices.append((i['organizationId'], i['name']))
			self.fields['organization'].choices = organizationChoices
	name = CharField(label = 'Name', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	username = CharField(label = 'Username', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	password = CharField(label = 'Password', widget = PasswordInput(attrs={'class':'form-control', 'required': True}))
	organization = ChoiceField(label = 'Organization', choices = [], widget = Select(attrs={'class':'form-control', 'required': True}))

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
	datetimeStart = CharField(label = 'Datetime Start', widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}))
	datetimeFinish = CharField(label = 'Datetime Finish', widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}))
	autoStart = BooleanField(label = 'Start Automatically', initial = True, required = False)
	scoringEnabled = BooleanField(label = 'Enable Scoring', initial = True, required = False)
	scoringInterval = CharField(label = 'Scoring Interval (seconds)', widget = NumberInput(attrs={'class':'form-control'}), required = False)
	scoringIntervalUncertainty = CharField(label = 'Scoring Interval Uncertainty (seconds)', widget = NumberInput(attrs={'class':'form-control'}), required = False)
	scoringMethod = CharField(label = 'Scoring Method', widget = TextInput(attrs={'class':'form-control', 'required': True})) # TODO: This actually needs to be a choice field
	scoringSlaEnabled = BooleanField(label = 'Enable SLAs', initial = True, required = False)
	scoringSlaThreashold = CharField(label = 'SLA Violation Threashold', widget = NumberInput(attrs={'class':'form-control'}), required = False)
	scoringSlaPenalty = CharField(label = 'SLA Violation Penalty', widget = NumberInput(attrs={'class':'form-control'}), required = False)
	servicesEnabled = BooleanField(label = 'Enable Services', initial = True, required = False)
	teamsViewRankingEnabled = BooleanField(label = 'Teams can see Ranking Page(s)', initial = True, required = False)
	teamsViewServiceStatisticsEnabled = BooleanField(label = 'Teams can see Service Statistics Page(s)', initial = True, required = False)
	teamsViewServiceStatusEnabled = BooleanField(label = 'Teams can see Service Status Page(s)', initial = True, required = False)
	teamsViewInjectsEnabled = BooleanField(label = 'Teams can see Inject Page(s)', initial = True, required = False)
	teamsViewIncidentResponseEnabled = BooleanField(label = 'Teams can see Incident Response Page(s)', initial = True, required = False)

# class CompetitionSettingsGeneralForm(ModelForm):
# 	class Meta:
# 		model = Competition
# 		fields = ['compname', 'compurl', 'description_short', 'description_full', 'datetime_display', 'datetime_start', 'datetime_finish']
# 		labels = {
# 			'datetime_display': ('Date Viewable'),
# 			'datetime_start': ('Start Time'),
# 			'datetime_finish': ('Finish Time')
# 		}
# 		widgets = {
# 			'compname': TextInput(attrs={'class':'form-control'}),
# 			'compurl': TextInput(attrs={'class':'form-control'}),
# 			'description_short': Textarea(attrs={'class':'form-control'}),
# 			'description_full': Textarea(attrs={'class':'form-control'}),
# 			'datetime_display': TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}),
# 			'datetime_start': TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}),
# 			'datetime_finish': TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"})
# 		}

# class CompetitionSettingsScoringForm(Form):
# 	scoring_enabled = BooleanField(label = 'Scoring Enabled', initial = False , required = False)
# 	scoring_interval = CharField(label = 'Scoring Interval (seconds)', widget = NumberInput(attrs={'class':'form-control'}), required = False)
# 	scoring_interval_uncty = CharField(label = 'Scoring Interval Uncertainty (seconds)', widget = NumberInput(attrs={'class':'form-control'}), required = False)
# 	scoring_method = CharField(label = 'Scoring Method', widget = TextInput(attrs={'class':'form-control'}), required = False)
# 	scoring_sla_enabled = BooleanField(label = 'SLA Violations Enabled', initial = True, required = False)
# 	scoring_sla_threashold = CharField(label = 'SLA Violation Threashold', initial = 6, widget = TextInput(attrs={'class':'form-control'}), required = False)
# 	scoring_sla_penalty = CharField(label = 'SLA Violation Penalty', initial = 50, widget = TextInput(attrs={'class':'form-control'}), required = False)

# class CompetitionSettingsServiceForm(Form):
# 	services_enabled = BooleanField(label = 'Services Enabled', initial = False, required = False)

# class CompetitionSettingsTeamForm(Form):
# 	teams_view_ranking_enabled = BooleanField(label = 'Ranking Enabled', initial = False, required = False)
# 	teams_view_scoreboard_enabled = BooleanField(label = 'Score Board Enabled', initial = False, required = False)
# 	teams_view_servicestatistics_enabled = BooleanField(label = 'Service Stats Enabled', initial = False, required = False)
# 	teams_view_servicestatus_enabled = BooleanField(label = 'Service Status Enabled', initial = False, required = False)
# 	teams_view_injects_enabled = BooleanField(label = 'Injects Enabled', initial = False, required = False)
# 	teams_view_incidentresponse_enabled = BooleanField(label = 'Incident Response Enabled', initial = False, required = False)

# class CreateTeamForm(ModelForm):
# 	class Meta:
# 		model = Team
# 		fields = ['teamname','username','password','networkaddr']
# 		labels = {
# 			'teamname': ('Team Name'),
# 			'username': ('Team Username'),
# 			'password': ('Password'),
# 			'networkaddr': ('Network Address'),
# 		}
# 		widgets = {
# 			'teamname': TextInput(attrs={'class':'form-control'}),
# 			'username': TextInput(attrs={'class':'form-control'}),
# 			'password': TextInput(attrs={'class':'form-control'}),
# 			'networkaddr': TextInput(attrs={'class':'form-control'}),
# 		}

# class TestServiceForm(Form):
# 	connectip = ChoiceField(label = "Connection Method", choices = [(0 ,'Domain Name'), (1,'IP Address')], widget = Select(attrs={'class':'form-control', 'required': True}))
# 	networkaddr = ChoiceField(label = "Network Address", widget = TextInput(attrs={'class':'form-control'}))
# 	networkloc = CharField(label = "Machine Address", widget = TextInput(attrs={'class':'form-control'}))
# 	defaultport = CharField(label = "Default Port", widget = NumberInput(attrs={'class':'form-control'}))

# class ServiceSelectionForm(Form):
# 	def __init__(self, *args, **kwargs):
# 		compid = kwargs.pop('compid')
# 		super(ServiceSelectionForm, self).__init__(*args, **kwargs)
# 		tuple_list = [(-1, "Overall Competition")]
# 		for i in Service.objects.filter(compid = compid, datetime_start__lte = timezone.now()):
# 			tuple_list.append((i.servid, "Service: "+i.name))
# 		self.fields['service'].choices = tuple_list

# 	service = ChoiceField(label = "Select service: ", choices = [], widget = Select(attrs={'class':'form-control', 'required': True}))
# 	class Meta:
# 		fields = ['service']

# class CreateServiceForm(ModelForm):
# 	def __init__(self, *args, **kwargs):
# 		super(CreateServiceForm, self).__init__(*args, **kwargs)
# 		tuple_list = []
# 		for i in ServiceModule.objects.all():
# 			tuple_list.append((i.servmdulid, i.modulename))
# 		self.fields['servicemodule'].choices = tuple_list

# 	servicemodule = ChoiceField(label = "Service Module", choices = [], widget = Select(attrs={'class':'form-control', 'required': True}))
# 	connectip = ChoiceField(label = "Connection Method", choices = [(0 ,'Domain Name'), (1,'IP Address')], widget = Select(attrs={'class':'form-control', 'required': True}))
# 	class Meta:
# 		model = Service
# 		fields = ['name', 'description', 'datetime_start', 'datetime_finish', 'points', 'networkloc', 'defaultport']
# 		labels = {
# 			'name': ('Name'),
# 			'description': ('Description'),
# 			'datetime_start': ('Start Scoring'),
# 			'datetime_finish': ('Stop Scoring'),
# 			'points': ('Points'),
# 			'networkloc': ('Machine Address'),
# 			'defaultport': ('Default Port')
# 		}
# 		widgets = {
# 			'name': TextInput(attrs={'class':'form-control'}),
# 			'points': NumberInput(attrs={'class':'form-control'}),
# 			'description': Textarea(attrs={'class':'form-control'}),
# 			'datetime_start': TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}),
# 			'datetime_finish': TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}),
# 			'networkloc': TextInput(attrs={'class':'form-control'}),
# 			'defaultport': NumberInput(attrs={'class':'form-control'}),
# 		}

# class CreateInjectForm(ModelForm):
# 	docfile = FileField(label = "File Upload", required = False)
# 	require_response = BooleanField(label = 'Require Response', initial = False , required = False)
# 	class Meta:
# 		model = Inject
# 		fields = ['compid', 'title', 'body', 'dt_delivery', 'dt_response_due', 'dt_response_close']
# 		labels = {
# 			'title': ('Title'),
# 			'body': ('Content'),
# 			'dt_delivery': ('Delivery Time'),
# 			'dt_response_due': ('Response Due Time'),
# 			'dt_response_close': ('Response Close Time')
# 		}
# 		widgets = {
# 			'title': TextInput(attrs={'class':'form-control'}),
# 			'body': Textarea(attrs={'class':'form-control'}),
# 			'dt_delivery': TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}),
# 			'dt_response_due': TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}),
# 			'dt_response_close': TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"})
# 		}

# class CreateServiceModuleForm(ModelForm):
# 	docfile = FileField(label = "File Upload", required = False)
# 	class Meta:
# 		model = ServiceModule
# 		fields = ['modulename', 'description']
# 		labels = {
# 			'modulename': ('Module Name'),
# 			'description': ('Description')
# 		}
# 		widgets = {
# 			'modulename': TextInput(attrs={'class':'form-control', 'required': True}),
# 			'description': Textarea(attrs={'class':'form-control', 'required': True})
# 		}

# class AdminLoginForm(ModelForm):
# 	class Meta:
# 		model = Admin
# 		fields = ['username', 'password']
# 		labels = {
# 			'username': ('Username'),
# 			'password': ('Password'),
# 		}
# 		widgets = {
# 			'username': TextInput(attrs={'class':'form-control', 'required': True}),
# 			'password': PasswordInput(attrs={'class':'form-control', 'required': True}),
# 		}

# class TeamLoginForm(ModelForm):
# 	def __init__(self, *args, **kwargs):
# 		super(TeamLoginForm, self).__init__(*args, **kwargs)
# 		tuple_list = []
# 		for i in Competition.objects.filter(datetime_start__lte = timezone.now(), datetime_finish__gt = timezone.now()):
# 			tuple_list.append((i.compid, i.compname))
# 		self.fields['compid'].choices = tuple_list

# 	compid = ChoiceField(label = "Competition", choices = [], widget = Select(attrs={'class':'form-control', 'required': True}))
# 	class Meta:
# 		model = Team
# 		fields = ['username', 'password', 'compid']
# 		labels = {
# 			'username': ('Team Name'),
# 			'password': ('Password')
# 		}
# 		widgets = {
# 			'username': TextInput(attrs={'class':'form-control', 'required': True}),
# 			'password': PasswordInput(attrs={'class':'form-control', 'required': True})
# 		}

# class InjectResponseForm(ModelForm):
# 	docfile = FileField(label = "File Upload", required = False)
# 	class Meta:
# 		model = InjectResponse
# 		fields = ['textentry']
# 		labels = {
# 			'textentry': ('Text Entry')
# 		}
# 		widgets = {
# 			'textentry': Textarea(attrs={'class':'form-control'})
# 		}

# class IncidentResponseForm(ModelForm):
# 	docfile = FileField(label = "File Upload", required = False)
# 	class Meta:
# 		model = IncidentResponse
# 		fields = ['textentry','subject']
# 		labels = {
# 			'subject': ('Subject'),
# 			'textentry': ('Text Entry')
# 		}
# 		widgets = {
# 			'subject': TextInput(attrs={'class':'form-control'}),
# 			'textentry': Textarea(attrs={'class':'form-control'})
# 		}

# class IncidentResponseReplyForm(ModelForm):
# 	docfile = FileField(label = "File Upload", required = False)
# 	class Meta:
# 		model = IncidentResponse
# 		fields = ['textentry']
# 		labels = {
# 			'textentry': ('Text Entry')
# 		}
# 		widgets = {
# 			'textentry': Textarea(attrs={'class':'form-control'}),
# 		}

