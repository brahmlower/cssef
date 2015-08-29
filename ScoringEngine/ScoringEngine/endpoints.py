from models import Competition as CompetitionModel
from models import Team as TeamModel
from models import Score as ScoreModel
from models import Inject as InjectModel
from models import InjectResponse as InjectResponseModel
from models import Incident as IncidentModel
from models import IncidentResponse as IncidentResponseModel
from Document import Document
from models import Organization as OrganizationModel
from models import Team as TeamModel
from models import Score as ScoreModel
from models import Inject as InjectModel
from models import InjectResponse as InjectResponseModel
from models import Incident as IncidentModel
from models import IncidentResponse as IncidentResponseModel
from Document import Document
from models import Plugin as PluginModel
from models import User as UserModel

from serializers import UserSerializer
from serializers import OrganizationSerializer
from serializers import CompetitionSerializer
from serializers import TeamSerializer
from serializers import InjectSerializer
from serializers import InjectResponseSerializer
from serializers import IncidentSerializer
from serializers import IncidentResponseSerializer
from serializers import ScoreSerializer

from django.core.exceptions import ObjectDoesNotExist

class CssefObjectDoesNotExist(Exception):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return repr(self.message)

class Competition:
	class Team:
		class ObjectDoesNotExist(CssefObjectDoesNotExist):
			def __init__(self, message):
				self.message = message

			def __str__(self):
				return repr(self.message)

		serializerObject = TeamSerializer
		modelObject = TeamModel

		def __init__(self, **kwargs):
			self.model = kwargs.pop('modelInst', None)
			if not self.model:
				try:
					self.model = Competition.Team.modelObject.objects.get(**kwargs)
				except ObjectDoesNotExist:
					raise self.ObjectDoesNotExist("custom 1 - Team matching query does not exist.")
				except Competition.Team.modelObject.DoesNotExist:
					raise self.ObjectDoesNotExist("custom 2 - Team matching query does not exist.")

		def delete(self):
			self.model.delete()

		@staticmethod
		def search(**kwargs):
			return wrappedSearch(Competition.Team, TeamModel, **kwargs)

		@staticmethod
		def create(postData, serialized = False):
			serializedModel = Competition.Team.serializerObject(data = postData)
			if serializedModel.is_valid():
				obj = serializedModel.save()
				if serialized:
					return serializedModel.data
				else:
					return obj
			else:
				print "failed to be created!"
				print serializedModel.errors
				# failed to create object
				return serializedModel.errors

		@staticmethod
		def serialize(items):
			if items.__class__.__name__ == "QuerySet":
				return Competition.Team.serializerObject(items, many = True).data
			else:
				return Competition.Team.serializerObject(items.model).data

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
		class ObjectDoesNotExist(CssefObjectDoesNotExist):
			def __init__(self, message):
				self.message = message

			def __str__(self):
				return repr(self.message)

		serializerObject = InjectSerializer
		modelObject = InjectModel
		def __init__(self, **kwargs):
			self.model = kwargs.pop('modelInst', None)
			if not self.model:
				try:
					self.model = Competition.Inject.modelObject.objects.get(**kwargs)
				except ObjectDoesNotExist:
					raise self.ObjectDoesNotExist("custom 1 - Inject matching query does not exist.")
				except Competition.Inject.modelObject.DoesNotExist:
					raise self.ObjectDoesNotExist("custom 2 - Inject matching query does not exist.")

		def delete(self):
			self.model.delete()

		@staticmethod
		def search(**kwargs):
			return wrappedSearch(Competition.Inject, InjectModel, **kwargs)

		@staticmethod
		def create(postData, serialized = False):
			serializedModel = Competition.Inject.serializerObject(data = postData)
			if serializedModel.is_valid():
				obj = serializedModel.save()
				if serialized:
					return serializedModel.data
				else:
					return obj
			else:
				print "====== Failed to be created ========"
				print "Errors:"
				print serializedModel.errors
				print "Provided data:"
				print postData
				# failed to create object
				return serializedModel.errors

		@staticmethod
		def serialize(items):
			if items.__class__.__name__ == "QuerySet":
				return Competition.Inject.serializerObject(items, many = True).data
			else:
				return Competition.Inject.serializerObject(items.model).data

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
		serializerObject = InjectResponseSerializer
		modelObject = InjectResponseModel
		def __init__(self, injectResponseModelObj = None, **kwargs):
			self.model = injectResponseModelObj
			if not self.model:
				self.model = InjectResponseModel(**kwargs)
				self.model.save()

		def delete(self):
			self.model.delete()

		@staticmethod
		def search(**kwargs):
			return wrappedSearch(Competition.InjectResponse, InjectResponseModel, **kwargs)

		@staticmethod
		def create(postData, serialized = False):
			serializedModel = Competition.InjectResponse.serializerObject(data = postData)
			if serializedModel.is_valid():
				obj = serializedModel.save()
				if serialized:
					return serializedModel.data
				else:
					return obj
			else:
				print "failed to be created!"
				print serializedModel.errors
				# failed to create object
				return serializedModel.errors

		@staticmethod
		def serialize(items):
			if items.__class__.__name__ == "QuerySet":
				return Competition.InjectResponse.serializerObject(items, many = True).data
			else:
				return Competition.InjectResponse.serializerObject(items.model).data

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

	class Incident:
		serializerObject = IncidentSerializer
		modelObject = IncidentModel
		def __init__(self, incidentModelObj = None, **kwargs):
			self.model = incidentModelObj
			if not self.model:
				self.model = IncidentModel(**kwargs)
				self.model.save()

		def delete(self):
			self.model.delete()

		@staticmethod
		def search(**kwargs):
			return wrappedSearch(Competition.Incident, IncidentModel, **kwargs)

		@staticmethod
		def create(postData, serialized = False):
			serializedModel = Competition.Incident.serializerObject(data = postData)
			if serializedModel.is_valid():
				obj = serializedModel.save()
				if serialized:
					return serializedModel.data
				else:
					return obj
			else:
				print "failed to be created!"
				print serializedModel.errors
				# failed to create object
				return serializedModel.errors

		@staticmethod
		def serialize(items):
			if items.__class__.__name__ == "QuerySet":
				return Competition.Incident.serializerObject(items, many = True).data
			else:
				return Competition.Incident.serializerObject(items.model).data

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

	class IncidentResponse:
		serializerObject = IncidentResponseSerializer
		modelObject = IncidentResponseModel
		def __init__(self, incidentResponseModelObj = None, **kwargs):
			self.model = incidentResponseModelObj
			if not self.model:
				self.model = IncidentResponseModel(**kwargs)
				self.model.save()

		def delete(self):
			self.model.delete()

		@staticmethod
		def search(**kwargs):
			return wrappedSearch(Competition.IncidentResponse, IncidentResponseModel, **kwargs)

		@staticmethod
		def create(postData, serialized = False):
			print "Create Method:"
			print postData
			serializedModel = Competition.IncidentResponse.serializerObject(data = postData)
			if serializedModel.is_valid():
				obj = serializedModel.save()
				if serialized:
					return serializedModel.data
				else:
					return obj
			else:
				print "failed to be created!"
				print serializedModel.errors
				# failed to create object
				return serializedModel.errors

		@staticmethod
		def serialize(items):
			if items.__class__.__name__ == "QuerySet":
				return Competition.IncidentResponse.serializerObject(items, many = True).data
			else:
				return Competition.IncidentResponse.serializerObject(items.model).data

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
		serializerObject = ScoreSerializer
		modelObject = ScoreModel
		def __init__(self, scoreModelObj = None, **kwargs):
			self.model = scoreModelObj
			if not self.model:
				self.model = ScoreModel(**kwargs)
				self.model.save()

		def delete(self):
			self.model.delete()

		@staticmethod
		def search(**kwargs):
			return wrappedSearch(Competition.Score, ScoreModel, **kwargs)

		@staticmethod
		def create(postData, serialized = False):
			serializedModel = Competition.Score.serializerObject(data = postData)
			if serializedModel.is_valid():
				obj = serializedModel.save()
				if serialized:
					return serializedModel.data
				else:
					return obj
			else:
				print "failed to be created!"
				print serializedModel.errors
				# failed to create object
				return serializedModel.errors

		@staticmethod
		def serialize(items):
			if items.__class__.__name__ == "QuerySet":
				return Competition.Score.serializerObject(items, many = True).data
			else:
				return Competition.Score.serializerObject(items.model).data

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

	class ObjectDoesNotExist(CssefObjectDoesNotExist):
		def __init__(self, message):
			self.message = message

		def __str__(self):
			return repr(self.message)

	serializerObject = CompetitionSerializer
	modelObject = CompetitionModel
	def __init__(self, **kwargs):
		self.model = kwargs.pop('modelInst', None)
		if not self.model:
			try:
				self.model = Competition.modelObject.objects.get(**kwargs)
			except ObjectDoesNotExist:
				raise self.ObjectDoesNotExist("custom 1 - Competition matching query does not exist.")
			except modelObject.DoesNotExist:
				raise self.ObjectDoesNotExist("custom 2 - Competition matching query does not exist.")

	def delete(self):
		self.model.delete()

	@staticmethod
	def count(**kwargs):
		return Competition.modelObject.objects.filter(**kwargs).count()

	@staticmethod
	def search(**kwargs):
		return wrappedSearch(Competition, Competition.modelObject, **kwargs)

	@staticmethod
	def create(postData, serialized = False):
		#serialized = kwargs.pop('serialized', False)
		serializedModel = Competition.serializerObject(data = postData)
		if serializedModel.is_valid():
			obj = serializedModel.save()
			if serialized:
				return serializedModel.data
			else:
				return obj
		else:
			print "failed to be created!"
			print serializedModel.errors
			# failed to create object
			return serializedModel.errors

	@staticmethod
	def serialize(items):
		if items.__class__.__name__ == "QuerySet":
			return Competition.serializerObject(items, many = True).data
		else:
			return Competition.serializerObject(items.model).data	

	def getName(self):
		return self.model.name

	# Teams modules
	# def newTeam(self, name, username, password, networkCidr, **kwargs):
	# 	Team(
	# 		kwargs,
	# 		name = name,
	# 		username = username,
	# 		password = password,
	# 		networkCidr = networkCidr)

	# def getTeam(self, serialized = False, **kwargs):
	# 	return self.searchOne(Team, serialized, **kwargs)

	# def getTeams(self, serialized = False):
	# 	return self.searchMany(Team, serialized)

	# def delTeam(self, teamObj):
	# 	# This was the cleanest I could get this. Not sure if it really works...
	# 	teamObj.delete()
	# 	del teamObj

	# Inject modules
	# def newInject(self, title, body, **kwargs):
	# 	Inject(
	# 		kwargs,
	# 		title = title,
	# 		body = body)

	# def getInject(self, serialized = False, **kwargs):
	# 	return self.searchOne(Inject, serialized, **kwargs)

	# def getInjects(self, serialized = False):
	# 	return self.searchMany(Inject, serialized)

	# def delInject(self, injectObj):
	# 	injectObj.delete()
	# 	del injectObj

	def check(self):
		# This conducts a consistency check on the compeititon settings.
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
		return Competition.Team.create(postData, serialized)

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
		return Competition.Service.create(postData, serialized)

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
		return Competition.Incident.create(postData, serialized)

	def getIncident(self, **kwargs):
		return getObject(Competition.Incident, competitionId = self.model.competitionId, **kwargs)

	def getIncidents(self, **kwargs):
		return getObjects(Competition.Incident, competitionId = self.model.competitionId, **kwargs)

	def deleteIncident(self, **kwargs):
		kwargs.pop('serialized', None)
		print kwargs
		self.getIncident(**kwargs).delete()

	def createIncidentResponse(self, postData, serialized = False):
		postData['organizationId'] = self.model.organization
		postData['competitionId'] = self.model.competitionId
		return Competition.IncidentResponse.create(postData, serialized)

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
		return Competition.Inject.create(postData, serialized)

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
		return Competition.InjectResponse.create(postData, serialized)

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
		return Competition.Score.create(postData, serialized)

	def getScore(self, **kwargs):
		return getObject(Competition.Score, competitionId = self.model.competitionId, **kwargs)

	def getScores(self, **kwargs):
		return getObjects(Competition.Score, competitionId = self.model.competitionId, **kwargs)

	def deleteScore(self, **kwargs):
		kwargs.pop('serialized', None)
		self.getScore(**kwargs).delete()


