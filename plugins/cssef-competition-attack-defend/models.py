from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
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

class Competition(Base):
	__tablename__ = tablePrefix + 'competition'
	pkid				= Column(Integer, primary_key = True)
	organization		= Column(Integer, ForeignKey(tablePrefix + 'organization.pkid'))
	#scoringEngine		= relationship('ScoringEngine')
	teams				= relationship('Team')
	scores				= relationship('Score')
	injects				= relationship('Inject')
	injectResponses		= relationship('InjectResponse')
	incidents			= relationship('Incident')
	incidentResponses	= relationship('IncidentResponse')
	name				= Column(String(50))
	url					= Column(String(50))
	description			= Column(String(1000))
	datetimeDisplay		= Column(DateTime)
	datetimeStart		= Column(DateTime)
	datetimeFinish		= Column(DateTime)
	autoStart			= Column(Boolean)
	# scoringInterval = PositiveIntegerField(null = True)
	# scoringIntervalUncertainty = PositiveIntegerField(null = True)
	# scoringMethod = CharField(max_length = 20, null = True, blank = True)	# set to either CIDR or domain name
	# scoringSlaEnabled = BooleanField(default = True)
	# scoringSlaThreashold = PositiveIntegerField(null = True)
	# scoringSlaPenalty = PositiveIntegerField(null = True)
	# servicesEnabled = BooleanField(default = True)

	# These are all related specifically to the Web Interface.
	# These should be moved over to a model for configuring the
	# web interface rather than the competition
	teamsViewRankingEnabled				= Column(Boolean)
	teamsViewScoreboardEnabled			= Column(Boolean)
	teamsViewServiceStatisticsEnabled	= Column(Boolean)
	teamsViewServiceStatusEnabled		= Column(Boolean)
	teamsViewInjectsEnabled				= Column(Boolean)
	teamsViewIncidentResponseEnabled	= Column(Boolean)

class Score(Base):
	__tablename__ = tablePrefix + 'score'
	pkid		= Column(Integer, primary_key = True)
	competition	= Column(Integer, ForeignKey(tablePrefix + 'competition.pkid'))
	team		= Column(Integer, ForeignKey(tablePrefix + 'team.pkid'))
	datetime	= Column(DateTime)
	value		= Column(Integer)
	message		= Column(String(100))

class Team(Base):
	__tablename__ = tablePrefix + 'team'
	pkid				= Column(Integer, primary_key = True)
	competition			= Column(Integer, ForeignKey(tablePrefix + 'competition.pkid'))
	scores				= relationship('Score')
	last_login			= Column(DateTime)
	name				= Column(String(30))
	username			= Column(String(30))
	password			= Column(String(64))
	networkCidr			= Column(String(30))
	scoreConfigurations	= Column(String(1000))

class Inject(Base):
	__tablename__ = tablePrefix + 'inject'
	pkid					= Column(Integer, primary_key = True)
	competition				= Column(Integer, ForeignKey(tablePrefix + 'competition.pkid'))
	title					= Column(String(50))
	body					= Column(String(1000))
	responses				= relationship('InjectResponse')
	requireResponse			= Column(Boolean, default = True)
	manualDelivery			= Column(Boolean, default = False)
	datetimeDelivery		= Column(DateTime, nullable = True, default = None)
	datetimeResponseDue		= Column(DateTime, nullable = True, default = None)
	datetimeResponseClose	= Column(DateTime, nullable = True, default = None)

class InjectResponse(Base):
	__tablename__ = tablePrefix + 'injectresponse'
	pkid		= Column(Integer, primary_key = True)
	competition	= Column(Integer, ForeignKey(tablePrefix + 'competition.pkid'))
	team		= Column(Integer, ForeignKey(tablePrefix + 'team.pkid'))
	inject		= Column(Integer, ForeignKey(tablePrefix + 'inject.pkid'))
	datetime	= Column(DateTime)
	content		= Column(String(20))

class Incident(Base):
	__tablename__ = tablePrefix + 'incident'
	pkid		= Column(Integer, primary_key = True)
	competition	= Column(Integer, ForeignKey(tablePrefix + 'competition.pkid'))
	team		= Column(Integer, ForeignKey(tablePrefix + 'team.pkid'))
	datetime	= Column(DateTime)
	subject		= Column(String(100))
	content		= Column(String(1000))

class IncidentResponse(Base):
	__tablename__ = tablePrefix + 'incidentresponse'
	pkid		= Column(Integer, primary_key = True)
	competition	= Column(Integer, ForeignKey(tablePrefix + 'competition.pkid'))
	team		= Column(Integer, ForeignKey(tablePrefix + 'team.pkid'))
	incident	= Column(Integer, ForeignKey(tablePrefix + 'incident.pkid'))
	replyTo		= Column(Integer, ForeignKey(tablePrefix + 'incidentresponse.pkid'))
	replies		= relationship('IncidentResponse')
	datetime	= Column(DateTime)
	subject		= Column(String(100))
	content		= Column(String(1000))

# class ScoringEngine(Base):
# 	__tablename__ = tablePrefix + 'scoringengine'
# 	pkid		= Column(Integer, primary_key = True)
# 	name		= Column(String(256))
# 	packageName	= Column(String(256))
# 	enabled		= Column(Boolean, default = True)