from django.forms import Form
from django.forms import ModelForm
from django.forms import TextInput
from django.forms import Textarea
from django.forms import CheckboxInput
from django.forms import NumberInput
from django.forms import Select
from django.forms import ChoiceField
from django.forms import FileField
#from django.forms import SplitDateTimeWidget
from django.forms import ModelChoiceField
from django.forms import DateInput
from django.forms import TimeInput
from django.forms.widgets import PasswordInput
from models import Competition
from models import InjectResponse
from models import IncidentResponse
from models import Service
from models import Inject
from models import Admin
from models import Team
from django.utils import timezone

class CreateCompetitionForm(ModelForm):
	class Meta:
		model = Competition
		fields = ['compname', 'compurl', 'shrt_desc', 'full_desc', 'viewable', 'autodisplay', 'dt_display', 'dt_start', 'dt_finish', 'score_delay', 'score_delay_uncert']
		labels = {
			'compname': ('Competition Name'),
			'compurl': ('Competition URL'),
			'shrt_desc': ('Short Description'),
			'full_desc': ('Description'),
			'viewable': ('Visible'),
			'autodisplay': ('Auto Display'),
			'dt_display': ('Viewable Date'),
			'dt_start': ('Start Time'),
			'dt_finish': ('Finish Time'),
			'score_delay': ('Scoring Interval'),
			'score_delay_uncert': ('Scoring Interval Uncertanty')
		}
		widgets = {
			'compname': TextInput(attrs={'class':'form-control', 'required': True}),
			'compurl': TextInput(attrs={'class':'form-control', 'required': True}),
			'shrt_desc': Textarea(attrs={'class': 'form-control','rows':3, 'required': True}),
			'full_desc': Textarea(attrs={'class':'form-control', 'required': True}),
			'viewable': CheckboxInput(attrs={'class':'form-control checkbox'}),
			'autodisplay': CheckboxInput(attrs={'class':'form-control checkbox'}),
			'dt_display': TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}),
			'dt_start': TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}),
			'dt_finish': TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}),
			'score_delay': NumberInput(attrs={'class':'form-control', 'required': True}),
			'score_delay_uncert': NumberInput(attrs={'class':'form-control', 'required': True}),
		}

class CreateTeamForm(ModelForm):
	class Meta:
		model = Team
		fields = ['teamname','password','domainname','compid','score_configs']
		labels = {
			'compid': ('Competition'),
			'teamname': ('Teamname'),
			'password': ('Password'),
			'domainname': ('Domain Name'),
			'score_configs': ('Score Configurations'),
		}
		widgets = {
			'teamname': TextInput(attrs={'class':'form-control'}),
			'password': TextInput(attrs={'class':'form-control'}),
			'domainname': TextInput(attrs={'class':'form-control'}),
			'score_configs': Textarea(attrs={'class':'form-control'}),
		}

class CreateServiceForm(ModelForm):
	class Meta:
		model = Service
		fields = ['compid', 'module', 'name', 'desc', 'config', 'points', 'subdomain']
		labels = {
			'compid': ('Competition'),
			'module': ('Module'),
			'name': ('Name'),
			'desc': ('Description'),
			'points': ('Points'),
			'config': ('Json Config'),
			'subdomain': ('Subdomain'),
		}
		widgets = {
			'compid': TextInput(attrs={'class':'form-control'}),
			'module': TextInput(attrs={'class':'form-control'}),
			'name': TextInput(attrs={'class':'form-control'}),
			'points': NumberInput(attrs={'class':'form-control'}),
			'desc': Textarea(attrs={'class':'form-control'}),
			'config': Textarea(attrs={'class':'form-control'}),
			'subdomain': TextInput(attrs={'class':'form-control'}),
		}

class CreateInjectForm(ModelForm):
	docfile = FileField(label = "File Upload", required = False)
	class Meta:
		model = Inject
		fields = ['compid','title', 'body', 'dt_delivery', 'dt_response_due', 'dt_response_close']
		labels = {
			'title': ('Title'),
			'body': ('Content'),
			'dt_delivery': ('Delivery Time'),
			'dt_response_due': ('Response Due Time'),
			'dt_response_close': ('Response Close Time')
		}
		widgets = {
			'title': TextInput(attrs={'class':'form-control'}),
			'body': Textarea(attrs={'class':'form-control'}),
			'dt_delivery': TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}),
			'dt_response_due': TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"}),
			'dt_response_close': TextInput(attrs={'class':'form-control', 'data-date-format': "YYYY-MM-DD HH:mm"})
		}

class AdminLoginForm(ModelForm):
	class Meta:
		model = Admin
		fields = ['username', 'password']
		labels = {
			'username': ('Username'),
			'password': ('Password'),
		}
		widgets = {
			'username': TextInput(attrs={'class':'form-control', 'required': True}),
			'password': PasswordInput(attrs={'class':'form-control', 'required': True}),
		}

class TeamLoginForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(TeamLoginForm, self).__init__(*args, **kwargs)
		tuple_list = []
		for i in Competition.objects.filter(dt_start__lte = timezone.now(), dt_finish__gt = timezone.now()):
			tuple_list.append((i.compid, i.compname))
		self.fields['compid'].choices = tuple_list

	compid = ChoiceField(label = "Competition", choices = [], widget = Select(attrs={'class':'form-control', 'required': True}))
	class Meta:
		model = Team
		fields = ['teamname', 'password', 'compid']
		labels = {
			'teamname': ('Team Name'),
			'password': ('Password')
		}
		widgets = {
			'teamname': TextInput(attrs={'class':'form-control', 'required': True}),
			'password': PasswordInput(attrs={'class':'form-control', 'required': True})
		}

class InjectResponseForm(ModelForm):
	docfile = FileField(label = "File Upload", required = False)
	class Meta:
		model = InjectResponse
		fields = ['textentry']
		labels = {
			'textentry': ('Text Entry')
		}
		widgets = {
			'textentry': Textarea(attrs={'class':'form-control'})
		}

class IncidentResponseForm(ModelForm):
	docfile = FileField(label = "File Upload", required = False)
	class Meta:
		model = IncidentResponse
		fields = ['textentry','subject']
		labels = {
			'subject': ('Subject'),
			'textentry': ('Text Entry')
		}
		widgets = {
			'subject': TextInput(attrs={'class':'form-control'}),
			'textentry': Textarea(attrs={'class':'form-control'})
		}

class IncidentResponseReplyForm(ModelForm):
	docfile = FileField(label = "File Upload", required = False)
	class Meta:
		model = IncidentResponse
		fields = ['textentry']
		labels = {
			'textentry': ('Text Entry')
		}
		widgets = {
			'textentry': Textarea(attrs={'class':'form-control'}),
		}