def getObjects(classPointer, **kwargs):
	if kwargs.pop('serialized', None):
		return classPointer.serialize(classPointer.search(**kwargs))
	else:
		return classPointer.search(**kwargs)

def getObject(classPointer, **kwargs):
	if kwargs.pop('serialized', None):
		return classPointer.serialize(classPointer(**kwargs))
	else:
		return classPointer(**kwargs)


#TODO: This could make life a lot easier. Maybe finish this method, then test it on the Organization and User classes

# class ModelWrapper:
# 	serializerObject = None
# 	modelObject = None

# 	def __init__(self, **kwargs):
# 		self.model = kwargs.pop('instance', None)
# 		if not self.model:
# 			try:
# 				self.model = Organization.modelObject.objects.get(**kwargs)
# 			except ObjectDoesNotExist:
# 				print "WOAH! Object couldn't be found!"
# 				self.model = None

# 	def delete(self):
# 		if self.model.deleteable:
# 			self.model.delete()

# 	@staticmethod
# 	def search(**kwargs):
# 		return wrappedSearch(Organization, Organization.modelObject, **kwargs)

# 	@staticmethod
# 	def create(postData, serialized = False):
# 		#serialized = kwargs.pop('serialized', False)
# 		serializedModel = Organization.serializerObject(data = postData)
# 		if serializedModel.is_valid():
# 			obj = serializedModel.save()
# 			if serialized:
# 				return serializedModel.data
# 			else:
# 				return obj
# 		else:
# 			print "failed to be created!"
# 			print serializedModel.errors
# 			# failed to create object
# 			return serializedModel.errors

