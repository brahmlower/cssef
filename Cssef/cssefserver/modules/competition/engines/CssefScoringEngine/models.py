from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from cssefserver.framework.models import Base
from cssefserver.framework.models import tablePrefix

class Plugin(Model):
	__tablename__ = tablePrefix + 'plugin'
	pkid			= Column(Integer, primary_key = True)
	name			= Column(String(20))
	description		= Column(String(256))

class Service(Model):
	__tablename__ = tablePrefix + 'service'
	pkid			= Column(Integer, primary_key = True)
	competition		= Column(Integer, ForeignKey(tablePrefix + 'competition.pkid'))
	plugin			= Column(Integer, ForeignKey(tablePrefix + 'plugin.pkid'))
	name			= Column(String(20))
	description		= Column(String(256))
	manualStart		= Column(Boolean, default = True)
	datetimeStart	= Column(DateTime)
	datetimeFinish	= Column(DateTime)
	points			= Column(Integer)
	machineIp		= Column(String(15))
	machineFqdn		= Column(String(50))
	defaultPort		= Column(Integer)