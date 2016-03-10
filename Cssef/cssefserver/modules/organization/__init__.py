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
		"""Provides a dictionary representation of the Organization

		Builds and returns a dictionary representing the values in the
		Organizations `fields` attribute. Organization.asDict() includes the
		readonly attribute `deletable`.

		Returns:
		    dict: A dictionary that represents the same values in the object.
		"""
		tmpDict = super(Organization, self).asDict()
		tmpDict['deletable'] = self.isDeletable()
		return tmpDict

	def isDeletable(self):
		"""Checks if the organization can be deleted.

		Return:
		    bool: True if the organization can be deleted, false if it cannot
		    be deleted.
		"""
		return self.model.deletable

	@property
	def canAddUsers(self):
		"""If the organization can add their own users

		This wraps the `canAddUsers` attribute of the associated model.

		Returns:
			bool: True if the organization can add its own users, false if not
		"""
		return self.model.canAddUsers

	@canAddUsers.setter
	def canAddUsers(self, value):
		self.model.canAddUsers = value
		self.db.commit()

	@property
	def canDeleteUsers(self):
		"""If the organization can delete their own users.

		This wraps the `canDeleteUsers` attribute of the associated model.

		Returns:
			str: True if the organization can delete its own users, false if
				not
		"""
		return self.model.canDeleteUsers

	@canDeleteUsers.setter
	def canDeleteUsers(self, value):
		self.model.canDeleteUsers = value
		self.db.commit()

	@property
	def canAddCompetitions(self):
		"""If the organization can add their own competitions

		This wraps the `canAddCompetitions` attribute of the associated model.

		Returns:
			bool: True if the organization can add its own competitions, false
				if not
		"""
		return self.model.canAddCompetitions

	@canAddCompetitions.setter
	def canAddCompetitions(self, value):
		self.model.canAddCompetitions = value
		self.db.commit()

	@property
	def canDeleteCompetitions(self):
		"""If the organization can delete their own competitions.

		This wraps the `canDeleteCompetitions` attribute of the associated model.

		Returns:
			str: True if the organization can delete its own competitions,
				false if not
		"""
		return self.model.canDeleteCompetitions

	@canDeleteCompetitions.setter
	def canDeleteCompetitions(self, value):
		self.model.canDeleteCompetitions = value
		self.db.commit()

	@property
	def name(self):
		"""Name of the organization.

		This wraps the `name` attribute of the associated model.

		Returns:
			str: String containing the name of the Organization object.
		"""
		return self.model.name

	@name.setter
	def name(self, value):
		self.model.name = value
		self.db.commit()

	@property
	def url(self):
		"""URL value for the organization.

		This wraps the `url` attribute of the associated model.

		Returns:
			str: String containing the url of the Organization object.
		"""
		return self.model.url

	@url.setter
	def url(self,value):
		self.model.url = value
		self.db.commit()

	@property
	def description(self):
		"""Description of the organization.

		This wraps the `description` attribute of the associated model.

		Returns:
			str: String containing the description of the Organization object.
		"""
		return self.model.description

	@description.setter
	def description(self, value):
		self.model.description = value
		self.db.commit()

	@property
	def maxMembers(self):
		"""Mamimum number of members of the organization can have.

		Integer value representing the maximum number of members the 
		organization may have.This wraps the `maxMembers` attribute of the
		associated model. 

		Returns:
			int:
		"""
		return self.model.maxMembers

	@maxMembers.setter
	def maxMembers(self, value):
		self.model.maxMembers = value
		self.db.commit()

	@property
	def maxCompetitions(self):
		"""Mamimum number of competitions of the organization can have.

		Integer value representing the maximum number of members the 
		organization may have.This wraps the `maxCompetitions` attribute of
		the associated model. 

		Returns:
			int:
		"""
		return self.model.maxCompetitions

	@maxCompetitions.setter
	def maxCompetitions(self, value):
		self.model.maxCompetitions = value
		self.db.commit()

	def getNumMembers(self):
		"""Gets the current number of competitions belonging to the organization

		This gets the "cached" count of the current number of competitions
		that belong to the organization.

		Returns:
		    int: The number of competitions that are part of the organization
		"""
		return self.model.numMembers

	def setNumMembers(self):
		"""Gets the current number of members in the organization

		This gets the "cached" count of the current number of users that are
		part of the organization.

		Returns:
		    int: The number of users that are part of the oragnizaiton
		"""
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
		"""Gets a specific member that belongs to the organization

		This will retrieve a specific user that belongs to the organization.

		TODO: This function is supposed to add `organization = self.getId()`
		to the keywords that are used to select the user from the database,
		but it does not.

		Args:
		    **kwargs: Keyword arguments that define the user to match.

		Returns:
		    User: A user that belongs to the organization
		"""
		return User(**kwargs)

	def createCompetition(self, kwDict):
		"""Creates a new competition that is automatically added to the organization

		Crates a competition through Organization.createMember() ensures that
		organization restrictions are checked and updated during the
		competition creation process.

		Args:
		    kwDict (dict): A dictionary containing keywords that will be
		    	passed to Competition.fromDict().

		Returns:
		    User: Returns the competition that is created if successful. None
		    if competition creation fails.

		Raises:
		    MaxCompetitionsReached: If the organization already has the
		    maximum number of competitions.
		"""
		if self.model.numCompetitions >= self.maxCompetitions:
			raise MaxCompetitionsReached(self.maxCompetitions)
		kwDict['organization'] = self.getId()
		newCompetition = Competition.fromDict(self.db, kwDict)
		self.setNumCompetitions()
		return newCompetition

	def createMember(self, kwDict):
		"""Creates a new user that is automatically added to the organization

		Creating a user through Organization.createMember() ensures that
		organization restrictions are checked and updated during the user
		creation process. They wouldn't be if the user was added simply by
		calling User.fromDict().

		TODO: Change that, because user creation using this method sucks...

		Args:
		    kwDict (dict): A dictionary containing keywords that will be
		    	passed to User.fromDict().

		Returns:
		    User: Returns the user that is created if successful. None if user
		    creation fails.

		Raises:
		    MaxMembersReached: If the organization already has the maximum
		    number of users.
		"""
		if self.model.numMembers >= self.maxMembers:
			raise MaxMembersReached(self.maxMembers)
		kwDict['organization'] = self.getId()
		newUser = User.fromDict(self.db, kwDict)
		self.setNumMembers()
		return newUser