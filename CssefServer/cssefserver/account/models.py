from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from cssefserver.modelbase import Base
from cssefserver.modelutils import getForeignKey

class Organization(Base):
	"""This is a base User SQLAlchemy model.
	"""
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
	organization	= Column(Integer, getForeignKey(Organization))
	last_login		= Column(DateTime)
	name			= Column(String(20))
	username		= Column(String(20))
	password		= Column(String(64))
	description		= Column(String(256))