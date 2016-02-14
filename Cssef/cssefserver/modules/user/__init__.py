from cssefserver.framework.utils import ModelWrapper
from cssefserver.modules.user.models import User as UserModel

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