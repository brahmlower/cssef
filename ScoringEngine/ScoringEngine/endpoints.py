from models import Competition as CompetitionModel
from models import Organization as OrganizationModel
from models import Team as TeamModel
from models import Score as ScoreModel
from models import Inject as InjectModel
from models import InjectResponse as InjectResponseModel
from models import Incident as IncidentModel
from models import IncidentResponse as IncidentResponseModel
from models import Plugin as PluginModel
from models import User as UserModel
from models import Document as DocumentModel

from serializers import UserSerializer
from serializers import OrganizationSerializer
from serializers import CompetitionSerializer
from serializers import TeamSerializer
from serializers import InjectSerializer
from serializers import InjectResponseSerializer
from serializers import IncidentSerializer
from serializers import IncidentResponseSerializer
from serializers import ScoreSerializer
from serializers import DocumentSerializer

from django.core.exceptions import ObjectDoesNotExist

class CssefObjectDoesNotExist(Exception):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return repr(self.message)

class MaxCompetitionsReached(Exception):
	def __init__(self, maxCompetitions):
		self.maxCompetitions = maxCompetitions
		self.message = "The maximum number of competitions is %d" % self.maxCompetitions

	def __str__(self):
		return repr(self.message)

class MaxMembersReached(Exception):
	def __init__(self, maxMembers):
		self.maxMembers = maxMembers
		self.message = "The maximum number of members is %d" % self.maxMembers
	def __str__(self):
		return repr(self.message)

class ModelWrapper:
	class ObjectDoesNotExist(CssefObjectDoesNotExist):
		def __init__(self, message):
			self.message = message

		def __str__(self):
			return repr(self.message)

	serializerObject = None
	modelObject = None

	def __init__(self, **kwargs):
		self.model = kwargs.pop('modelInst', None)
		if not self.model:
			try:
				self.model = self.modelObject.objects.get(**kwargs)
			except ObjectDoesNotExist:
				raise self.ObjectDoesNotExist("custom 1 - Database object matching query does not exist.")
			except self.modelObject.DoesNotExist:
				raise self.ObjectDoesNotExist("custom 2 - Database object matching query does not exist.")

	def delete(self):
		self.model.delete()

	@staticmethod
	def search(objectType, **kwargs):
		return wrappedSearch(objectType, objectType.modelObject, **kwargs)

	@staticmethod
	def create(objectType, postData, serialized = False):
		serializedModel = objectType.serializerObject(data = postData)
		if serializedModel.is_valid():
			obj = serializedModel.save()
			if serialized:
				return serializedModel.data
			else:
				return obj
		else:
			print "\n====================================="
			print "Failed to create %s object!" % objectType.__name__
			print "-------------------------------------"
			print "Serializer errors:"
			print serializedModel.errors
			print "Provided values:"
			print postData
			print "=====================================\n"
			# failed to create object
			return serializedModel.errors

	@staticmethod
	def serialize(objectType, items):
		if items.__class__.__name__ == "QuerySet":
			return objectType.serializerObject(items, many = True).data
		else:
			return objectType.serializerObject(items.model).data

