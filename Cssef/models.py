from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref


Base = declarative_base()
tablePrefix = 'cssef_'

class Competition(Base):
	__tablename__ = tablePrefix + 'competition'
	pkid				= Column(Integer, primary_key = True)
	organization		= Column(Integer, ForeignKey(tablePrefix + 'organization.pkid'))
	scoringEngine		= relationship('ScoringEngine')
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
	# ^ With regard to score configuration
	# holy shitballs! Use a serialziser for this!
	# teh scoring engine will have an object to interpret this, and then when it needs to save the object
	# or load it, it will be serialized and then saved to the database. Wehnt htis is read from the database,
	# it is de-serialized!

class Score(Base):
	__tablename__ = tablePrefix + 'score'
	pkid		= Column(Integer, primary_key = True)
	competition	= Column(Integer, ForeignKey(tablePrefix + 'competition.pkid'))
	team		= Column(Integer, ForeignKey(tablePrefix + 'team.pkid'))
	datetime	= Column(DateTime)
	value		= Column(Integer)
	message		= Column(String(100))

class Inject(Base):
	__tablename__ = tablePrefix + 'inject'
	pkid					= Column(Integer, primary_key = True)
	competition				= Column(Integer, ForeignKey(tablePrefix + 'competition.pkid'))
	responses				= relationship('InjectResponse')
	requireResponse			= Column(Boolean)
	manualDelivery			= Column(Boolean)
	datetimeDelivery		= Column(DateTime)
	datetimeResponseDue		= Column(DateTime)
	datetimeResponseClose	= Column(DateTime)
	title					= Column(String(50))
	body					= Column(String(1000))

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


class User(Base):
	__tablename__ = tablePrefix + 'user'
	pkid			= Column(Integer, primary_key = True)
	organization	= Column(Integer, ForeignKey(tablePrefix + 'organization.pkid'))
	last_login		= Column(DateTime)
	name			= Column(String(20))
	username		= Column(String(20))
	password		= Column(String(64))
	description		= Column(String(256))

class ScoringEngine(Base):
	__tablename__ = tablePrefix + 'scoringengine'
	pkid		= Column(Integer, primary_key = True)
	name		= Column(String(256))
	packageName	= Column(String(256))
	disabled	= Column(Boolean)

class Organization(Base):
	__tablename__ = tablePrefix + 'organization'
	pkid			= Column(Integer, primary_key = True)
	deleteable		= Column(Boolean)
	name			= Column(String(256))
	url				= Column(String(256))
	description		= Column(String(1000))
	maxMembers		= Column(Integer)
	maxCompetitions	= Column(Integer)
	numMembers		= Column(Integer)
	numCompetitions	= Column(Integer)

class Document(Base):
	__tablename__ = tablePrefix + 'document'
	pkid				= Column(Integer, primary_key = True)
	contentType			= Column(String(64))
	fileHash			= Column(String(32))
	filePath			= Column(String(64))
	fileName			= Column(String(64))
	urlEncodedFilename	= Column(String(128))

	# def get_cleaned_content_type(self):
	# 	if not self.content_type:
	# 		return'application/force-download'
	# 	else:
	# 		return self.content_type
