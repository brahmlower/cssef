from cssefserver.utils import ModelWrapper
from cssefserver.account.api import Organization
from cssefserver.account.errors import MaxCompetitionsReached
from cssefcdc.models import Competition as CompetitionModel
from cssefcdc.models import Team as TeamModel
from cssefcdc.models import Score as ScoreModel
from cssefcdc.models import Inject as InjectModel
from cssefcdc.models import InjectResponse as InjectResponseModel
from cssefcdc.models import Incident as IncidentModel
from cssefcdc.models import IncidentResponse as IncidentResponseModel
from cssefcdc.models import ScoringEngine as ScoringEngineModel
from cssefcdc.models import Plugin as PluginModel
from cssefcdc.models import Service as ServiceModel

class Plugin(ModelWrapper):
	model_object = PluginModel
	fields = [
		'name',
		'description'
	]

	@property
	def name(self):
		return self.model.name

	@name.setter
	def name(self, value):
		self.model.name = value
		self.db.commit()

	@property
	def description(self):
		return self.model.description

	@description.setter
	def description(self, value):
		self.model.description = value
		self.db.commit()

	def getModuleName(self):
		#return Document.objects.get(servicemodule = self.servicemodule).filename.split(".")[0]
		pass

	def getImportPath(self, moduleName = None):
		if moduleName:
			#return settings.CONTENT_PLUGGINS_PATH.replace('/','.')[1:] + moduleName
			return ""
		else:
			return self.getImportPath(self.getModuleName())

class Service(ModelWrapper):
	model_objectmodel_object = ServiceModel
	fields = [
		'name',
		'description',
		'manualStart',
		'datetimeStart',
		'datetimeFinish',
		'points',
		'machineIp',
		'machineFqdn',
		'defaultPort'
	]

	@property
	def name(self):
		return self.model.name

	@name.setter
	def name(self, value):
		self.model.name = value
		self.db.commit()

	@property
	def description(self):
		return self.model.description

	@description.setter
	def description(self, value):
		self.model.description = value
		self.db.commit()

	@property
	def manualStart(self):
		return self.model.manualStart

	@manualStart.setter
	def manualStart(self, value):
		self.model.manualStart = value
		self.db.commit()

	@property
	def datetimeStart(self):
		return self.model.datetimeStart

	@datetimeStart.setter
	def datetimeStart(self, value):
		self.model.datetimeStart = value
		self.db.commit()

	@property
	def datetimeFinish(self):
		return self.model.datetimeFinish

	@datetimeFinish.setter
	def datetimeFinish(self, value):
		self.model.datetimeFinish = value
		self.db.commit()

	@property
	def points(self):
		return self.model.points

	@points.setter
	def points(self, value):
		self.model.points = value
		self.db.commit()

	@property
	def machineIp(self):
		return self.model.machineIp

	@machineIp.setter
	def machineIp(self, value):
		self.model.machineIp = value
		self.db.commit()

	@property
	def machineFqdn(self):
		return self.model.machineFqdn

	@machineFqdn.setter
	def machineFqdn(self, value):
		self.model.machineFqdn = value
		self.db.commit()

	@property
	def defaultPort(self):
		return self.model.defaultPort

	@defaultPort.setter
	def defaultPort(self, value):
		self.model.defaultPort = value
		self.db.commit()

	def score(self, team):
		instance = self.loadPlugin()
		scoreInstance = instance.score(team)
		scoreInstance.datetime = timezone.now()
		scoreInstance.teamId = team.teamId
		scoreInstance.serviceId = self.serviceId
		scoreInstance.competitionId = self.competitionId
		return score_obj

	# def loadPlugin(self):
	# 	#moduleName = Document.objects.get(servicemodule = self.servicemodule).filename.split(".")[0]
	# 	#module = __import__(settings.CONTENT_PLUGGINS_PATH.replace('/','.')[1:] + moduleName, fromlist=[moduleName])
	# 	moduleName = self.plugin.getModuleName()
	# 	module = __import__(self.plugin.getImportPath(moduleName), fromlist=[moduleName])
	# 	return getattr(module, moduleName)(self)

class ScoringEngine(ModelWrapper):
	'Scoring Engine object to represent a scoring engine module available for use by competitions.'
	model_object = ScoringEngineModel
	fields = [
		'name',
		'packageName',
		'enabled'
	]

	@property
	def name(self):
		return self.model.name

	@name.setter
	def name(self, value):
		self.model.name = value
		self.db.commit()

	@property
	def enabled(self):
		return self.model.enabled

	@enabled.setter
	def enabled(self, value):
		self.model.enabled = value
		self.db.commit()

	@property
	def packageName(self):
		# This is a read-only attribute, so there is no corresponding setter method
		return self.model.name