class Competition(ModelWrapper):
	class Team(ModelWrapper):
		serializerObject = TeamSerializer
		modelObject = TeamModel

		def edit(self, **kwargs):
			self.serialized = kwargs.pop('serialized', None)
			for i in kwargs:
				if i == 'username':					self.setUsername(kwargs.get(i))
				elif i == 'name':					self.setName(kwargs.get(i))
				elif i == 'password':				self.setPassword(kwargs.get(i))
				elif i == 'networkCidr':			self.setNetworkCidr(kwargs.get(i))
				elif i == 'scoreConfigurations':	self.setScoreConfigurations(kwargs.get(i))

		# Username methods
		def setUsername(self, username):
			self.model.username = username
			self.model.save()

		def getUsername(self):
			return self.model.username

		# Name methods
		def setName(self, name):
			self.model.name = name
			self.model.save()

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

	class Inject(ModelWrapper):
		serializerObject = InjectSerializer
		modelObject = InjectModel

		def edit(self, **kwargs):
			self.serialized = kwargs.pop('serialized', None)
			for i in kwargs:
				if i == 'requireResponse':			self.setRequireResponse(kwargs.get(i))
				elif i == 'manualDelivery':			self.setManualDelivery(kwargs.get(i))
				elif i == 'datetimeDelivery':		self.setDatetimeDelivery(kwargs.get(i))
				elif i == 'datetimeResponseDue':	self.setDatetimeResponseDue(kwargs.get(i))
				elif i == 'datetimeResponseClose':	self.setDatetimeResponseClose(kwargs.get(i))
				elif i == 'title':					self.setTitle(kwargs.get(i))
				elif i == 'body':					self.setBody(kwargs.get(i))

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

	class InjectResponse(ModelWrapper):
		serializerObject = InjectResponseSerializer
		modelObject = InjectResponseModel

		def edit(self, **kwargs):
			self.serialized = kwargs.pop('serialized', None)
			for i in kwargs:
				if i == 'datetime':		self.setDatetime(kwargs.get(i))
				elif i == 'content':	self.setContent(kwargs.get(i))

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

	class Incident(ModelWrapper):
		serializerObject = IncidentSerializer
		modelObject = IncidentModel

		def edit(self, **kwargs):
			self.serialized = kwargs.pop('serialized', None)
			for i in kwargs:
				if i == 'datetime':		self.setDatetime(kwargs.get(i))
				elif i == 'subject':	self.setSubject(kwargs.get(i))
				elif i == 'content':	self.setContent(kwargs.get(i))

		def getDatetime(self):
			return self.model.datetime

		def setDatetime(self, datetime):
			self.model.datetime = datetime
			self.model.save()

		def getSubject(self):
			return self.model.subject

		def setSubject(self, subject):
			self.model.subject = subject
			self.model.save()

		def setContent(self):
			return self.model.content

		def getContent(self, content):
			self.model.content = content
			self.model.save()

	class IncidentResponse(ModelWrapper):
		serializerObject = IncidentResponseSerializer
		modelObject = IncidentResponseModel

		def edit(self, **kwargs):
			self.serialized = kwargs.pop('serialized', None)
			for i in kwargs:
				if i == 'replyTo':		self.setReplyTo(kwargs.get(i))
				elif i == 'datetime':	self.setDatetime(kwargs.get(i))
				elif i == 'subject':	self.setSubject(kwargs.get(i))
				elif i == 'content':	self.setContent(kwargs.get(i))

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

	class Score(ModelWrapper):
		serializerObject = ScoreSerializer
		modelObject = ScoreModel

		def edit(self, **kwargs):
			self.serialized = kwargs.pop('serialized', None)
			for i in kwargs:
				if i == 'datetime':		self.setDatetime(kwargs.get(i))
				elif i == 'value':		self.setValue(kwargs.get(i))
				elif i == 'message':	self.setMessage(kwargs.get(i))

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

	serializerObject = CompetitionSerializer
	modelObject = CompetitionModel

	@staticmethod
	def count(**kwargs):
		return Competition.modelObject.objects.filter(**kwargs).count()

	def getName(self):
		return self.model.name

	def check(self):
		# This conducts a consistency check on the competiton settings.
		print "A consistency check was conducted here..."

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

	def createTeam(self, postData, serialized = False):
		postData['organizationId'] = self.model.organization
		postData['competitionId'] = self.model.competitionId
		return Competition.Team.create(Competition.Team, postData, serialized)

	def editTeam(self, **kwargs):
		team = self.getTeam(teamId = kwargs.pop('teamId', None))
		return team.edit(**kwargs)

	def getTeam(self, **kwargs):
		return getObject(Competition.Team, competitionId = self.model.competitionId, **kwargs)

	def getTeams(self, **kwargs):
		return getObjects(Competition.Team, competitionId = self.model.competitionId, **kwargs)

	def deleteTeam(self, **kwargs):
		kwargs.pop('serialized', None)
		self.getTeam(**kwargs).delete()

	def createService(self, postData, serialized = False):
		postData['organizationId'] = self.model.organization
		postData['competitionId'] = self.model.competitionId
		return Competition.Service.create(Competition.Service, postData, serialized)

	def editService(self, **kwargs):
		service = self.getService(serviceId = kwargs.pop('serviceId', None))
		return service.edit(**kwargs)

	def editService(self, **kwargs):
		service = self.getService(serviceId = kwargs.pop('serviceId', None))
		return service.edit(**kwargs)

	def getService(self, **kwargs):
		return getObject(Competition.Service, competitionId = self.model.competitionId, **kwargs)

	def getServices(self, **kwargs):
		return getObjects(Competition.Service, competitionId = self.model.competitionId, **kwargs)

	def deleteService(self, **kwargs):
		kwargs.pop('serialized', None)
		self.getService(**kwargs).delete()

	def createIncident(self, postData, serialized = False):
		postData['organizationId'] = self.model.organization
		postData['competitionId'] = self.model.competitionId
		return Competition.Incident.create(Competition.Incident, postData, serialized)

	def editIncident(self, **kwargs):
		incident = self.getIncident(incidentId = kwargs.pop('incidentId', None))
		return incident.edit(**kwargs)

	def getIncident(self, **kwargs):
		return getObject(Competition.Incident, competitionId = self.model.competitionId, **kwargs)

	def getIncidents(self, **kwargs):
		return getObjects(Competition.Incident, competitionId = self.model.competitionId, **kwargs)

	def deleteIncident(self, **kwargs):
		kwargs.pop('serialized', None)
		self.getIncident(**kwargs).delete()

	def createIncidentResponse(self, postData, serialized = False):
		postData['organizationId'] = self.model.organization
		postData['competitionId'] = self.model.competitionId
		return Competition.IncidentResponse.create(Competition.IncidentResponse, postData, serialized)

	def editIncidentResponse(self, **kwargs):
		incidentResponse = self.getIncidentResponse(incidentResponseId = kwargs.pop('incidentResponseId', None))
		return incidentResponse.edit(**kwargs)

	def getIncidentResponse(self, **kwargs):
		return getObject(Competition.IncidentResponse, competitionId = self.model.competitionId, **kwargs)

	def getIncidentResponses(self, **kwargs):
		return getObjects(Competition.IncidentResponse, competitionId = self.model.competitionId, **kwargs)

	def deleteIncidentResponse(self, **kwargs):
		kwargs.pop('serialized', None)
		self.getIncidentResponse(**kwargs).delete()

	def createInject(self, postData, serialized = False):
		postData['organizationId'] = self.model.organization
		postData['competitionId'] = self.model.competitionId
		return Competition.Inject.create(Competition.Inject, postData, serialized)

	def editInject(self, **kwargs):
		inject = self.getInject(injectId = kwargs.pop('injectId', None))
		return inject.edit(**kwargs)

	def getInject(self, **kwargs):
		return getObject(Competition.Inject, competitionId = self.model.competitionId, **kwargs)

	def getInjects(self, **kwargs):
		return getObjects(Competition.Inject, competitionId = self.model.competitionId, **kwargs)

	def deleteInject(self, **kwargs):
		kwargs.pop('serialized', None)
		self.getInject(**kwargs).delete()

	def createInjectResponse(self, postData, serialized = False):
		postData['organizationId'] = self.model.organization
		postData['competitionId'] = self.model.competitionId
		return Competition.InjectResponse.create(Competition.InjectResponse, postData, serialized)

	def editInjectResponse(self, **kwargs):
		injectResponse = self.getInjectResponse(injectResponseId = kwargs.pop('injectResponseId', None))
		return injectResponse.edit(**kwargs)

	def getInjectResponse(self, **kwargs):
		return getObject(Competition.InjectResponse, competitionId = self.model.competitionId, **kwargs)

	def getInjectResponses(self, **kwargs):
		return getObjects(Competition.InjectResponse, competitionId = self.model.competitionId, **kwargs)

	def deleteInjectResponse(self, **kwargs):
		kwargs.pop('serialized', None)
		self.getInjectResponse(**kwargs).delete()

	def createScore(self, postData, serialized = False):
		postData['organizationId'] = self.model.organization
		postData['competitionId'] = self.model.competitionId
		return Competition.Score.create(Competition.Score, postData, serialized)

	def editScore(self, **kwargs):
		score = self.getScore(scoreId = kwargs.pop('scoreId', None))
		return score.edit(**kwargs)

	def getScore(self, **kwargs):
		return getObject(Competition.Score, competitionId = self.model.competitionId, **kwargs)

	def getScores(self, **kwargs):
		return getObjects(Competition.Score, competitionId = self.model.competitionId, **kwargs)

	def deleteScore(self, **kwargs):
		kwargs.pop('serialized', None)
		self.getScore(**kwargs).delete()

