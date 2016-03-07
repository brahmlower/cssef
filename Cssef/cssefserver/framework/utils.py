import traceback
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cssefserver.framework import dbPath
from cssefserver.framework.models import Base

class CssefObjectDoesNotExist(Exception):
	'An exception for when the requested object does not exist - not needed I think'
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return repr(self.message)

class PasswordHash(object):
	"""
	This code pulled from http://variable-scope.com/posts/storing-and-verifying-passwords-with-sqlalchemy
	There are a couple minor changes to it, but most credit goes Elmer de Looff - Thank you!
	"""
    def __init__(self, hash_):
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

class ModelWrapper(object):
	'The base class for wrapping model objects'
	class ObjectDoesNotExist(CssefObjectDoesNotExist):
		def __init__(self, message):
			self.message = message

		def __str__(self):
			return repr(self.message)

	modelObject = None
	fields = None

	def __init__(self, db, model):
		self.db = db
		self.model = model

	def getId(self):
		return self.model.pkid

	def edit(self, **kwargs):
		for i in kwargs:
			if i in self.fields:
				setattr(self, i, kwargs[i])

	def delete(self):
		self.db.delete(self.model)
		self.db.commit()

	def asDict(self):
		tmpDict = {}
		tmpDict['id'] = self.getId()
		for i in self.fields:
			try:
				tmpDict[i] = getattr(self, i)
			except AttributeError:
				# The field is not an attribute of the subclassed model wrapper
				# We'll try to find it in the classes modesl
				tmpDict[i] = getattr(self.mode, i)
		return tmpDict

	@classmethod
	def count(cls, db, **kwargs):
		return db.query(cls.modelObject).filter_by(**kwargs).count()

	@classmethod
	def search(cls, db, **kwargs):
		modelObjectList = db.query(cls.modelObject).filter_by(**kwargs)
		clsList = []
		for i in modelObjectList:
			clsList.append(cls(db, i))
		return clsList

	@classmethod
	def fromDatabase(cls, db, pkid):
		try:
			return cls.search(db, pkid = pkid)[0]
		except IndexError:
			#print pkid
			return None

	@classmethod
	def fromDict(cls, db, kwDict):
		modelObjectInst = cls.modelObject()
		clsInst = cls(db, modelObjectInst)
		for i in kwDict:
			if i in clsInst.fields:
				setattr(clsInst, i, kwDict[i])
		db.add(clsInst.model)
		db.commit()
		return clsInst

def databaseConnection(sqliteFilepath):
	'Returns a database session for the specified database'
	dbEngine = create_engine('sqlite:///' + sqliteFilepath)
	Base.metadata.create_all(dbEngine)
	Base.metadata.bind = dbEngine
	DBSession = sessionmaker(bind = dbEngine)
	return DBSession()

def handleException(e):
	# todo
	# log the full stacktrace!
	returnDict = getEmptyReturnDict()
	returnDict['value'] = 1
	returnDict['message'] = traceback.format_exc().splitlines()
	return returnDict

def getEmptyReturnDict():
	return {
		'value': 0,
		'message': 'Success',
		'content': []
	}

def modelDel(cls, pkid):
	db = databaseConnection(dbPath)
	if pkid == "*":
		# todo: implement a wildcard
		returnDict = getEmptyReturnDict()
		returnDict['value'] = 1
		returnDict['message'] = ["Wildcards are not implemented yet."]
		return returnDict
	elif type(pkid) == str and "-" in pkid:
		x = pkid.split("-")
		if len(x) == 2:
			try:
				for pkid in range(int(x[0]), int(x[1])+1):
					modelObj = cls.fromDatabase(db, pkid)
					if modelObj:
						modelObj.delete()
			except ValueError:
				# One of the ranges provided could not be cast as an integer. Return error.
				returnDict = getEmptyReturnDict()
				returnDict['value'] = 1
				returnDict['message'] = ["Range value could not be cast to integer. Expected integer range like 1-4. Got '%s' instead." % pkid]
				return returnDict
		else:
			print x
			returnDict = getEmptyReturnDict()
			returnDict['value'] = 1
			returnDict['message'] = ["Expected integer range like 1-4. Got '%s' instead." % pkid]
			return returnDict
	elif type(pkid) == int:
		modelObj = cls.fromDatabase(db, pkid)
		modelObj.delete()
	else:
		# We don't know what the hell we were given. Disregard it and thow an error :(
		returnDict = getEmptyReturnDict()
		returnDict['value'] = 1
		returnDict['message'] = ["Expected integer value (5) or range (2-7). Got '%s' of type %s instead." % (str(pkid), str(type(pkid)))]
	return getEmptyReturnDict()

def modelSet(cls, pkid, **kwargs):
	db = databaseConnection(dbPath)
	modelObj = cls.fromDatabase(db, pkid)
	modelObj.edit(**kwargs)
	returnDict = getEmptyReturnDict()
	returnDict['content'].append(modelObj.asDict())
	return returnDict

def modelGet(cls, **kwargs):
	db = databaseConnection(dbPath)
	modelObjs = cls.search(db, **kwargs)
	returnDict = getEmptyReturnDict()
	for i in modelObjs:
		returnDict['content'].append(i.asDict())
	return returnDict