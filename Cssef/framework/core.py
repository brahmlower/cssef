from models import ScoringEngine as ScoringEngineModel
from models import Organization as OrganizationModel
from models import Document as DocumentModel
from models import User as UserModel

from framework.utils import ModelWrapper
from framework.competition import Competition

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

class Organization(ModelWrapper):
	modelObject = OrganizationModel

	class __metaclass__(type):
		def __str__(self):
			return "Organization '%s' (id: %d)" % (self.name, self.getId())

	def edit(self, **kwargs):
		for i in kwargs:
			if i == 'name':					self.name = kwargs.get(i)
			elif i == 'url':				self.url = kwargs.get(i)
			elif i == 'description':		self.description = kwargs.get(i)
			elif i == 'maxMembers':			self.maxMembers = kwargs.get(i)
			elif i == 'maxCompetitions':	self.maxCompetitions = kwargs.get(i)

	def isDeleteable(self):
		return self.model.deleteable

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
	def url(self,value):
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
	def maxMembers(self):
		return self.model.maxMembers

	@maxMembers.setter
	def maxMembers(self, value):
		self.model.maxMembers = value
		self.model.save()

	@property
	def maxCompetitions(self):
		return self.model.maxCompetitions

	@maxCompetitions.setter
	def maxCompetitions(self, value):
		self.model.maxCompetitions = values
		self.model.save()

	def getNumMembers(self):
		return self.model.numMembers

	def setNumMembers(self):
		self.model.numMembers = User.count(organization = self.getId())
		self.model.save()

	def getNumCompetitions(self):
		return self.model.setNumCompetitions

	def setNumCompetitions(self):
		self.model.numCompetitions = Competition.count(organization = self.getId())
		self.model.save()

	def getCompetitions(self, **kwargs):
		return Competition.search(Competition, organization = self.getId(), **kwargs)

	def getMembers(self, **kwargs):
		return User.search(User, organization = self.getId(), **kwargs)

	def getCompetition(self, **kwargs):
		return Competition(**kwargs)

	def getMember(self, **kwargs):
		return User(**kwargs)

	def createCompetition(self, kwDict):
		if self.model.numCompetitions >= self.maxCompetitions:
			raise MaxCompetitionsReached(self.maxCompetitions)
		kwDict['organization'] = self.getId()
		newCompetition = Competition.create(kwDict)
		self.setNumCompetitions()
		return newCompetition

	def createMember(self, kwDict):
		if self.model.numMembers >= self.maxMembers:
			raise MaxMembersReached(self.maxMembers)
		kwDict['organization'] = self.getId()
		newUser = User.create(kwDict)
		self.setNumMembers()
		return newUser

	def deleteCompetition(self, **kwargs):
		competition = self.getCompetition(**kwargs)
		competition.delete()
		self.setNumCompetitions()

	def deleteMember(self, **kwargs):
		member = self.getMember(**kwargs)
		member.delete()
		self.setNumMembers()

	def editMember(self, **kwargs):
		member = self.getMember(pkid = kwargs.pop('pkid', None))
		return member.edit(**kwargs)

	def editCompetition(self, **kwargs):
		competition = self.getCompetition(pkid = kwargs.pop('pkid', None))
		return competition.edit(**kwargs)

class User(ModelWrapper):
	modelObject = UserModel

	@staticmethod
	def count(**kwargs):
		return User.modelObject.objects.filter(**kwargs).count()

	def edit(self, **kwargs):
		for i in kwargs:
			if i == 'name':				self.name = kwargs.get(i)
			elif i == 'username':		self.username = kwargs.get(i)
			elif i == 'password':		self.password = kwargs.get(i)
			elif i == 'description':	self.description = kwargs.get(i)
			elif i == 'organization':	self.organization = kwargs.get(i)

	@property
	def name(self):
		return self.model.name

	@name.setter
	def name(self, value):
		self.model.name = value
		self.model.save()

	@property
	def username(self):
		return self.model.username

	@username.setter
	def username(self, value):
		self.model.username = value
		self.model.save()

	@property
	def password(self):
		return self.model.password

	@password.setter
	def password(self, value):
		self.model.password = value
		self.model.save()

	@property
	def description(self):
		return self.model.description

	@description.setter
	def description(self, value):
		self.model.description = value
		self.model.save()

	@property
	def organization(self):
		return self.model.organization

	@organization.setter
	def organization(self, value):
		self.model.organization = value
		self.model.save()

class ScoringEngine(ModelWrapper):
	modelObject = ScoringEngineModel

	def delete(self):
		print '[WARNING] Cannot delete ScoringEngine. Redirecting to disable.'
		return self.disable()

	def disable(self):
		self.disabled = True

	def enable(self):
		self.disabled = False

	@property
	def name(self):
		return self.model.name

	@name.setter
	def name(self, value):
		self.model.name = value
		self.model.save()

	@property
	def disabled(self):
		return self.model.disabled

	@disabled.setter
	def disabled(self, value):
		self.model.disabled = value
		self.model.save()

	@property
	def packageName(self):
		return self.model.packageName

	@packageName.setter
	def packageName(self, value):
		self.model.packageName = value
		self.model.save()

class Document(ModelWrapper):
	modelObject = DocumentModel

	def edit(self, **kwargs):
		for i in kwargs:
			if i == 'contentType':			self.contentType = kwargs.get(i)
			elif i == 'fileHash':			self.fileHash = kwargs.get(i)
			elif i == 'filePath':			self.filePath = kwargs.get(i)
			elif i == 'filename':			self.fileName = kwargs.get(i)
			elif i == 'urlEncodedFilename': self.urlEncodedFilename = kwargs.get(i)

	@property
	def contentType(self):
		return self.model.contentType

	@contentType.setter
	def contentType(self, value):
		self.model.contentType = value
		self.model.save()

	@property
	def fileHash(self):
		return self.model.fileHash

	@fileHash.setter
	def fileHash(self, value):
		self.model.fileHash = value
		self.model.save()

	@property
	def filePath(self):
		return self.model.filePath

	@filePath.setter
	def filePath(self, value):
		self.model.filePath = value
		self.model.save()

	@property
	def fileName(self):
		return self.model.fileName

	@fileName.setter
	def fileName(self, value):
		self.model.fileName = value
		self.model.save()

	@property
	def urlEncodedFileName(self):
		return self.model.urlEncodedFileName

	@urlEncodedFileName.setter
	def setUrlEncodedFileName(self, value):
		self.model.urlEncodedFileName = value
		self.model.save()

def getObjects(db, classPointer, **kwargs):
	return classPointer.search(db, classPointer, **kwargs)

def getObject(classPointer, **kwargs):
	return classPointer(**kwargs)

def getCompetition(**kwargs):
	return getObject(Competition, **kwargs)

def getCompetitions(**kwargs):
	return getObjects(Competition, **kwargs)

def getOrganization(**kwargs):
	return getObject(Organization, **kwargs)

def getOrganizations(**kwargs):
	return getObjects(Organization, **kwargs)

def createOrganization(kwDict):
	return Organization.create(kwDict)

def deleteOrganization():
	pass

def getUser(**kwargs):
	return getObject(User, **kwargs)

def getUsers(**kwargs):
	return getObjects(User, **kwargs)

def getScoringEngine(**kwargs):
	return getObject(ScoringEngine, **kwargs)

def getScoringEngines(**kwargs):
	return getObjects(ScoringEngine, **kwargs)

def createScoringEngine(kwDict):
	return ScoringEngine.create(kwDict)