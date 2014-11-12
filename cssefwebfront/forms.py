from django.forms import ModelForm
from django.forms import TextInput
from django.forms import Textarea
from django.forms import CheckboxInput
from django.forms import NumberInput
from django.forms import Select
from django.forms import ChoiceField
from django.forms.widgets import PasswordInput
from models import Competition
from models import Service
from models import Inject
from models import Admins
from models import Team

class CreateCompetitionForm(ModelForm):
	class Meta:
		model = Competition
		fields = ['compname','compurl','shrt_desc','full_desc', 'viewable','autodisplay','displaytime', 'score_delay', 'score_delay_uncert']
		labels = {
			'compname': ('Competition Name'),
			'compurl': ('Competition URL Value'),
			'shrt_desc': ('Short Description'),
			'full_desc': ('Description'),
			'viewable': ('Visible'),
			'autodisplay': ('Auto Display'),
			'displaytime': ('Display Time'),
			'score_delay': ('Scoring Interval'),
			'score_delay_uncert': ('Scoring Interval Uncertanty')
		}
		widgets = {
			'compname': TextInput(attrs={'class':'form-control', 'required': True}),
			'compurl': TextInput(attrs={'class':'form-control', 'required': True}),
			'shrt_desc': Textarea(attrs={'class': 'form-control','rows':3, 'required': True}),
			'full_desc': Textarea(attrs={'class':'form-control', 'required': True}),
			'viewable': CheckboxInput(attrs={'class':'form-control checkbox', 'required': False}),
			'autodisplay': CheckboxInput(attrs={'class':'form-control checkbox', 'required': False}),
			'displaytime': NumberInput(attrs={'class':'form-control', 'required': False}),
			'score_delay': NumberInput(attrs={'class':'form-control', 'required': True}),
			'score_delay_uncert': NumberInput(attrs={'class':'form-control', 'required': True}),
		}

class CreateTeamForm(ModelForm):
	class Meta:
		model = Team
		fields = ['teamname','password','domainname','compid']
		labels = {
			'compid': ('Competition'),
			'teamname': ('Teamname'),
			'password': ('Password'),
			'domainname': ('Domain Name'),
		}
		widgets = {
			'teamname': TextInput(attrs={'class':'form-control'}),
			'password': TextInput(attrs={'class':'form-control'}),
			'domainname': TextInput(attrs={'class':'form-control'}),
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
	class Meta:
		model = Inject
		fields = ['title', 'body']
		label = {
			'title': ('Title'),
			'body': ('Content'),
		}
		widgets = {
			'title': TextInput(attrs={'class':'form-control'}),
			'body': Textarea(attrs={'class':'form-control'}),
		}

class AdminLoginForm(ModelForm):
	class Meta:
		model = Admins
		fields = ['username','password']
		labels = {
			'username': ('Username'),
			'password': ('Password'),
		}
		widgets = {
			'username': TextInput(attrs={'class':'form-control', 'required': True}),
			'password': PasswordInput(attrs={'class':'form-control', 'required': True}),
		}

class TeamLoginForm(ModelForm):
	class Meta:
		model = Team
		fields = ['teamname','password','compid']
		labels = {
			'teamname': ('Teamname'),
			'password': ('Password'),
			'compid': ('Competition')
		}
		widgets = {
			'teamname': TextInput(attrs={'class':'form-control', 'required': True}),
			'password': PasswordInput(attrs={'class':'form-control', 'required': True}),
			'compid': Select(attrs={'class':'form-control', 'required': True}),
		}

		def __init__(self, *args, **kwargs):
			super(TeamLoginForm, self).__init__(*args, **kwargs)
			comp_list = []
			comps = Competition.objects.all()
			for i in comps:
				comp_list.append((i.compid, i.compname))
			print comp_list