class Organization(ModelWrapper):
	serializerObject = OrganizationSerializer
	modelObject = OrganizationModel

	def edit(self, **kwargs):
		self.serialized = kwargs.pop('serialized', None)
		for i in kwargs:
			if i == 'name':					self.setName(kwargs.get(i))
			elif i == 'url':				self.setUrl(kwargs.get(i))
			elif i == 'description':		self.setDescription(kwargs.get(i))
			elif i == 'maxMembers':			self.setMaxMembers(kwargs.get(i))
			elif i == 'maxCompetitions':	self.setMaxCompetitions(kwargs.get(i))

	def getDeleteable(self):
		return self.model.deleteable

	def getName(self):
		return self.model.name

	def setName(self, name):
		self.model.name = name
		self.model.save()

	def getUrl(self):
		return self.model.url

	def setUrl(self, url):
		self.model.url = url
		self.model.save()

	def getDescription(self):
		return self.model.description

	def setDescription(self, description):
		self.model.description = description
		self.model.save()

	def getMaxMembers(self):
		return self.model.maxMembers

	def setMaxMembers(self, maxMembers):
		self.model.maxMembers = maxMembers
		self.model.save()

	def getMaxCompetitions(self):
		return self.model.maxCompetitions

	def setMaxCompetitions(self, maxCompetitions):
		self.model.maxCompetitions = maxCompetitions
		self.model.save()

	def getNumMembers(self):
		return self.model.numMembers

	def setNumMembers(self):
		self.model.numMembers = User.count(organizationId = self.model.organizationId)
		self.model.save()

	def getNumCompetitions(self):
		return self.model.setNumCompetitions

	def setNumCompetitions(self):
		self.model.numCompetitions = Competition.count(organization = self.model.organizationId)
		self.model.save()

