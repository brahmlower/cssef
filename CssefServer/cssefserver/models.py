from sqlalchemy.ext.declarative import declarative_base
from cssefserver import config

class Base(object):
	@declared_attr
	def __tablename__(cls):
		tablePrefix = config.database_table_prefix
		modulePrefix = "test"
		moduleName = self.__class__.__name__.lower()
		self.__tablename__ = "%s_%s_%s" % (tablePrefix, modulePrefix, moduleName)

DbBase = declarative_base(cls=Base)

class Model(DbBase):
	__tablename__ = ''
	def __init__(self):
		tablePrefix = config.database_table_prefix
		modulePrefix = "test"
		moduleName = self.__class__.__name__.lower()
		self.__tablename__ = "%s_%s_%s" % (tablePrefix, modulePrefix, moduleName)