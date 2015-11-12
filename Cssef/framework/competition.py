from models import Competition as CompetitionModel
from models import Team as TeamModel
from models import Score as ScoreModel
from models import Inject as InjectModel
from models import InjectResponse as InjectResponseModel
from models import Incident as IncidentModel
from models import IncidentResponse as IncidentResponseModel

from framework.utils import ModelWrapper

class Competition(ModelWrapper):
	'Competition object for controling competition settings and operation'
	modelObject = CompetitionModel

	class __metaclass__(type):
		def __str__(self):
			return "Competition '%s' (id: %d)" % (self.name, self.getId())

	def edit(self, **kwargs):
		for i in kwargs:
			if i == 'organization':							self.organization = kwargs.get(i)
			elif i == 'name':								self.name = kwargs.get(i)
			elif i == 'url':								self.url = kwargs.get(i)
			elif i == 'description':						self.description = kwargs.get(i)
			elif i == 'datetimeDisplay':					self.datetimeDisplay = kwargs.get(i)
			elif i == 'datetimeStart':						self.datetimeStart = kwargs.get(i)
			elif i == 'datetimeFinish':						self.datetimeFinish = kwargs.get(i)
			elif i == 'autoStart':							self.autoStart = kwargs.get(i)
			elif i == 'scoringEngine':						self.scoringEngine = kwargs.get(i)

	@property
	def organization(self):
		return self.model.organization

	@organization.setter
	def organization(self, value):
		self.model.organization = value
		self.model.save()

	@property
	def name(self):
		return self.model.name

	@name.setter
	def name(self, value):
		self.model.name = value
		self.model.save()

	@property
	def url(self):
		return self.model.url

	@url.setter
	def url(self, value):
		self.model.url = value
		self.model.save()

	@property
	def description(self):
		return self.model.description

	@description.setter
	def description(self, value):
		self.model.description = value
		self.model.save()

	@property
	def datetimeDisplay(self):
		return self.model.datetimeDisplay

	@datetimeDisplay.setter
	def datetimeDisplay(self, value):
		self.model.datetimeDisplay = value
		self.model.save()

	@property
	def datetimeStart(self):
		return self.model.datetimeStart

	@datetimeStart.setter
	def datetimeStart(self, value):
		self.model.datetimeStart = value
		self.model.save()

	@property
	def datetimeFinish(self):
		return self.model.datetimeFinish

	@datetimeFinish.setter
	def datetimeFinish(self, value):
		self.model.datetimeFinish = value
		self.model.save()

	@property
	def autoStart(self):
		return self.model.autoStart

	@autoStart.setter
	def autoStart(self, value):
		self.model.autoStart = value
		self.model.save()

	@property
	def scoringEngine(self):
		return self.model.scoringEngine

	@scoringEngine.setter
	def scoringEngine(self, value):
		self.model.scoringEngine = value
		self.model.save()

	@staticmethod
	def count(**kwargs):
		return Competition.modelObject.objects.filter(**kwargs).count()

	def check(self):
		# This conducts a consistency check on the competiton settings.
		print "A consistency check was conducted here..."

	def createTeam(self, kwDict):
		kwDict['competition'] = self.getId()
		return Team.create(kwDict)

	def createIncident(self, kwDict):
		kwDict['competition'] = self.getId()
		return Incident.create(kwDict)

	def createIncidentResponse(self, kwDict):
		kwDict['competition'] = self.getId()
		return IncidentResponse.create(kwDict)

	def createInject(self, kwDict):
		kwDict['competition'] = self.getId()
		return Inject.create(kwDict)

	def createInjectResponse(self, kwDict):
		kwDict['competition'] = self.getId()
		return InjectResponse.create(kwDict)

	def createScore(self, kwDict):
		kwDict['competition'] = self.getId()
		return Score.create(kwDict)

class Team(ModelWrapper):
	'Team object for controling team settings'
	modelObject = TeamModel

	def edit(self, **kwargs):
		for i in kwargs:
			if i == 'username':					self.username = kwargs.get(i)
			elif i == 'name':					self.name = kwargs.get(i)
			elif i == 'password':				self.password = kwargs.get(i)
			elif i == 'networkCidr':			self.networkCidr = kwargs.get(i)
			elif i == 'scoreConfigurations':	self.scoreConfigurations = kwargs.get(i)

	@property
	def username(self):
		return self.model.username

	@username.setter
	def username(self, value):
		self.model.username = value
		self.model.save()

	@property
	def name(self):
		return self.model.name

	@name.setter
	def name(self, value):
		self.model.name = value
		self.model.save()

	@property
	def password(self):
		return self.model.password

	@password.setter
	def password(self, value):
		self.model.password = value
		self.model.save()

	@property
	def networkCidr(self):
		return self.model.networkCidr

	@networkCidr.setter
	def networkCidr(self, value):
		self.model.networkCidr = value
		self.model.save()

	def getScoreConfigurations(self):
		return self.model.scoreConfigurations

	def setScoreConfigurations(self, scoreConfigurations):
		# This function will also need to change as I improve the way
		# score configurations are interacted with....
		self.model.scoreConfigurations = scoreConfigurations
		self.model.save()

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
	modelObject = ScoreModel

	def edit(self, **kwargs):
		for i in kwargs:
			if i == 'datetime':		self.datetime = kwargs.get(i)
			elif i == 'value':		self.value = kwargs.get(i)
			elif i == 'message':	self.message = kwargs.get(i)

	@property
	def datetime(self):
		return self.model.datetime
	
	@datetime.setter
	def datetime(self, value):
		self.model.datetime = datetime
		self.model.save()

	@property
	def value(self):
		return self.model.value

	@value.setter
	def value(self, value):
		self.model.value = value
		self.model.save()

	@property
	def message(self):
		return self.model.message

	@message.setter
	def message(self, value):
		self.model.message
		self.model.save()

