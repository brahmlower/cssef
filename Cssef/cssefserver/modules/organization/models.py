from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Integer
from cssefserver.framework.models import Base
from cssefserver.framework.models import tablePrefix

class Organization(Base):
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
