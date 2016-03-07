import time
import tokenlib
from cssefserver.framework.utils import PasswordHash
from cssefserver.framework.utils import ModelWrapper
from cssefserver.modules.user.models import User as UserModel

# THIS IS HARDCODED, WHICH IS BAD
secretSalt = "Gv1Z5EYyCJzNuc6hEbj5fd+E2P4+iNFw"

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
		return PasswordHash(self.model.password)

	@password.setter
	def password(self, value):
		rounds = 10
		ph = PasswordHash.new(value, rounds)
		self.model.password = ph.hash
		self.db.commit()
		return ph.hash

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

	def authenticateToken(self, token):
		tk = tokenlib.parse_token(token, secret = secretSalt, now = time.time())
		return tk['id'] == self.getId() and tk['username'] == self.username and tk['organization'] == self.organization

	def authenticatePassword(self, password):
		if self.password == password:
			tokenDict = {"id": self.getId(), "username": self.username, "organization": self.organization}
			token = tokenlib.make_token(tokenDict, secret = secretSalt)
			return token
		else:
			return None