class Inject(ModelWrapper):
	'Inject object for controling inject settings'
	modelObject = InjectModel

	def edit(self, **kwargs):
		for i in kwargs:
			if i == 'requireResponse':			self.requireResponse = kwargs.get(i)
			elif i == 'manualDelivery':			self.manualDelivery = kwargs.get(i)
			elif i == 'datetimeDelivery':		self.datetimeDelivery = kwargs.get(i)
			elif i == 'datetimeResponseDue':	self.datetimeResponseDue = kwargs.get(i)
			elif i == 'datetimeResponseClose':	self.datetimeResponseClose = kwargs.get(i)
			elif i == 'title':					self.title = kwargs.get(i)
			elif i == 'body':					self.body = kwargs.get(i)

	@property
	def requireResponse(self):
		return self.model.requireResponse

	@requireResponse.setter
	def requireResponse(self, value):
		self.model.requireResponse = value
		self.model.save()

	# Manual Delivery modules
	@property
	def manualDelivery(self):
		return self.model.manualDelivery

	@manualDelivery.setter
	def manualDelivery(self, value):
		self.model.manualDelivery = value
		self.model.save()

	# Datetime Delivery modules
	@property
	def datetimeDelivery(self):
		return self.model.datetimeDelivery

	@datetimeDelivery.setter
	def datetimeDelivery(self, value):
		self.model.datetimeDelivery = value
		self.model.save()

	# Datetime Response Due modules
	@property
	def datetimeResponseDue(self):
		return self.model.datetimeResponseDue

	@datetimeResponseDue.setter
	def datetimeResponseDue(self, value):
		self.model.datetimeResponseDue = value
		self.model.save()

	# Datetime Response Close modules
	@property
	def datetimeResponseClose(self):
		return self.model.datetimeResponseClose

	@datetimeResponseClose.setter
	def datetimeResponseClose(self, value):
		self.model.datetimeResponseClose = value
		self.model.save()

	# Title modules
	@property
	def title(self):
		return self.model.title

	@title.setter
	def title(self, value):
		self.model.title = value
		self.model.save()

	# Body modules
	@property
	def body(self):
		return self.model.body

	@body.setter
	def body(self, value):
		self.model.body = value
		self.model.save()

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
	modelObject = InjectResponseModel

	def edit(self, **kwargs):
		for i in kwargs:
			if i == 'datetime':		self.datetime = kwargs.get(i)
			elif i == 'content':	self.content = kwargs.get(i)

	@property
	def datetime(self):
		return self.model.datetime

	@datetime.setter
	def datetime(self, value):
		self.model.datetime = value
		self.model.save()

	@property
	def content(self):
		return self.model.content

	@content.setter
	def content(self, value):
		self.model.content = value
		self.model.save()

class Incident(ModelWrapper):
	'Incident object for controlling incident settings'
	modelObject = IncidentModel

	def edit(self, **kwargs):
		for i in kwargs:
			if i == 'datetime':		self.datetime = kwargs.get(i)
			elif i == 'subject':	self.subject = kwargs.get(i)
			elif i == 'content':	self.content = kwargs.get(i)

	@property
	def datetime(self):
		return self.model.datetime

	@datetime.setter
	def datetime(self, value):
		self.model.datetime = value
		self.model.save()

	@property
	def subject(self):
		return self.model.subject

	@subject.setter
	def subject(self, value):
		self.model.subject = value
		self.model.save()

	@property
	def content(self):
		return self.model.content

	@content.setter
	def content(self, value):
		self.model.content = value
		self.model.save()

class IncidentResponse(ModelWrapper):
	'Incident Response object for controlling incident response settings'
	modelObject = IncidentResponseModel

	def edit(self, **kwargs):
		for i in kwargs:
			if i == 'replyTo':		self.replyTo = kwargs.get(i)
			elif i == 'datetime':	self.datetime = kwargs.get(i)
			elif i == 'subject':	self.subject = kwargs.get(i)
			elif i == 'content':	self.content = kwargs.get(i)

	@property
	def replyTo(self):
		return self.model.replyTo

	@replyTo.setter
	def replyTo(self, value):
		self.model.replyTo
		self.model.save()

	@property
	def datetime(self):
		return self.model.datetime

	@datetime.setter
	def datetime(self, value):
		self.model.replyTo
		self.model.save()

	@property
	def subject(self):
		return self.model.subject

	@subject.setter
	def subject(self, value):
		self.model.subject = value
		self.model.save()

	@property
	def content(self):
		return self.model.content

	@content.setter
	def content(self, value):
		self.model.content = value
		self.modle.save()
