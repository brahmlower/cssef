from django.forms import Form
from django.forms import TextInput
from django.forms import Textarea
from django.forms import FileField
from django.forms import CharField
from django.forms import IntegerField
from django.forms import HiddenInput
from django.forms.widgets import PasswordInput

# class DeleteObject(Form):
# 	objectId = IntegerField(widget = HiddenInput())
# 	def __init__(self, objectId):
# 		super(DeleteObject, self).__init__()
# 		self.fields['objectId'].initial = objectId

class DeleteObjectForm(Form):
	pkid = CharField(widget = HiddenInput())

class LoginSiteAdmin(Form):
	username = CharField(label = 'Username', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	password = CharField(label = 'Password', widget = PasswordInput(attrs={'class':'form-control', 'required': True}))

class LoginOrganizationUser(Form):
	username = CharField(label = 'Username', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	password = CharField(label = 'Password', widget = PasswordInput(attrs={'class':'form-control', 'required': True}))

class CreatePlugin(Form):
	name = CharField(label = 'Name', widget = TextInput(attrs={'class':'form-control', 'required': True}))
	description = CharField(label = 'Description', widget = Textarea(attrs={'class':'form-control', 'required': True}))
	pluginFile = FileField(label = "File Upload", required = False)
