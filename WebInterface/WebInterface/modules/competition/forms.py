from django.forms import Form
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

class CreateCompetitionForm(Form):
	name = CharField(
		label = 'Name',
		widget = TextInput(attrs={'class':'form-control', 'required': 'True'})
	)
	url = CharField(
		label = 'URL',
		widget = TextInput(attrs={'class':'form-control', 'required': 'True'})
	)
	description = CharField(
		label = 'Description',
		widget = Textarea(attrs={'class':'form-control', 'required': 'True'})
	)

class CreateInjectForm(Form):
	title = CharField(
		label = 'Title',
		widget = TextInput(attrs={'class':'form-control', 'required': 'True'})
	)
	body = CharField(
		label = 'Body',
		widget = Textarea(attrs={'class':'form-control', 'required': 'True'})
	)
	requireResponse = BooleanField(
		label = 'Require Response',
		initial = True,
		required = False
	)
	manualDelivery = BooleanField(
		label = 'Manual Delivery',
		initial = True,
		required = False
	)
	datetimeDelivery = CharField(
		label = 'Delivery Date',
		widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm:ss"}),
		required = False
	)
	datetimeResponseDue = CharField(
		label = 'Response Due Date',
		widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm:ss"}),
		required = False
	)
	datetimeResponseClose = CharField(
		label = 'Response Close Date',
		widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm:ss"}),
		required = False
	)

class CreateTeamForm(Form):
	name = CharField(
		label = 'Team Name',
		widget = TextInput(attrs={'class':'form-control', 'required': 'True'})
	)
	username = CharField(
		label = 'Username',
		widget = TextInput(attrs={'class':'form-control', 'required': 'True'})
	)
	password = CharField(
		label = 'Password',
		widget = PasswordInput(attrs={'class':'form-control', 'required': 'True'})
	)
	passwordConf = CharField(
		label = 'Confirm Password',
		widget = PasswordInput(attrs={'class':'form-control', 'required': 'True'})
	)
	networkCidr = CharField(
		label = 'Team CIDR',
		widget = TextInput(attrs={'class':'form-control', 'required': 'True'})
	)

# class CreateServiceForm(Form):
# 	def __init__(self, *args, **kwargs):
# 		competitionId = kwargs.pop('competitionId', None)
# 		serviceId = kwargs.pop('serviceId', None)
# 		kwargs.update(initial = cssefApi.getService(competitionId, serviceId))
# 		super(CreateService, self).__init__(*args, **kwargs)
# 		# get a list of plugins
# 		self.fields['plugin'].choices = []
# 		for i in cssefApi.getPlugins():
# 			self.fields['plugin'].choices.append((i['pluginId'], i['name']))
# 	name = CharField(label = 'Name', widget = TextInput(attrs={'class':'form-control', 'required': True}))
# 	description = CharField(label = 'Description', widget = Textarea(attrs={'class':'form-control', 'required': True}))
# 	plugin = ChoiceField(label = "Plugin", choices = [], widget = Select(attrs={'class':'form-control', 'required': True}))
# 	manualStart = BooleanField(label = 'Deliver Manually', initial = True, required = False)
# 	datetimeStart = CharField(label = 'Start Scoring Date', widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}))
# 	datetimeFinish = CharField(label = 'Stop Scoring Date', widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}))
# 	machineIp = CharField(label = 'Machine IP', widget = TextInput(attrs={'class':'form-control', 'required': True}))
# 	machineFqdn = CharField(label = 'Machine FQND', widget = TextInput(attrs={'class':'form-control', 'required': True}))
# 	defaultPort = CharField(label = 'Default Port', widget = NumberInput(attrs={'class':'form-control'}), required = False)
# 	points = CharField(label = 'Points', widget = NumberInput(attrs={'class':'form-control'}), required = False)

class CompetitionSettingsForm(Form):
	name = CharField(
		label = 'Name',
		widget = TextInput(attrs={'class':'form-control', 'required': 'True'})
	)
	url = CharField(
		label = 'URL',
		widget = TextInput(attrs={'class':'form-control', 'required': 'True'})
	)
	description = CharField(
		label = 'Description',
		widget = Textarea(attrs={'class':'form-control', 'required': 'True'})
	)
	datetimeDisplay = CharField(
		label = 'Datetime Viewable',
		widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"})
	)
	autoStart = BooleanField(
		label = 'Start Automatically',
		initial = True,
		required = False
	)
	datetimeStart = CharField(
		label = 'Datetime Start',
		widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"})
	)
	datetimeFinish = CharField(
		label = 'Datetime Finish',
		widget = TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"})
	)
	scoringEnabled = BooleanField(
		label = 'Enable Scoring',
		initial = True,
		required = False
	)
	scoringInterval = CharField(
		label = 'Scoring Interval (seconds)',
		widget = NumberInput(attrs={'class':'form-control'}),
		required = False
	)
	scoringIntervalUncertainty = CharField(
		label = 'Scoring Interval Uncertainty (seconds)',
		widget = NumberInput(attrs={'class':'form-control'}),
		required = False
	)
	scoringMethod = CharField(
		label = 'Scoring Method',
		widget = TextInput(attrs={'class':'form-control', 'required': True})
	) # TODO: This actually needs to be a choice field
	scoringSlaEnabled = BooleanField(
		label = 'Enable SLAs',
		initial = False,
		required = False
	)
	scoringSlaThreashold = CharField(
		label = 'SLA Violation Threashold',
		widget = NumberInput(attrs={'class':'form-control'}),
		required = False
	)
	scoringSlaPenalty = CharField(
		label = 'SLA Violation Penalty',
		widget = NumberInput(attrs={'class':'form-control'}),
		required = False
	)
	servicesEnabled = BooleanField(
		label = 'Enable Services',
		initial = True,
		required = False
	)
	teamsViewRankingEnabled = BooleanField(
		label = 'Teams can see Ranking Page(s)',
		initial = True,
		required = False
	)
	teamsViewScoreboardEnabled = BooleanField(
		label = 'Teams can see their scores',
		initial = True,
		required = False
	)
	teamsViewServiceStatisticsEnabled = BooleanField(
		label = 'Teams can see Service Statistics Page(s)',
		initial = True,
		required = False
	)
	teamsViewServiceStatusEnabled = BooleanField(
		label = 'Teams can see Service Status Page(s)',
		initial = True,
		required = False
	)
	teamsViewInjectsEnabled = BooleanField(
		label = 'Teams can see Inject Page(s)',
		initial = True,
		required = False
	)
	teamsViewIncidentResponseEnabled = BooleanField(
		label = 'Teams can see Incident Response Page(s)',
		initial = True,
		required = False
	)