class Competition(ModelWrapper):
	'Competition object for controling competition settings and operation'
	model_object = CompetitionModel
	fields = [
		'organization',
		'name',
		'url',
		'description',
		'datetimeDisplay',
		'datetimeStart',
		'datetimeFinish',
		'autoStart']

	@property
	def organization(self):
		return self.model.organization

	@organization.setter
	def organization(self, value):
		# Todo:
		# Only site admins should be able to change this
		self.model.organization = value
		self.db.commit()

	@property
	def name(self):
		return self.model.name

	@name.setter
	def name(self, value):
		# Todo:
		# Only site admins & organization admins should be able to change this
		self.model.name = value
		self.db.commit()

	@property
	def url(self):
		return self.model.url

	@url.setter
	def url(self, value):
		# Todo:
		# Only site admins should be able to change this
		self.model.url = value
		self.db.commit()

	@property
	def description(self):
		return self.model.description

	@description.setter
	def description(self, value):
		# Todo:
		# Only site admins & organization admins should be able to change this
		self.model.description = value
		self.db.commit()

	@property
	def datetimeDisplay(self):
		return self.model.datetimeDisplay

	@datetimeDisplay.setter
	def datetimeDisplay(self, value):
		# Todo:
		# Only site admins & organization admins should be able to change this
		self.model.datetimeDisplay = value
		self.db.commit()

	@property
	def datetimeStart(self):
		return self.model.datetimeStart

	@datetimeStart.setter
	def datetimeStart(self, value):
		# Todo:
		# Only site admins & organization admins should be able to change this
		self.model.datetimeStart = value
		self.db.commit()

	@property
	def datetimeFinish(self):
		return self.model.datetimeFinish

	@datetimeFinish.setter
	def datetimeFinish(self, value):
		# Todo:
		# Only site admins & organization admins should be able to change this
		self.model.datetimeFinish = value
		self.db.commit()

	@property
	def autoStart(self):
		return self.model.autoStart

	@autoStart.setter
	def autoStart(self, value):
		# Todo:
		# Only site admins & organization admins should be able to change this
		self.model.autoStart = value
		self.db.commit()

	@property
	def scoringEngine(self):
		return self.model.scoringEngine

	@scoringEngine.setter
	def scoringEngine(self, value):
		# Todo:
		# Only site admins & organization admins should be able to change this
		self.model.scoringEngine = value
		self.db.commit()

	@classmethod
	def fromDict(cls, db, kwDict):
		org = Organization.fromDatabase(db, pkid = kwDict['organization'])
		if not org:
			print "Failed to get organization with pkid '%s'" % kwDict['organization']
			raise ValueError
		# Competition limiting is disabled for now since I'm not entirely sure
		# how it will be implemented with the new plugin arrangement
		#if org.model.numCompetitions >= org.maxCompetitions:
		#	raise MaxCompetitionsReached(org.maxCompetitions)
		# Copied right from ModelWrapper.fromDict
		modelObjectInst = cls.modelObject()
		clsInst = cls(db, modelObjectInst)
		for i in kwDict:
			if i in clsInst.fields:
				setattr(clsInst, i, kwDict[i])
		db.add(clsInst.model)
		db.commit()
		#org.setNumCompetitions()
		return clsInst

	def check(self):
		# Todo:
		# I don't think this is necessary. Lets just remove this
		# This conducts a consistency check on the competiton settings.
		print "A consistency check was conducted here..."

	def start(self):
		# Somehow start scoring the competition :O
		pass

class Team(ModelWrapper):
	'Team object for controling team settings'
	model_object = TeamModel
	fields = [
		'username',
		'name',
		'password',
		'networkCidr',
		'scoreConfigurations']

	@property
	def username(self):
		return self.model.username

	@username.setter
	def username(self, value):
		self.model.username = value
		self.db.commit()

	@property
	def name(self):
		return self.model.name

	@name.setter
	def name(self, value):
		self.model.name = value
		self.db.commit()

	@property
	def password(self):
		return self.model.password

	@password.setter
	def password(self, value):
		self.model.password = value
		self.db.commit()

	@property
	def networkCidr(self):
		return self.model.networkCidr

	@networkCidr.setter
	def networkCidr(self, value):
		x = ipaddr.IPNetwork(value)
		self.model.networkCidr = value
		self.db.commit()

	@property
	def scoreConfigurations(self):
		return self.model.scoreConfigurations

	@scoreConfigurations.setter
	def scoreConfigurations(self, value):
		# This function will also need to change as I improve the way
		# score configurations are interacted with....
		self.model.scoreConfigurations = scoreConfigurations
		self.db.commit()		

	def getScores(self, **kwargs):
		return Scores.search(team = self.model, **kwargs)

	def getIncidents(self):
		return Incident.search(team = self.model, **kwargs)

	def getIncidentResponses(self):
		return IncidentResponse.search(self.model, **kwargs)

	def getInjectResponses(self):
		return InjectResponse.search(self.model, **kwargs)

