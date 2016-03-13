from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from cssefserver.framework.models import Base
from cssefserver.framework.models import tablePrefix

class Organization(Base):
	"""This is a base User SQLAlchemy model.
	"""
	__tablename__ = tablePrefix + 'organization'
	pkid			= Column(Integer, primary_key = True)
	deletable		= Column(Boolean, default = True)
	canAddUsers		= Column(Boolean, default = True)
	canDeleteUsers	= Column(Boolean, default = True)
	canAddCompetitions = Column(Boolean, default = True)
	canDeleteCompetitions = Column(Boolean, default = True)
	name			= Column(String(256))
	url				= Column(String(256))
	description		= Column(String(1000))
	maxMembers		= Column(Integer)
	maxCompetitions	= Column(Integer)
	numMembers		= Column(Integer)
	numCompetitions	= Column(Integer)

class User(Base):
	"""This is a base User SQLAlchemy model.
	"""
	__tablename__ = tablePrefix + 'user'
	pkid			= Column(Integer, primary_key = True)
	organization	= Column(Integer, ForeignKey(tablePrefix + 'organization.pkid'))
	last_login		= Column(DateTime)
	name			= Column(String(20))
	username		= Column(String(20))
	password		= Column(String(64))
	description		= Column(String(256))