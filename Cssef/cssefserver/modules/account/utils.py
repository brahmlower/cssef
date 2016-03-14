import bcrypt
from cssefserver.framework.utils import Configuration
from cssefserver.framework.utils import returnError
import cssefserver.modules.account

class PasswordHash(object):
	"""
	This code pulled from http://variable-scope.com/posts/storing-and-verifying-passwords-with-sqlalchemy
	There are a couple minor changes to it, but most credit goes Elmer de Looff - Thank you!
	"""
	def __init__(self, hash_):
		"""Instantiates a PasswordHash object based on a provided string representing a bcrypt hash.

		Args:
			hash_ (str): The hash string to build the object off of.

		Raises:
			Assertion Error: If `hash_` is not of length 60.

			Assertion Error: If `hash_` does not contain three '$'.
		"""
		assert len(hash_) == 60, 'bcrypt hash should be 60 chars.'
		assert hash_.count('$'), 'bcrypt hash should have 3x "$".'
		self.hash = str(hash_)
		self.rounds = int(self.hash.split('$')[2])

	def __eq__(self, candidate):
		"""Hashes the candidate string and compares it to the stored hash."""
		if isinstance(candidate, basestring):
			if isinstance(candidate, unicode):
				candidate = candidate.encode('utf8')
			return bcrypt.hashpw(candidate, self.hash) == self.hash
		return False

	def __repr__(self):
		"""Simple object representation."""
		return self.hash

	@classmethod
	def new(cls, password, rounds):
		"""Creates a PasswordHash from the given password."""
		if isinstance(password, unicode):
			password = password.encode('utf8')
		return cls(bcrypt.hashpw(password, bcrypt.gensalt(rounds)))

def authorizeAccess(authDict, config):
	db = config.establishDatabaseConnection()
	# Check if we're doing user authentication, or admin token auth.
	if 'admin-token' in authDict:
		# Just check that the auth key matches that of the authkey in the server config file
		if config.admin_token == authDict['admin-token']:
			# Auth key matched!
			print "[AUTH INFO] Provided auth-token was correct."
			return None
		else:
			print "[AUTH WARNING] Provided auth-token was incorrect."
	# Importing for this got pretty ugly... :(
	if not authDict.get('username', None):
		print "[AUTH WARNING] No username provided."
		return returnError('no_user_provided')
	if not authDict.get('organization', None):
		print "[AUTH WARNING] No organization was provided."
		return returnError('no_organization_provided')
	userList = cssefserver.modules.account.User.search(db, username = authDict['username'], organization = authDict['organization'])
	if len(userList) < 1:
		# No matching user was found
		return returnError('user_not_found')
	if len(userList) > 1:
		# There are multiple users. This is extremely bad
		return returnError('multiple_users_found')
	user = userList[0]
	# Authenticate the user
	if not user.authenticate(authDict):
		return returnError('user_auth_failed')
	# Authorize the user
	if not user.authorized(authDict, 'organization'):
		return returnError('user_permission_denied')
	return None
