import time
import tokenlib
from cssefserver.framework.utils import ModelWrapper
from cssefserver.modules.account.models import User as UserModel
from cssefserver.modules.account.models import Organization as OrganizationModel
from cssefserver.modules.account.utils import PasswordHash
from cssefserver.modules.account.errors import *

# THIS IS HARDCODED, WHICH IS BAD
secretSalt = "Gv1Z5EYyCJzNuc6hEbj5fd+E2P4+iNFw"

class User(ModelWrapper):
	"""Defines a basic User object.

	This subclasses ModelWrapper, and uses user.models.User as it's database
	model.

	Attributes:
		modelObject (UserModel): Defines the model the object is associated
			with
		fields (list): Lists the fields within the associated model to present
			to the client
	"""
	modelObject = UserModel
	fields = [
		'name',
		'username',
		'password',
		'description',
		'organization']

	@property
	def name(self):
		"""Name of the user.

		This wraps the name attribute of the associated model.

		Returns:
			str: String containing the name of the User object.
		"""
		return self.model.name

	@name.setter
	def name(self, value):
		"""Sets the name of the User.

		This abstracts the process setting the new value in the database.

		Args:
			value (str): The value to set the name to.

		Returns:
			None:

		Example:
			<todo>
		"""
		self.model.name = value
		self.db.commit()

	@property
	def username(self):
		"""Username for the user.

		This wraps the username attribute of the associated model.

		Returns:
			str: String containing the username of the User object.
		"""
		return self.model.username

	@username.setter
	def username(self, value):
		"""Sets the username of the User.

		This abstracts the process setting the new value in the database.

		TODO: This will eventually have to check that the username is unique
		to the organization. If it has already been taken, thow an error.

		Args:
			value (str): The value to set the username to.

		Returns:
			None:

		Example:
			<todo>
		"""
		self.model.username = value
		self.db.commit()

	@property
	def password(self):
		"""Password for the user.

		This wraps the password attribute of the associated model.

		Returns:
			PasswordHash: Contains the hash of the users password. The hash
			itself can be extracted by reading the PasswordHash.hash
			attribute. See PasswordHash for more information.

		Example:
			The following is an example shows instantiating an existing user
			via its pkid, displaying the value type of its password attribute,
			then retrieving the password hash from the PasswordHash object.::

				>>> u = User(pkid = 1)
				>>> type(u.password)
				<type 'PasswordHash'>
				>>> print u.password.hash
				abiglonghashisprintedhere
				>>>

		"""
		return PasswordHash(self.model.password)

	@password.setter
	def password(self, value):
		"""Sets the password for the User.

		This abstracts the process setting the new value in the database.

		Args:
			value (str): Plaintext value the password should be set to.

		Returns:
			None:

		Example:
			<todo>
		"""
		rounds = 10
		ph = PasswordHash.new(value, rounds)
		self.model.password = ph.hash
		self.db.commit()
		#return ph.hash # Commented out because returning a value might be really weird since this is a @property...

	@property
	def description(self):
		"""Description for the user.

		This wraps the description attribute of the associated model.

		Returns:
			str: String containing the description of the User object.
		"""
		return self.model.description

	@description.setter
	def description(self, value):
		"""Sets the description for the User.

		This abstracts the process setting the new value in the database.

		Args:
			value (str): The value to set the description to.

		Returns:
			None:

		Example:
			<todo>
		"""
		self.model.description = value
		self.db.commit()

	@property
	def organization(self):
		"""Sets the description for the User.

		This abstracts the process setting the new value in the database. This
		should eventaully instantiate an instance of the Organization with the
		associated ID and then return that, rather than just the ID.

		Returns:
			Int: Represents the Organization ID.

		Example:
			<todo>
		"""
		return self.model.organization

	@organization.setter
	def organization(self, value):
		"""Sets the organization the User is a part of.

		This abstracts the process setting the new value in the database. This
		will eventually require additional processes to authorize the moving
		of an account from one organization to another.

		Args:
			value (int): The organization ID of the organization to put the
				user in.

		Returns:
			None:

		Example:
			<todo>
		"""
		self.model.organization = value
		self.db.commit()

	@classmethod
	def fromDict(cls, db, kwDict):
		org = Organization.fromDatabase(db, pkid = kwDict['organization'])
		if not org:
			print "Failed to get organization with pkid '%s'" % kwDict['organization']
			raise ValueError
		if org.model.numMembers >= org.maxMembers:
			raise MaxMembersReached(org.maxMembers)
		# Copied right from ModelWrapper.fromDict
		modelObjectInst = cls.modelObject()
		clsInst = cls(db, modelObjectInst)
		for i in kwDict:
			if i in clsInst.fields:
				setattr(clsInst, i, kwDict[i])
		db.add(clsInst.model)
		db.commit()
		org.setNumMembers()
		return clsInst

	def authorized(self, authDict, group):
		# Testing right now
		return True

	def authenticate(self, authDict):
		print authDict.keys()
		if 'token' in authDict.keys():
			# Do token authentication
			return self.authenticateToken(authDict['token'])
		elif 'password' in authDict.keys():
			# Do password authentication
			return self.authenticatePassword(authDict['password'], returnToken = False)
		else:
			# Cannot authenticate!
			print "There was no password or token!"
			return False

	def authenticateToken(self, token):
		"""Check if the provided token is valid for this user.

		This abstracts the process setting the new value in the database. This
		will eventually require additional processes to authorize the moving
		of an account from one organization to another.

		Args:
			value (int): The organization ID of the organization to put the
				user in.

		Returns:
			bool: True if the token belongs to the user and contains the
			correct user ID and organization ID. False if the token does not
			belong to the user, or contains an incorrect user ID or
			organization ID.

		Example:
			<todo>
		"""
		tk = tokenlib.parse_token(token, secret = secretSalt, now = time.time())
		return tk['id'] == self.getId() and tk['username'] == self.username and tk['organization'] == self.organization

	def authenticatePassword(self, password, returnToken = True):
		"""Check if the provided plaintext password is valid for this user.

		This will check that the provided password matches the users password.
		The actual password comparison is done through the __eq__ attribute of
		the PasswordHash class. A token is created and returned if the
		password is correct, allowing the user to make further requests
		without having to reauthenticate each time.

		Args:
			password (str): Plaintext password candidate

		Returns:
			str: When the password is password correct, a new token to
				validate further requests is returned. Returns none if
				password is incorrect.
		"""
		if self.password == password:
			if not returnToken:
				return True
			else:
				tokenDict = {"id": self.getId(), "username": self.username, "organization": self.organization}
				token = tokenlib.make_token(tokenDict, secret = secretSalt)
				return token
		else:
			return None

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

	# def setNumCompetitions(self):
	# 	self.model.numCompetitions = Competition.count(self.db, organization = self.getId())
	# 	self.db.commit()

	# def getCompetitions(self, **kwargs):
	# 	return Competition.search(Competition, organization = self.getId(), **kwargs)

	def getMembers(self, **kwargs):
		return User.search(User, organization = self.getId(), **kwargs)

	# def getCompetition(self, **kwargs):
	# 	return Competition(**kwargs)

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

	# def createCompetition(self, kwDict):
	# 	"""Creates a new competition that is automatically added to the organization

	# 	Crates a competition through Organization.createMember() ensures that
	# 	organization restrictions are checked and updated during the
	# 	competition creation process.

	# 	Args:
	# 		kwDict (dict): A dictionary containing keywords that will be
	# 			passed to Competition.fromDict().

	# 	Returns:
	# 		User: Returns the competition that is created if successful. None
	# 		if competition creation fails.

	# 	Raises:
	# 		MaxCompetitionsReached: If the organization already has the
	# 		maximum number of competitions.
	# 	"""
	# 	if self.model.numCompetitions >= self.maxCompetitions:
	# 		raise MaxCompetitionsReached(self.maxCompetitions)
	# 	kwDict['organization'] = self.getId()
	# 	newCompetition = Competition.fromDict(self.db, kwDict)
	# 	self.setNumCompetitions()
	# 	return newCompetition