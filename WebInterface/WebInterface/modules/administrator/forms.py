from django.forms import Form
from django.forms import CharField
from django.forms import TextInput
from django.forms import NumberInput
from django.forms import ChoiceField
from django.forms import Select
from django.forms import PasswordInput
from WebInterface.utils import makeApiRequest
from cssefclient.cssefclient import OrganizationGet as ApiOrganizationGet

class CreateOrganizationForm(Form):
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
		widget = NumberInput(attrs={'class': 'form-control'}),
		required = False
	)
	maxCompetitions = CharField(
		label = 'Maximum Competitions',
		widget = NumberInput(attrs={'class': 'form-control'}),
		required = False
	)

def getOrganizationChoices():
	organizationChoices = []
	output = makeApiRequest(ApiOrganizationGet, {})
	for i in output['content']:
		organizationChoices.append((i['id'], i['name']))
	return organizationChoices

class CreateUserForm(Form):
	def __init__(self, *args, **kwargs):
		super(CreateUserForm, self).__init__(*args, **kwargs)
		self.fields['organization'].choices = getOrganizationChoices()

	def getOrganizationChoices():
		organizationChoices = []
		output = makeApiRequest(ApiOrganizationGet, {})
		for i in output['content']:
			organizationChoices.append((i['id'], i['name']))
		return organizationChoices

	name = CharField(
		label = 'Name',
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
	organization = ChoiceField(
		label = 'Organization',
		choices = [],
		widget = Select(attrs={'class':'form-control', 'required': 'True'})
	)