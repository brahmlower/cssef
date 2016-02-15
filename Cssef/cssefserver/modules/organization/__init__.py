from cssefserver.framework.utils import ModelWrapper
from cssefserver.modules.organization.models import Organization as OrganizationModel
from cssefserver.modules.organization.errors import *
from cssefserver.modules.user import User
from cssefserver.modules.competition import Competition

class Organization(ModelWrapper):
	modelObject = OrganizationModel
	fields = [
		'name',
		'url',
		'description',
		'maxMembers',
		'maxCompetitions',
		'canAddUsers',
		'canDeleteUsers',
		'canAddCompetitions',
		'canDeleteCompetitions']

	def asDict(self):
		tmpDict = super(Organization, self).asDict()
		tmpDict['deletable'] = self.isDeletable()
		return tmpDict

	def isDeletable(self):
		return self.model.deletable

	@property
	def canAddUsers(self):
		return self.model.canAddUsers

	@canAddUsers.setter
	def canAddUsers(self, value):
		self.model.canAddUsers = value
		self.db.commit()

	@property
	def canDeleteUsers(self):
		return self.model.canDeleteUsers

	@canDeleteUsers.setter
	def canDeleteUsers(self, value):
		self.model.canDeleteUsers = value
		self.db.commit()

	@property
	def canAddCompetitions(self):
		return self.model.canAddCompetitions

	@canAddCompetitions.setter
	def canAddCompetitions(self, value):
		self.model.canAddCompetitions = value
		self.db.commit()

	@property
	def canDeleteCompetitions(self):
		return self.model.canDeleteCompetitions

	@canDeleteCompetitions.setter
	def canDeleteCompetitions(self, value):
		self.model.canDeleteCompetitions = value
		self.db.commit()

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