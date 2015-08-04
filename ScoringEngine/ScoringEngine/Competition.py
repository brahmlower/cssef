from models import Competition as CompetitionModel
from models import Team as TeamModel
from models import Score as ScoreModel
from models import Inject as InjectModel
from models import InjectResponse as InjectResponseModel
from models import Incident as IncidentModel
from models import IncidentResponse as IncidentResponseModel
from Document import Document

class Team:
	def __init__(self, teamModelObj = None, **kwargs):
		self.model = teamModelObj
		if not self.model:
			self.model = TeamModel(**kwargs)
			self.model.save()

	def delete(self):
		self.model.delete()

	@staticmethod
	def search(**kwargs):
		return wrappedSearch(Team, TeamModel, **kwargs)

	# Username methods
	def setUsername(self, username):
		self.model.username = username
		self.model.save()

	def getUsername(self):
		return self.model.username

	# Name methods
	def setName(self, name):
		self.model.name = name
		self.model.name.save()

	def getName(self):
		return self.model.name

	# Password method
	def setPassword(self, password):
		self.model.password = password
		# plaintext I know, I'll cross this bridge when i get here

	# Network CIDR methods
	def setNetworkCidr(self):
		return self.model.networkCidr

	def getNetworkCidr(self):
		self.model.networkCidr = networkCidr
		self.model.save()

	# Score Configuration methds
	def setScoreConfigurations(self):
		return self.model.scoreConfigurations

	def getScoreConfigurations(self):
		# This function will also need to change as I improve the way
		# score configurations are interacted with....
		self.model.scoreConfigurations = scoreConfigurations
		self.model.save()

	# Score methods
	def addScore(self, value, message, **kwargs):
		newScore = Score(
			kwargs,
			team = self.model,
			value = value,
			message = message)

	def getScores(self, **kwargs):
		return Scores.search(team = self.model, **kwargs)

	# Incident methods
	def addIncident(self):
		newIncident = Incident() #TODO: Write the incident everything

	def getIncidents(self):
		return Incident.search(team = self.model, **kwargs)

	# Incident Response modules
	def addIncidentResponse(self, subject, content, **kwargs):
		newIncidentResponse = IncidentResponse(
			kwargs,
			team = self.model,
			subject = subject,
			content = content)

	def getIncidentResponses(self):
		return IncidentResponse.search(self.model, **kwargs)

	# Inject Response modules
	def addInjectResponse(self, inject, content, **kwargs):
		newInjectResponse = InjectResponse(
			kwargs,
			team = self.model,
			inject = inject,
			content = content)

	def getInjectResponses(self):
		return InjectResponse.search(self.model, **kwargs)

class Inject:
	def __init__(self, injectModelObj = None, **kwargs):
		self.model = injectModelObj
		if not self.model:
			self.model = InjectModel(**kwargs)
			self.model.save()

	def delete(self):
		self.model.delete()

	@staticmethod
	def search(**kwargs):
		return wrappedSearch(Inject, InjectModel, **kwargs)

	# Require Response modules
	def setRequireResponse(self, requireResponse):
		self.model.requireResponse = requireResponse
		self.model.save()

	def getRequireResponse(self):
		return self.model.requireResponse

	# Manual Delivery modules
	def setManualDelivery(self, manualDelivery):
		self.model.manualDelivery = manualDelivery
		self.model.save()

	def getManualDelivery(self):
		return self.model.manualDelivery

	# Datetime Delivery modules
	def setDatetimeDelivery(self, datetimeDelivery):
		self.model.datetimeDelivery = datetimeDelivery
		self.model.save()

	def getDatetimeDelivery(self):
		return self.model.datetimeDelivery

	# Datetime Response Due modules
	def setDatetimeResponseDue(self, datetimeResponseDue):
		self.model.datetimeResponseDue = datetimeResponseDue
		self.model.save()

	def getDatetimeResponseDue(self):
		return self.model.datetimeResponseDue

	# Datetime Response Close modules
	def setDatetimeResponseClose(self, datetimeResponseClose):
		self.model.datetimeResponseClose = datetimeResponseClose
		self.model.save()

	def getDatetimeResponseClose(self):
		return self.model.datetimeResponseClose

	# Title modules
	def setTitle(self, title):
		self.model.title = title
		self.model.save()

	def getTitle(self):
		return self.model.title

	# Body modules
	def setBody(self, body):
		self.model.body = body
		self.model.save()

	def getBody(self):
		return self.model.body

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

