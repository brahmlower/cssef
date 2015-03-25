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
	competitionId = AutoField(primary_key = True)
	name = CharField(max_length = 50)
	url = CharField(max_length = 50)
	descriptionShort = CharField(max_length = 300)
	descriptionFull = TextField(max_length = 1000)
	datetimeDisplay = DateTimeField()
	datetimeStart = DateTimeField()
	datetimeFinish = DateTimeField()
	scoringEnabled = BooleanField(default = True)
	scoringInterval = PositiveIntegerField(null = True)
	scoringIntervalUncertainty = PositiveIntegerField(null = True)
	scoringMethod = CharField(max_length = 20, null = True, blank = True)
	scoringSlaEnabled = BooleanField(default = True)
	scoringSlaThreashold = PositiveIntegerField(null = True)
	scoringSlaPenalty = PositiveIntegerField(null = True)
	servicesEnabled = BooleanField(default = True)
	teamsViewRankingEnabled = BooleanField(default = True)
	teamsViewScoreboardEnabled = BooleanField(default = True)
	teamsViewServiceStatisticsEnabled = BooleanField(default = True)
	teamsViewServiceStatusEnabled = BooleanField(default = True)
	teamsViewInjectsEnabled = BooleanField(default = True)
	teamsViewIncidentResponseEnabled = BooleanField(default = True)

class Team(Model):
	teamId = AutoField(primary_key = True)
	competitionId = PositiveIntegerField()
	last_login = DateTimeField(default = timezone.now())
	teamname = CharField(max_length = 30)
	username = CharField(max_length = 30)
	password = CharField(max_length = 64)
	networkaddr = CharField(max_length = 30)
	scoreConfigurations = TextField(max_length = 500, default = "{}")

	def is_authenticated(self):
		return True

class Plugin(Model):
	pluginId = AutoField(primary_key = True)
	name = CharField(max_length = 20)
	description = TextField(max_length = 500)

class Service(Model):
	serviceId = AutoField(primary_key = True)
	competitionId = PositiveIntegerField()
	plugin = ForeignKey(Plugin, unique = False)
	name = CharField(max_length = 30)
	description = CharField(max_length = 200)
	datetimeStart = DateTimeField()
	datetimeFinish = DateTimeField()
	points = PositiveIntegerField()
	connectIp = BooleanField(default = True)
	connectDisplay = CharField(max_length = 15)
	networkLocation = CharField(max_length = 15)
	defaultPort = PositiveIntegerField()

	# Service object now has the ability to score itself
	def score(self, team_obj):
		instance = self.load_plugin()
		score_obj = instance.score(team_obj)
		score_obj.datetime = timezone.now()
		return score_obj

	def load_plugin(self):
		module_name = Document.objects.get(servicemodule = self.servicemodule).filename.split(".")[0]
		module = __import__(settings.CONTENT_PLUGGINS_PATH.replace('/','.')[1:] + module_name, fromlist=[module_name])
		return getattr(module, module_name)(self)

class Score(Model):
	scoreId = AutoField(primary_key = True)
	competitionId = PositiveIntegerField()
	teamId = PositiveIntegerField()
	serviceId = PositiveIntegerField()
	datetime = DateTimeField(default = timezone.now())
	value = PositiveIntegerField()
	message = CharField(max_length = 100)

class Inject(Model):
	injectId = AutoField(primary_key = True)
	competitionId = PositiveIntegerField()
	datetimeDelivery = DateTimeField()
	datetimeResponseDue = DateTimeField(null = True, blank = True)
	datetimeResponseClose = DateTimeField(null = True, blank = True)
	requireResponse = BooleanField(default=False)
	title = CharField(max_length = 50)
	body = CharField(max_length = 1000)

class User(Model):
	last_login = DateTimeField(default = timezone.now())
	userId = AutoField(primary_key = True)
	username = CharField(max_length = 20)
	password = CharField(max_length = 64)

	def is_authenticated(self):
		return True

class InjectResponse(Model):
	injectResponseId = AutoField(primary_key = True)
	competitionId = PositiveIntegerField()
	teamId = PositiveIntegerField()
	injectId = PositiveIntegerField()
	datetime = DateTimeField(default = timezone.now())
	content = TextField(max_length = 1000)

class IncidentResponse(Model):
	incidentResponseId = AutoField(primary_key = True)
	competitionId = PositiveIntegerField()
	teamId = PositiveIntegerField()
	replyto = IntegerField()
	datetime = DateTimeField(default = timezone.now())
	subject = CharField(max_length = 100, default = "")
	content = TextField(max_length = 1000)

class Document(Model):
	documentId = AutoField(primary_key = True)
	inject = ForeignKey(Inject, null = True, blank = True, unique = False)
	injectresponse = ForeignKey(InjectResponse, null = True, blank = True, unique = False)
	incidentresponse = ForeignKey(IncidentResponse, null = True, blank = True, unique = False)
	plugin = ForeignKey(Plugin, null = True, blank = True, unique = True)
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

class Organization(Model):
	organizationId = AutoField(primary_key = True)
	name = CharField(max_length = 256, blank = False, null = False)