#	----------------------------------------------

	def getCompetitions(self, **kwargs):
		if kwargs.pop('serialized', None):
			return Competition.serialize(Competition, Competition.search(Competition, organization = self.model.organizationId, **kwargs))
		else:
			return Competition.search(Competition, organization = self.model.organizationId, **kwargs)

	def getMembers(self, **kwargs):
		if kwargs.pop('serialized', None):
			return User.serialize(User, User.search(User, organizationId = self.model.organizationId, **kwargs))
		else:
			return User.search(User, organizationId = self.model.organizationId, **kwargs)

	def getCompetition(self, **kwargs):
		if kwargs.pop('serialized', None):
			return Competition.serialize(Competition, Competition(**kwargs))
		else:
			return Competition(**kwargs)

	def getMember(self, **kwargs):
		if kwargs.pop('serialized', None):
			return User.serialize(User, User(**kwargs))
		else:
			return User(**kwargs)

	def createCompetition(self, postData, serialized = False):
		if self.model.numCompetitions >= self.getMaxCompetitions():
			raise MaxCompetitionsReached(self.getMaxCompetitions())
		#postData['serialized'] = serialized
		postData['organization'] = self.model.organizationId
		newCompetition = Competition.create(Competition, postData, serialized = True)
		self.setNumCompetitions()
		return newCompetition

	def createMember(self, postData, serialized = False):
		if self.model.numMembers >= self.getMaxMembers():
			raise MaxMembersReached(self.getMaxMembers())
		#postData['serialized'] = serialized
		postData['organizationId'] = self.model.organizationId
		newUser = User.create(User, postData, serialized = True)
		self.setNumMembers()
		return newUser

	def deleteCompetition(self, **kwargs):
		kwargs.pop('serialized', None)
		competition = self.getCompetition(**kwargs)
		competition.delete()
		self.setNumCompetitions()

	def deleteMember(self, **kwargs):
		kwargs.pop('serialized', None)
		member = self.getMember(**kwargs)
		member.delete()
		self.setNumMembers()

	def editMember(self, **kwargs):
		member = self.getMember(userId = kwargs.pop('memberId', None))
		return member.edit(**kwargs)

	def editCompetition(self, **kwargs):
		competition = self.getCompetition(competitionId = kwargs.pop('competitionId', None))
		return competition.edit(**kwargs)