class InjectResponse:
	def __init__(self, injectResponseModelObj = None, **kwargs):
		self.model = injectResponseModelObj
		if not self.model:
			self.model = InjectResponseModel(**kwargs)
			self.model.save()

	def delete(self):
		self.model.delete()

	@staticmethod
	def search(**kwargs):
		return wrappedSearch(InjectResponse, InjectResponseModel, **kwargs)

	def setDatetime(self, datetime):
		self.model.datetime = datetime
		self.model.save()

	def getDatetime(self):
		return self.model.datetime

	def setContent(self, content):
		self.model.content = content
		self.model.save()

	def getContent(self):
		return self.model.content

# This model doesn't even exist!
class Incident:
	def __init__(self, incidentModelObj = None, **kwargs):
		self.model = incidentModelObj
		if not self.model:
			self.model = IncidentModel(**kwargs)
			self.model.save()

	def delete(self):
		self.model.delete()

	@staticmethod
	def search(**kwargs):
		return wrappedSearch(Incident, IncidentModel, **kwargs)

class IncidentResponse:
	def __init__(self, incidentResponseModelObj = None, **kwargs):
		self.model = incidentResponseModelObj
		if not self.model:
			self.model = IncidentResponseModel(**kwargs)
			self.model.save()

	def delete(self):
		self.model.delete()

	@staticmethod
	def search(**kwargs):
		return wrappedSearch(IncidentResponse, IncidentResponseModel, **kwargs)

	def setReplyTo(self, replyTo):
		self.model.replyTo = replyTo
		self.model.save()

	def getReplyTo(self):
		return self.model.replyTo

	def setDatetime(self, datetime):
		self.model.datetime = datetime
		self.model.save()

	def getDatetime(self):
		return self.model.datetime

	def setSubject(self, subject):
		self.model.subject = subject
		self.model.save()

	def getSubject(self):
		return self.model.subject

	def setContent(self, content):
		self.model.content = content
		self.model.save()

	def getContent(self):
		return self.model.content

class Score:
	def __init__(self, scoreModelObj = None, **kwargs):
		self.model = scoreModelObj
		if not self.model:
			self.model = ScoreModel(**kwargs)
			self.model.save()

	def delete(self):
		self.model.delete()

	@staticmethod
	def search(**kwargs):
		return wrappedSearch(Score, ScoreModel, **kwargs)

	def isSlaViolation(competition):
		# TODO: LEGACY CODE, NEEDS TO BE UPDATED
		slaThreashold = competition.scoringSlaThreashold
		lastScores = Score.objects.filter(competitionId = competition.competitionId,
			serviceId = serviceId, teamId = teamId).order_by('-scoreId')[:slaThreashold]
		if len(lastScores) < slaThreashold:
			return False
		for score in lastScores:
			if score.value > 0:
				return False
		return True

	def setDatetime(self, datetime):
		self.model.datetime = datetime
		self.model.save()

	def getDatetime(self):
		return self.model.datetime

	def setValue(self, value):
		self.model.value = value
		self.model.save()

	def getValue(self):
		return self.model.value

	def setMessage(self, message):
		self.model.message = message
		self.model.save()

	def getMessage(self):
		return self.model.message

# Teams modules
def newTeam(self, name, username, password, networkCidr, **kwargs):
	Team(
		kwargs,
		name = name,
		username = username,
		password = password,
		networkCidr = networkCidr)

def getTeam(self, serialized = False, **kwargs):
	return self.searchOne(Team, serialized, **kwargs)

def getTeams(self, serialized = False):
	return self.searchMany(Team, serialized)

def delTeam(self, teamObj):
	# This was the cleanest I could get this. Not sure if it really works...
	teamObj.delete()
	del teamObj

# Inject modules
def newInject(self, title, body, **kwargs):
	Inject(
		kwargs,
		title = title,
		body = body)

def getInject(self, serialized = False, **kwargs):
	return self.searchOne(Inject, serialized, **kwargs)

def getInjects(self, serialized = False):
	return self.searchMany(Inject, serialized)

def delInject(self, injectObj):
	injectObj.delete()
	del injectObj

def check(self):
	# This conducts a consistency check on the compeititon settings.
	print "A consistency check was conducted here..."

def wrappedSearch(objType, objModelType, queryDict, **kwargs):
	modelResults = objModelType.object.filter(**kwargs)
	results = []
	for i in modelResults:
		results.append(objType(i))
	return results



def searchOne(self, objType, serialized = False, **kwargs):
	obj = objType.search(kwargs, competition = self.model)
	if serialized:
		return serializedModel(obj)
	else:
		return obj

def searchMany(self, objType, serialized = False):
	obj = objType.search(competition = self.model)
	if serialized:
		return serializedModel(obj)
	else:
		return obj