# 	@staticmethod
# 	def serialize(items):
# 		if items.__class__.__name__ == "QuerySet":
# 			return Organization.serializerObject(items, many = True).data
# 		else:
# 			return Organization.serializerObject(items.model).data


class Organization:
	class ObjectDoesNotExist(CssefObjectDoesNotExist):
		def __init__(self, message):
			self.message = message

		def __str__(self):
			return repr(self.message)

	serializerObject = OrganizationSerializer
	modelObject = OrganizationModel
	def __init__(self, **kwargs):
		self.model = kwargs.pop('modelInst', None)
		if not self.model:
		# 	self.model = Organization.modelObject.objects.get(**kwargs)
			try:
				self.model = Organization.modelObject.objects.get(**kwargs)
			except ObjectDoesNotExist:
				raise self.ObjectDoesNotExist("custom 1 - Organization matching query does not exist.")
			except modelObject.DoesNotExist:
				raise self.ObjectDoesNotExist("custom 2 - Organization matching query does not exist.")

	def delete(self):
		if self.model.deleteable:
			self.model.delete()

	@staticmethod
	def search(**kwargs):
		return wrappedSearch(Organization, Organization.modelObject, **kwargs)

	@staticmethod
	def create(postData, serialized = False):
		serializedModel = Organization.serializerObject(data = postData)
		if serializedModel.is_valid():
			obj = serializedModel.save()
			if serialized:
				return serializedModel.data
			else:
				return obj
		else:
			print "failed to be created!"
			print serializedModel.errors
			# failed to create object
			return serializedModel.errors

	@staticmethod
	def serialize(items):
		if items.__class__.__name__ == "QuerySet":
			return Organization.serializerObject(items, many = True).data
		else:
			return Organization.serializerObject(items.model).data	

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
			return Competition.serialize(Competition.search(organization = self.model.organizationId, **kwargs))
		else:
			return Competition.search(organization = self.model.organizationId, **kwargs)

	def getMembers(self, **kwargs):
		if kwargs.pop('serialized', None):
			return User.serialize(User.search(organizationId = self.model.organizationId, **kwargs))
		else:
			return User.search(organizationId = self.model.organizationId, **kwargs)

	def getCompetition(self, **kwargs):
		if kwargs.pop('serialized', None):
			return Competition.serialize(Competition(**kwargs))
		else:
			return Competition(**kwargs)

	def getMember(self, **kwargs):
		if kwargs.pop('serialized', None):
			return User.serialize(User(**kwargs))
		else:
			return User(**kwargs)

	def createCompetition(self, postData, serialized = False):
		if self.model.numCompetitions >= self.getMaxCompetitions():
			raise MaxCompetitionsReached(self.getMaxCompetitions())
		#postData['serialized'] = serialized
		postData['organization'] = self.model.organizationId
		newCompetition = Competition.create(postData, serialized = True)
		self.setNumCompetitions()
		return newCompetition

	def createMember(self, postData, serialized = False):
		if self.model.numMembers >= self.getMaxMembers():
			raise MaxMembersReached(self.getMaxMembers())
		#postData['serialized'] = serialized
		postData['organizationId'] = self.model.organizationId
		newUser = User.create(postData, serialized = True)
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

