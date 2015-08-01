from django.db.models import Model
from django.db.models import CharField
from django.db.models import BooleanField
from django.db.models import TextField
from django.db.models import AutoField
from django.db.models import DateTimeField
from django.db.models import PositiveIntegerField
from django.db.models import ForeignKey
#from ScoringEngine.ScoringEngine.models import Document
#import settings

class Plugin(Model):
	pluginId = AutoField(primary_key = True)
	name = CharField(max_length = 20)
	description = TextField(max_length = 500)

	def getModuleName(self):
		return Document.objects.get(servicemodule = self.servicemodule).filename.split(".")[0]

	def getImportPath(self, moduleName = None):
		if moduleName:
			#return settings.CONTENT_PLUGGINS_PATH.replace('/','.')[1:] + moduleName
			return ""
		else:
			return self.getImportPath(self.getModuleName())

class Service(Model):
	serviceId = AutoField(primary_key = True)
	competitionId = PositiveIntegerField()
	plugin = ForeignKey(Plugin, unique = False)
	name = CharField(max_length = 30)
	description = CharField(max_length = 200)
	manualStart = BooleanField(default = True)
	datetimeStart = DateTimeField(null = True)
	datetimeFinish = DateTimeField(null = True)
	points = PositiveIntegerField()
	machineIp = CharField(max_length = 15)
	machineFqdn = CharField(max_length = 15)
	defaultPort = PositiveIntegerField()

	# Service object now has the ability to score itself
	def score(self, team):
		instance = self.loadPlugin()
		scoreInstance = instance.score(team)
		scoreInstance.datetime = timezone.now()
		scoreInstance.teamId = team.teamId
		scoreInstance.serviceId = self.serviceId
		scoreInstance.competitionId = self.competitionId
		return score_obj

	def loadPlugin(self):
		#moduleName = Document.objects.get(servicemodule = self.servicemodule).filename.split(".")[0]
		#module = __import__(settings.CONTENT_PLUGGINS_PATH.replace('/','.')[1:] + moduleName, fromlist=[moduleName])
		moduleName = self.plugin.getModuleName()
		module = __import__(self.plugin.getImportPath(moduleName), fromlist=[moduleName])
		return getattr(module, moduleName)(self)