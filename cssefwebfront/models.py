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
from django.utils import timezone
from cssefwebfront import settings

class Competition(Model):
	compid = AutoField(primary_key = True)
	compname = CharField(max_length = 50)
	compurl = CharField(max_length = 50)
	description_short = CharField(max_length = 300)
	description_full = TextField(max_length = 1000)
	datetime_display = DateTimeField()
	datetime_start = DateTimeField()
	datetime_finish = DateTimeField()
	scoring_enabled = BooleanField(default = True)
	scoring_interval = PositiveIntegerField(null = True)
	scoring_interval_uncty = PositiveIntegerField(null = True)
	scoring_method = CharField(max_length = 20, null = True, blank = True)
	services_enabled = BooleanField(default = True)
	teams_view_ranking_enabled = BooleanField(default = True)
	teams_view_scoreboard_enabled = BooleanField(default = True)
	teams_view_servicestatistics_enabled = BooleanField(default = True)
	teams_view_servicestatus_enabled = BooleanField(default = True)
	teams_view_injects_enabled = BooleanField(default = True)
	teams_view_incidentresponse_enabled = BooleanField(default = True)

class Team(Model):
	teamid = AutoField(primary_key = True)
	compid = PositiveIntegerField()
	last_login = DateTimeField(default = timezone.now())
	teamname = CharField(max_length = 30)
	username = CharField(max_length = 30)
	password = CharField(max_length = 64)
	networkaddr = CharField(max_length = 30)
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
	datetime_start = DateTimeField()
	datetime_finish = DateTimeField()
	points = PositiveIntegerField()
	connectip = BooleanField(default = True)
	connect_display = CharField(max_length = 15)
	networkloc = CharField(max_length = 15)
	defaultport = PositiveIntegerField()

	# Service object now has the ability to score itself
	def score(self, team_obj):
		instance = self.load_pluggin()
		score_obj = instance.score(team_obj)
		score_obj.datetime = timezone.now()
		return score_obj

	def load_pluggin(self):
		module_name = Document.objects.get(servicemodule = self.servicemodule).filename.split(".")[0]
		module = __import__(settings.CONTENT_PLUGGINS_PATH.replace('/','.')[1:] + module_name, fromlist=[module_name])
		return getattr(module, module_name)(self)

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
	content_type = CharField(max_length = 64, null = True)
	filehash = CharField(max_length = 32)
	filepath = CharField(max_length = 256)
	filename = CharField(max_length = 64)
	urlencfilename = CharField(max_length = 128)

	def get_cleaned_content_type(self):
		if not self.content_type:
			return'application/force-download'
		else:
			return self.content_type
