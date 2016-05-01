from django.forms import Form
from django.forms import TextInput
from django.forms import Textarea
from django.forms import CharField
from django.forms import HiddenInput

class DeletePluginCompForm(Form):
	pkid = CharField(
		widget = HiddenInput()
	)

class CreatePluginCompForm(Form):
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
