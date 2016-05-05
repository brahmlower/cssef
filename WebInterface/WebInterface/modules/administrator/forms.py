from django.forms import Form
from django.forms import CharField
from django.forms import TextInput
from django.forms import NumberInput
from django.forms import ChoiceField
from django.forms import BooleanField
from django.forms import Select
from django.forms import PasswordInput
from django.forms import HiddenInput
from WebInterface.utils import makeApiRequest

class CreateOrganizationForm(Form):
	name = CharField(
		label = 'Organization Name',
		widget = TextInput(attrs={'class':'form-control'}),
		required = True
	)
	url = CharField(
		label = 'Organization URL',
		widget = TextInput(attrs={'class':'form-control'}),
		required = True
	)
	description = CharField(
		label = 'Description',
		widget = TextInput(attrs={'class':'form-control'}),
		required = False
	)
	max_members = CharField(
		label = 'Maximum Members',
		widget = NumberInput(attrs={'class': 'form-control'}),
		required = False
	)
	max_competitions = CharField(
		label = 'Maximum Competitions',
		widget = NumberInput(attrs={'class': 'form-control'}),
		required = False
	)
	can_add_users = BooleanField(
		label = 'Can Create Users',
		initial = True,
		required = False
	)
	can_delete_users = BooleanField(
		label = 'Can Delete Users',
		initial = True,
		required = False
	)
	can_add_competitions = BooleanField(
		label = 'Can Create Competitions',
		initial = True,
		required = False
	)
	can_delete_competitions = BooleanField(
		label = 'Can Delete Competitions',
		initial = True,
		required = False
	)

class DeleteOrganizationForm(Form):
	pkid = CharField(
		widget = HiddenInput()
	)

def getOrganizationChoices():
	organizationChoices = []
	output = makeApiRequest('organizationget', {})
	for i in output['content']:
		organizationChoices.append((i['id'], i['name']))
	return organizationChoices

class CreateUserForm(Form):
	def __init__(self, *args, **kwargs):
		super(CreateUserForm, self).__init__(*args, **kwargs)
		self.fields['organization'].choices = getOrganizationChoices()

	name = CharField(
		label = 'Name',
		widget = TextInput(attrs={'class':'form-control'})
	)
	username = CharField(
		label = 'Username',
		widget = TextInput(attrs={'class':'form-control'})
	)
	password = CharField(
		label = 'Password',
		widget = PasswordInput(attrs={'class':'form-control'})
	)
	organization = ChoiceField(
		label = 'Organization',
		choices = [],
		widget = Select(attrs={'class':'form-control'})
	)

class DeleteUserForm(Form):
	pkid = CharField(
		widget = HiddenInput()
	)