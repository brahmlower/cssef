from django import forms
from django.db.models import Model
from django.db.models import CharField
from django.db.models import BooleanField
from django.db.models import TextField
from django.db.models import AutoField
from django.db.models import DateTimeField
from django.db.models import DateField
from django.db.models import TimeField
from django.db.models import FileField
from django.db.models import IntegerField
from django.db.models import PositiveIntegerField
from django.db.models import ForeignKey
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import User
#from datetime import datetime
from django.utils import timezone

class Competition(Model):
	compid = AutoField(primary_key = True)
	compname = CharField(max_length = 50)		# Full name of the competition
	compurl = CharField(max_length = 50)		# string ID of the competition, used in url
	shrt_desc = CharField(max_length = 300)		# A short description of the competition - abreviated version of description field
	full_desc = TextField(max_length = 1000)	# A full description of the competition, what it's about, what the goals are and whatnot
	viewable = BooleanField(default = False)	# Boolean indicating if it's published on the public competition list
	autodisplay = BooleanField(default = False)
	dt_display = DateTimeField()
	dt_start = DateTimeField()
	dt_finish = DateTimeField()
	score_delay = PositiveIntegerField()
	score_delay_uncert = PositiveIntegerField()

class Team(Model):
	teamid = AutoField(primary_key = True)
	compid = PositiveIntegerField()
	last_login = DateTimeField(default = timezone.now())
	teamname = CharField(max_length = 30)
	username = CharField(max_length = 30)
	password = CharField(max_length = 64)
	domainname = CharField(max_length = 30)
	score_configs = TextField(max_length = 500, default = "{}")

	def is_authenticated(self):
		return True

class ServiceModule(Model):
	servmdulid = AutoField(primary_key = True)
	modulename = CharField(max_length = 20)
	description = TextField(max_length = 500)

class Service(Model):
	servid = AutoField(primary_key = True)
	compid = PositiveIntegerField()
	servicemodule = ForeignKey(ServiceModule, unique = False)
	name = CharField(max_length = 30)
	description = CharField(max_length = 200)
	points = PositiveIntegerField()
	connectip = BooleanField()
	connect_display = CharField(max_length = 15)
	networkloc = CharField(max_length = 15)
	defaultport = PositiveIntegerField()
	#configuration = CharField(max_length = 1000, default = "{}")

class Score(Model):
	scorid = AutoField(primary_key = True)
	compid = PositiveIntegerField()
	teamid = PositiveIntegerField()
	servid = PositiveIntegerField()
	datetime = DateTimeField(default = timezone.now())
	value = PositiveIntegerField()
	message = CharField(max_length = 100)

class Inject(Model):
	ijctid = AutoField(primary_key = True)
	compid = PositiveIntegerField()
	dt_delivery = DateTimeField()
	dt_response_due = DateTimeField()
	dt_response_close = DateTimeField()
	title = CharField(max_length = 50)
	body = CharField(max_length = 1000)

class Admin(Model):
	last_login = DateTimeField(default = timezone.now())
	userid = AutoField(primary_key = True)
	username = CharField(max_length = 20)
	password = CharField(max_length = 64)

	def is_authenticated(self):
		return True

class InjectResponse(Model):
	ijctrespid = AutoField(primary_key = True)
	compid = PositiveIntegerField()
	teamid = PositiveIntegerField()
	ijctid = PositiveIntegerField()
	datetime = DateTimeField(default = timezone.now())
	textentry = TextField(max_length = 1000)

class IncidentResponse(Model):
	intrspid = AutoField(primary_key = True)
	compid = PositiveIntegerField()
	teamid = PositiveIntegerField()
	replyto = IntegerField()
	datetime = DateTimeField(default = timezone.now())
	subject = CharField(max_length = 100, default = "")
	textentry = TextField(max_length = 1000)

class Document(Model):
	docid = AutoField(primary_key = True)
	inject = ForeignKey(Inject, null = True, blank = True, unique = False)
	injectresponse = ForeignKey(InjectResponse, null = True, blank = True, unique = False)
	incidentresponse = ForeignKey(IncidentResponse, null = True, blank = True, unique = False)
	servicemodule = ForeignKey(ServiceModule, null = True, blank = True, unique = True)
	filehash = CharField(max_length = 32)
	filepath = CharField(max_length = 256)
	filename = CharField(max_length = 64)
	urlencfilename = CharField(max_length = 128)


