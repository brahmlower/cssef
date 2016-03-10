import time
import tokenlib
from cssefserver.framework.utils import PasswordHash
from cssefserver.framework.utils import ModelWrapper
from cssefserver.modules.user.models import User as UserModel

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

	def authenticatePassword(self, password):
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
			tokenDict = {"id": self.getId(), "username": self.username, "organization": self.organization}
			token = tokenlib.make_token(tokenDict, secret = secretSalt)
			return token
		else:
			return None