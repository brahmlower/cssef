from cssefserver.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class CssefObjectDoesNotExist(Exception):
	'An exception for when the requested object does not exist - not needed I think'
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return repr(self.message)

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
			tmpDict[i] = getattr(self, i)
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
			print pkid
			return None

	@classmethod
	def fromDict(cls, db, kwDict):
		modelObjectInst = cls.modelObject(**kwDict)
		db.add(modelObjectInst)
		db.commit()
		return cls(db, modelObjectInst)

def databaseConnection(sqliteFilepath):
	'Returns a database session for the specified database'
	dbEngine = create_engine('sqlite:///' + sqliteFilepath)
	Base.metadata.create_all(dbEngine)
	Base.metadata.bind = dbEngine
	DBSession = sessionmaker(bind = dbEngine)
	return DBSession()