from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
import cssefserver

class BaseModel(object):
	@declared_attr
	def __tablename__(cls):
		tablePrefix = cssefserver.config.database_table_prefix
		modulePrefix = "test"
		moduleName = cls.__name__.lower()
		return "%s_%s_%s" % (tablePrefix, modulePrefix, moduleName)

	pkid =  Column(Integer, primary_key = True)

Base = declarative_base(cls = BaseModel)