class Score(ModelWrapper):
	'Score object for controlling score settings'
	model_object = ScoreModel
	fields = [
		'datetime',
		'value',
		'message']

	@property
	def datetime(self):
		return self.model.datetime
	
	@datetime.setter
	def datetime(self, value):
		self.model.datetime = datetime
		self.db.commit()

	@property
	def value(self):
		return self.model.value

	@value.setter
	def value(self, value):
		self.model.value = value
		self.db.commit()

	@property
	def message(self):
		return self.model.message

	@message.setter
	def message(self, value):
		self.model.message = value
		self.db.commit()

class Inject(ModelWrapper):
	'Inject object for controling inject settings'
	model_object = InjectModel
	fields = [
		'requireResponse',
		'manualDelivery',
		'datetimeDelivery',
		'datetimeResponseDue',
		'datetimeResponseClose',
		'title',
		'body']

	@property
	def requireResponse(self):
		return self.model.requireResponse

	@requireResponse.setter
	def requireResponse(self, value):
		self.model.requireResponse = value
		self.db.commit()

	# Manual Delivery modules
	@property
	def manualDelivery(self):
		return self.model.manualDelivery

	@manualDelivery.setter
	def manualDelivery(self, value):
		self.model.manualDelivery = value
		self.db.commit()

	# Datetime Delivery modules
	@property
	def datetimeDelivery(self):
		return self.model.datetimeDelivery

	@datetimeDelivery.setter
	def datetimeDelivery(self, value):
		self.model.datetimeDelivery = value
		self.db.commit()

	# Datetime Response Due modules
	@property
	def datetimeResponseDue(self):
		return self.model.datetimeResponseDue

	@datetimeResponseDue.setter
	def datetimeResponseDue(self, value):
		self.model.datetimeResponseDue = value
		self.db.commit()

	# Datetime Response Close modules
	@property
	def datetimeResponseClose(self):
		return self.model.datetimeResponseClose

	@datetimeResponseClose.setter
	def datetimeResponseClose(self, value):
		self.model.datetimeResponseClose = value
		self.db.commit()

	# Title modules
	@property
	def title(self):
		return self.model.title

	@title.setter
	def title(self, value):
		self.model.title = value
		self.db.commit()

	# Body modules
	@property
	def body(self):
		return self.model.body

	@body.setter
	def body(self, value):
		self.model.body = value
		self.db.commit()

	# Document modules
	def addDocument(self, fileObj, contentType, filePath, filename, **kwargs):
		# What do I do with the file object....?
		Document(
			kwargs,
			inject = self.model,
			contentType = contentType,
			filePath = filePath,
			filename = filename)

	def getDocuments(self):
		return Document.search(inject = self.model)

	def delDocument(self, documentObj):
		documentObj.delete()
		del documentObj

	# Inject Response module
	def getResponses(self):
		return InjectResponse.search(inject = self.model)

class InjectResponse(ModelWrapper):
	'Inject Response object for controling inject response settings'
	model_object = InjectResponseModel
	fields = [
		'datetime',
		'content']

	@property
	def datetime(self):
		return self.model.datetime

	@datetime.setter
	def datetime(self, value):
		self.model.datetime = value
		self.db.commit()

	@property
	def content(self):
		return self.model.content

	@content.setter
	def content(self, value):
		self.model.content = value
		self.db.commit()

class Incident(ModelWrapper):
	'Incident object for controlling incident settings'
	model_object = IncidentModel
	fields = [
		'datetime',
		'subject',
		'content']

	@property
	def datetime(self):
		return self.model.datetime

	@datetime.setter
	def datetime(self, value):
		self.model.datetime = value
		self.db.commit()

	@property
	def subject(self):
		return self.model.subject

	@subject.setter
	def subject(self, value):
		self.model.subject = value
		self.db.commit()

	@property
	def content(self):
		return self.model.content

	@content.setter
	def content(self, value):
		self.model.content = value
		self.db.commit()

class IncidentResponse(ModelWrapper):
	'Incident Response object for controlling incident response settings'
	model_object = IncidentResponseModel
	fields = [
		'replyTo',
		'datetime',
		'subject',
		'content']

	@property
	def replyTo(self):
		return self.model.replyTo

	@replyTo.setter
	def replyTo(self, value):
		self.model.replyTo
		self.db.commit()

	@property
	def datetime(self):
		return self.model.datetime

	@datetime.setter
	def datetime(self, value):
		self.model.replyTo
		self.db.commit()

	@property
	def subject(self):
		return self.model.subject

	@subject.setter
	def subject(self, value):
		self.model.subject = value
		self.db.commit()

	@property
	def content(self):
		return self.model.content

	@content.setter
	def content(self, value):
		self.model.content = value
		self.db.commit()