from django import forms
from django.db.models import Model
from django.db.models import CharField
from django.db.models import BooleanField
from django.db.models import TextField
from django.db.models import BooleanField
from django.db.models import AutoField
from django.db.models import DateTimeField
from django.db.models import PositiveIntegerField
from django.forms.widgets import PasswordInput
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

class Competition(Model):
	compid = AutoField(primary_key = True)
	compname = CharField(max_length = 50)		# Full name of the competition
	compurl = CharField(max_length = 25)		# string ID of the competition, used in url
	shrt_desc = CharField(max_length = 300)		# A short description of the competition - abreviated version of description field
	full_desc = TextField(max_length = 1000)	# A full description of the competition, what it's about, what the goals are and whatnot
	viewable = BooleanField()					# Boolean indicating if it's published on the public competition list
	autodisplay = BooleanField()
	displaytime = PositiveIntegerField()
	#starttime = PositiveIntegerField()
	#finishtime = PositiveIntegerField()
	# inject_ids = "" # String of inject ids
	score_delay = PositiveIntegerField()
	score_delay_uncert = PositiveIntegerField()

class Team(Model):
	teamid = AutoField(primary_key = True)
	compid = PositiveIntegerField()
	last_login = DateTimeField(default = timezone.now)
	teamname = CharField(max_length = 30)
	password = CharField(max_length = 64)
	domainname = CharField(max_length = 30)
	score_configs = TextField(max_length = 500)#, default = "{}")

	def is_authenticated(self):
		return True

class Service(Model):
	servid = AutoField(primary_key = True)
	compid = PositiveIntegerField()
	module = CharField(max_length = 10)
	name = CharField(max_length = 30)
	desc = CharField(max_length = 200)
	config = CharField(max_length = 1000)
	points = PositiveIntegerField()
	subdomain = CharField(max_length = 20)

class Score(Model):
	scorid = AutoField(primary_key = True)
	compid = PositiveIntegerField()
	teamid = PositiveIntegerField()
	servid = PositiveIntegerField()
	datetime = DateTimeField()
	value = PositiveIntegerField()

class Inject(Model):
	ijctid = AutoField(primary_key = True)
	compid = PositiveIntegerField()
	title = CharField(max_length = 50)
	body = CharField(max_length = 1000)

class Admins(Model):
	last_login = DateTimeField(default = timezone.now)
	userid = AutoField(primary_key = True)
	username = CharField(max_length = 20)
	password = CharField(max_length = 64)

# class Teams(Model): #Why isn't this User?
# 	userid = AutoField(primary_key=True)
# 	username = CharField(max_length=20)
# 	password = CharField(max_length=64)
# 	competitions = CharField(max_length=100)