class Plugin:
	def __init__(self, pluginModelInst = None, **kwargs):
		self.model = pluginModelInst
		if not self.model:
			self.model = PluginModel(**kwargs)
			self.model.save()

	def delete(self):
		self.model.delete()

	@staticmethod
	def search(**kwargs):
		return wrappedSearch(Plugin, PluginModel, **kwargs)

	def getName(self):
		return self.model.name

	def setName(self, name):
		self.model.name = name
		self.model.save()

	def getDescription(self):
		return self.model.description

	def setDescription(self, description):
		self.model.description = description
		self.model.save()

	def getModuleName(self):
		#return Document.objects.get(servicemodule = self.servicemodule).filename.split(".")[0]
		pass

	def getImportPath(self, moduleName = None):
		if moduleName:
			#return settings.CONTENT_PLUGGINS_PATH.replace('/','.')[1:] + moduleName
			return ""
		else:
			return self.getImportPath(self.getModuleName())

class User:
	class ObjectDoesNotExist(CssefObjectDoesNotExist):
		def __init__(self, message):
			self.message = message

		def __str__(self):
			return repr(self.message)

	serializerObject = UserSerializer
	modelObject = UserModel
	def __init__(self, **kwargs):
		self.model = kwargs.pop('userModelInst', None)
		if not self.model:
			try:
				self.model = User.modelObject.objects.get(**kwargs)
			except ObjectDoesNotExist:
				raise self.ObjectDoesNotExist("custom 1 - User matching query does not exist.")
			except modelObject.DoesNotExist:
				raise self.ObjectDoesNotExist("custom 2 - User matching query does not exist.")

	def delete(self):
		self.model.delete()

	@staticmethod
	def count(**kwargs):
		return User.modelObject.objects.filter(**kwargs).count()

	@staticmethod
	def search(**kwargs):
		return wrappedSearch(User, UserModel, **kwargs)

	@staticmethod
	def create(postData, serialized = False):
		serializedModel = User.serializerObject(data = postData)
		if serializedModel.is_valid():
			obj = serializedModel.save()
			if serialized:
				return serializedModel.data
			else:
				return obj
		else:
			print "failed to be created!"
			print serializedModel.errors
			# failed to create object
			return serializedModel.errors

	@staticmethod
	def serialize(items):
		if items.__class__.__name__ == "QuerySet":
			return User.serializerObject(items, many = True).data
		else:
			return User.serializerObject(items.model).data		

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

def wrappedSearch(objType, objTypeModel, **kwargs):
	serialized = kwargs.pop('serialized', False)
	modelResults = objTypeModel.objects.filter(**kwargs)
	if serialized:
		return objType.serialize(modelResults)
	else:
		#return objType(modelInst = modelResults)
		return modelResults

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

