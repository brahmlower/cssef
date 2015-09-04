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
#from django.contrib.auth.models import User
from django.utils import timezone
import settings
from ScoringEngine.models import *

class Competition(Model):
	competitionId = AutoField(primary_key = True)
	organization = PositiveIntegerField()
	name = CharField(max_length = 50)
	url = CharField(max_length = 50)
	description = CharField(max_length = 1000, default = '')
	datetimeDisplay = DateTimeField(null = True)
	datetimeStart = DateTimeField(null = True)
	datetimeFinish = DateTimeField(null = True)
	autoStart = BooleanField(default = False)
	scoringEnabled = BooleanField(default = True)
	scoringInterval = PositiveIntegerField(null = True)
	scoringIntervalUncertainty = PositiveIntegerField(null = True)
	scoringMethod = CharField(max_length = 20, null = True, blank = True)	# set to either CIDR or domain name
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

	def sleepScoreInterval(self):
		min_seconds = score_delay - score_delay_uncert
		max_seconds = score_delay + score_delay_uncert
		sleep(randrange(min_seconds, max_seconds))

class Team(Model):
	teamId = AutoField(primary_key = True)
	competitionId = PositiveIntegerField()
	last_login = DateTimeField(default = timezone.now())
	name = CharField(max_length = 30)
	username = CharField(max_length = 30)
	password = CharField(max_length = 64)
	networkCidr = CharField(max_length = 30)
	scoreConfigurations = TextField(max_length = 500, default = "{}")
	# ^ With regard to score configuration
	# holy shitballs! Use a serialziser for this!
	# teh scoring engine will have an object to interpret this, and then when it needs to save the object
	# or load it, it will be serialized and then saved to the database. Wehnt htis is read from the database,
	# it is de-serialized!

	def is_authenticated(self):
		return True

class Score(Model):
	scoreId = AutoField(primary_key = True)
	competitionId = PositiveIntegerField()
	teamId = PositiveIntegerField()
	#serviceId = PositiveIntegerField()
	datetime = DateTimeField(default = timezone.now())
	value = PositiveIntegerField()
	message = CharField(max_length = 100)

class User(Model):
	last_login = DateTimeField(default = timezone.now())
	userId = AutoField(primary_key = True)
	name = CharField(max_length = 20)
	username = CharField(max_length = 20)
	password = CharField(max_length = 64)
	description = CharField(max_length = 256)
	organizationId = PositiveIntegerField()

	def is_authenticated(self):
		return True

class Inject(Model):
	injectId = AutoField(primary_key = True)
	competitionId = PositiveIntegerField()
	requireResponse = BooleanField(default = True)
	manualDelivery = BooleanField(default = False)
	datetimeDelivery = DateTimeField(null = True, blank = True)
	datetimeResponseDue = DateTimeField(null = True, blank = True)
	datetimeResponseClose = DateTimeField(null = True, blank = True)
	title = CharField(max_length = 50)
	body = CharField(max_length = 1000)

class InjectResponse(Model):
	injectResponseId = AutoField(primary_key = True)
	competitionId = PositiveIntegerField()
	teamId = PositiveIntegerField()
	injectId = PositiveIntegerField()
	datetime = DateTimeField(default = timezone.now())
	content = TextField(max_length = 1000)

class Incident(Model):
	incidentId = AutoField(primary_key = True)
	competitionId = PositiveIntegerField()
	teamId = PositiveIntegerField()
	datetime = DateTimeField(default = timezone.now())
	subject = CharField(max_length = 100, default = "")
	content = TextField(max_length = 1000)

class IncidentResponse(Model):
	incidentResponseId = AutoField(primary_key = True)
	competitionId = PositiveIntegerField()
	teamId = PositiveIntegerField()
	incidentId = PositiveIntegerField()
	replyTo = IntegerField()
	datetime = DateTimeField(default = timezone.now())
	subject = CharField(max_length = 100, default = "")
	content = TextField(max_length = 1000)

class Organization(Model):
	organizationId = AutoField(primary_key = True)
	deleteable = BooleanField(default = True)
	name = CharField(max_length = 256, blank = False, null = False)
	url = CharField(max_length = 256, blank = False, null = False)
	description = TextField(max_length = 1000, default = '')
	maxMembers = PositiveIntegerField(default = 0)
	maxCompetitions = PositiveIntegerField(default = 0)
	numMembers = PositiveIntegerField(default = 0)
	numCompetitions = PositiveIntegerField(default = 0)

class Document(Model):
	documentId = AutoField(primary_key = True)
	inject = ForeignKey(Inject, null = True, blank = True, unique = False)
	injectResponse = ForeignKey(InjectResponse, null = True, blank = True, unique = False)
	incidentResponse = ForeignKey(IncidentResponse, null = True, blank = True, unique = False)
	plugin = ForeignKey(Plugin, null = True, blank = True, unique = True)
	contentType = CharField(max_length = 64, null = True)
	fileHash = CharField(max_length = 32)
	filePath = CharField(max_length = 256)
	filename = CharField(max_length = 64)
	urlEncodedFilename = CharField(max_length = 128)

	def get_cleaned_content_type(self):
		if not self.content_type:
			return'application/force-download'
		else:
			return self.content_type
