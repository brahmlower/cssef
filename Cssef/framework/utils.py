from models import Base
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

	def __init__(self, model):
		self.model = model

	def getId(self):
		return self.model.pkid

	def delete(self):
		self.model.delete()

	def reload(self,):
		self.model.refresh_from_db()

	@classmethod
	def search(cls, db, **kwargs):
		modelObjectList = db.query(cls.modelObject).filter_by(**kwargs)
		clsList = []
		for i in modelObjectList:
			clsList.append(cls(i))
		print clsList
		return clsList

	@classmethod
	def fromDatabase(cls, db, pkid):
		return cls.search(pkid = pkid)[0]

	@classmethod
	def fromDict(cls, db, kwDict):
		modelObjectInst = cls.modelObject(**kwDict)
		db.add(modelObjectInst)
		db.commit()
		return cls(modelObjectInst)

def databaseConnection(sqliteFilepath):
	'Returns a database session for the specified database'
	dbEngine = create_engine('sqlite:///' + sqliteFilepath)
	Base.metadata.create_all(dbEngine)
	Base.metadata.bind = dbEngine
	DBSession = sessionmaker(bind = dbEngine)
	return DBSession()