class User(ModelWrapper):
	serializerObject = UserSerializer
	modelObject = UserModel

	@staticmethod
	def count(**kwargs):
		return User.modelObject.objects.filter(**kwargs).count()

	def edit(self, **kwargs):
		self.serialized = kwargs.pop('serialized', None)
		for i in kwargs:
			if i == 'name':				self.setName(kwargs.get(i))
			elif i == 'username':		self.setUsername(kwargs.get(i))
			elif i == 'password':		self.setPassword(kwargs.get(i))
			elif i == 'description':	self.setDescription(kwargs.get(i))
			elif i == 'organization':	self.setOrganizationId(kwargs.get(i))	

	def getName(self):
		return self.model.name

	def setName(self, name):
		self.model.name = name
		self.model.save()

	def getUsername(self):
		return self.model.username

	def setUsername(self, name):
		self.model.username = username
		self.model.save()

	def getPassword(self):
		return self.model.password

	def setPassword(self, password):
		self.model.password = password
		self.model.save()

	def getDescription(self):
		return self.model.description

	def setDescription(self, description):
		self.model.description = description
		self.model.save()

	def getOrganizationId(self):
		return self.model.organizationId

	def setOrganizationId(self, organizationId):
		self.model.organizationId = organizationId
		self.model.save()

class Document(ModelWrapper):
	serializerObject = DocumentSerializer
	modelObject = DocumentModel

	def edit(self, **kwargs):
		self.serialized = kwargs.pop('serialized', None)
		for i in kwargs:
			if i == 'contentType':			self.setContentType(kwargs.get(i))
			elif i == 'fileHash':			self.setFileHash(kwargs.get(i))
			elif i == 'filePath':			self.setFilePath(kwargs.get(i))
			elif i == 'filename':			self.setFilename(kwargs.get(i))
			elif i == 'urlEncodedFilename': self.setUrlEncodedFilename(kwargs.get(i))

	def setContentType(self, contentType):
		self.model.contentType = contentType
		self.model.save()

	def getContentType(self):
		return self.model.contentType

	def setFileHash(self, fileHash):
		self.model.fileHash = fileHash
		self.model.save()

	def getFileHash(self):
		return self.model.fileHash

	def setFilePath(self, filePath):
		self.model.filePath = filePath
		self.model.save()

	def getFilePath(self):
		return self.model.filePath

	def setFilename(self, filename):
		self.model.filename = filename
		self.model.save()

	def getFilename(self):
		return self.model.filename

	def setUrlEncodedFilename(self, urlEncodedFilename):
		self.model.urlEncodedFilename = urlEncodedFilename
		self.model.save()

	def getUrlEncodedFilename(self):
		return self.model.urlEncodedFilename

def getObjects(classPointer, **kwargs):
	if kwargs.pop('serialized', None):
		return classPointer.serialize(classPointer, classPointer.search(classPointer, **kwargs))
	else:
		return classPointer.search(**kwargs)

def getObject(classPointer, **kwargs):
	if kwargs.pop('serialized', None):
		return classPointer.serialize(classPointer, classPointer(**kwargs))
	else:
		return classPointer(**kwargs)

def wrappedSearch(objType, objTypeModel, **kwargs):
	serialized = kwargs.pop('serialized', False)
	modelResults = objTypeModel.objects.filter(**kwargs)
	if serialized:
		return objType.serialize(modelResults)
	else:
		return modelResults

def getCompetition(**kwargs):
	return getObject(Competition, **kwargs)

def getCompetitions(**kwargs):
	return getObjects(Competition, **kwargs)

def getOrganization(**kwargs):
	return getObject(Organization, **kwargs)

def getOrganizations(**kwargs):
	return getObjects(Organization, **kwargs)

def createOrganization(postData, serialized = False):
	return Organization.create(Organization, postData, serialized)

def editOrganization(**kwargs):
	organization = getOrganization(organizationId = kwargs.pop('organizationId', None))
	return organization.edit(**kwargs)

def getUsers(**kwargs):
	return getObjects(User, **kwargs)

def getUser(**kwargs):
	return getObject(User, **kwargs)

def editUser(**kwargs):
	user = getUser(userId = kwargs.pop('userId', None))
	return user.edit(**kwargs)



