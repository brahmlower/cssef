from cssefserver.models import ScoringEngine as ScoringEngineModel
from cssefserver.models import Organization as OrganizationModel
from cssefserver.models import Document as DocumentModel
from cssefserver.models import User as UserModel

from cssefserver.framework.utils import ModelWrapper
from cssefserver.framework.competition import Competition

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
	fields = [
		'name',
		'url',
		'description',
		'maxMembers',
		'maxCompetitions']

	def isDeleteable(self):
		return self.model.deleteable

	@property
	def name(self):
		return self.model.name

	@name.setter
	def name(self, value):
		self.model.name = value
		self.db.commit()

	@property
	def url(self):
		return self.model.url

	@url.setter
	def url(self,value):
		self.model.url = value
		self.db.commit()

	@property
	def description(self):
		return self.model.description

	@description.setter
	def description(self, value):
		self.model.description = value
		self.db.commit()

	@property
	def maxMembers(self):
		return self.model.maxMembers

	@maxMembers.setter
	def maxMembers(self, value):
		self.model.maxMembers = value
		self.db.commit()

	@property
	def maxCompetitions(self):
		return self.model.maxCompetitions

	@maxCompetitions.setter
	def maxCompetitions(self, value):
		self.model.maxCompetitions = value
		self.db.commit()

	def getNumMembers(self):
		return self.model.numMembers

	def setNumMembers(self):
		self.model.numMembers = User.count(self.db, organization = self.getId())
		self.db.commit()

	def getNumCompetitions(self):
		return self.model.setNumCompetitions

	def setNumCompetitions(self):
		self.model.numCompetitions = Competition.count(self.db, organization = self.getId())
		self.db.commit()

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
		newCompetition = Competition.fromDict(self.db, kwDict)
		self.setNumCompetitions()
		return newCompetition

	def createMember(self, kwDict):
		if self.model.numMembers >= self.maxMembers:
			raise MaxMembersReached(self.maxMembers)
		kwDict['organization'] = self.getId()
		newUser = User.fromDict(self.db, kwDict)
		self.setNumMembers()
		return newUser

class User(ModelWrapper):
	modelObject = UserModel
	fields = [
		'name',
		'username',
		'password',
		'description',
		'organization']

	@property
	def name(self):
		return self.model.name

	@name.setter
	def name(self, value):
		self.model.name = value
		self.db.commit()

	@property
	def username(self):
		return self.model.username

	@username.setter
	def username(self, value):
		self.model.username = value
		self.db.commit()

	@property
	def password(self):
		return self.model.password

	@password.setter
	def password(self, value):
		self.model.password = value
		self.db.commit()

	@property
	def description(self):
		return self.model.description

	@description.setter
	def description(self, value):
		self.model.description = value
		self.db.commit()

	@property
	def organization(self):
		return self.model.organization

	@organization.setter
	def organization(self, value):
		self.model.organization = value
		self.db.commit()

class ScoringEngine(ModelWrapper):
	modelObject = ScoringEngineModel
	fields = [
		'name',
		'disabled',
		'packageName']

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
		self.db.commit()

	@property
	def disabled(self):
		return self.model.disabled

	@disabled.setter
	def disabled(self, value):
		self.model.disabled = value
		self.db.commit()

	@property
	def packageName(self):
		return self.model.packageName

	@packageName.setter
	def packageName(self, value):
		self.model.packageName = value
		self.db.commit()

class Document(ModelWrapper):
	modelObject = DocumentModel
	fields = [
		'contentType',
		'fileHash',
		'fielPath',
		'fileName',
		'urlEncodedFileName']

	@property
	def contentType(self):
		return self.model.contentType

	@contentType.setter
	def contentType(self, value):
		self.model.contentType = value
		self.db.commit()

	@property
	def fileHash(self):
		return self.model.fileHash

	@fileHash.setter
	def fileHash(self, value):
		self.model.fileHash = value
		self.db.commit()

	@property
	def filePath(self):
		return self.model.filePath

	@filePath.setter
	def filePath(self, value):
		self.model.filePath = value
		self.db.commit()

	@property
	def fileName(self):
		return self.model.fileName

	@fileName.setter
	def fileName(self, value):
		self.model.fileName = value
		self.db.commit()

	@property
	def urlEncodedFileName(self):
		return self.model.urlEncodedFileName

	@urlEncodedFileName.setter
	def setUrlEncodedFileName(self, value):
		self.model.urlEncodedFileName = value
		self.db.commit()