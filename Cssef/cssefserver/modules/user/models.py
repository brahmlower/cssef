from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from cssefserver.framework.models import Base
from cssefserver.framework.models import tablePrefix

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