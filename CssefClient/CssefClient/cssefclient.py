import sys
from time import sleep
from celery import Celery

versionMajor = '0'
versionMinor = '0'
versionRelease = '1'
version = ".".join([versionMajor, versionMinor, versionRelease])

RPC_USERNAME = 'cssefd'
RPC_PASSWORD = 'cssefd-pass'
RPC_HOST = 'localhost'
AMQP_USERNAME = 'cssefd'
AMQP_PASSWORD = 'cssefd-pass'
AMQP_HOST = 'localhost'

def getConn():
	backend = "rpc://%s:%s@%s//" % (
		'cssefd',#settings.RPC_USERNAME, 
		'cssefd-pass',#settings.RPC_PASSWORD,
		'localhost')#settings.RPC_HOST)
	broker = "amqp://%s:%s@%s//" % (
		'cssefd',#settings.AMQP_USERNAME,
		'cssefd-pass',#settings.AMQP_PASSWORD,
		'localhost')#settings.AMQP_HOST) 
	return Celery('api', backend = backend, broker = broker)

class Argument(object):
	def __init__(self, displayName, name = None, keyword = False, optional = False):
		self.displayName = displayName
		if not name:
			self.name = self.displayName.lower()
		else:
			self.name = name
		self.keyword = keyword
		self.optional = optional

class Endpoint(object):
	def __init__(self, celeryName, args):
		self.apiConn = None
		self.celeryName = celeryName
		self.args = args

	def execute(self, *args, **kwargs):
		x = self.apiConn.send_task(self.celeryName, args = args, kwargs = kwargs)
		return x.get()

############################################
# Competition endpoints
############################################
class CompetitionAdd(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionAdd'
		self.args = [
			Argument('Organization', keyword = True),
			Argument('Name', keyword = True),
			Argument('URL', keyword = True, optional = True),
			Argument('Description', keyword = True, optional = True),
			Argument('Datetime Display', keyword = True, optional = True),
			Argument('Datetime Start', keyword = True, optional = True),
			Argument('Datetime Finish', keyword = True, optional = True),
			Argument('Auto-start', keyword = True, optional = True)
		]

class CompetitionDel(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionDel'
		self.args = [
			Argument('Competition', keyword = True)
		]

class CompetitionSet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionSet'
		self.args = [
			Argument('Competition', keyword = True),
			Argument('Name', keyword = True, optional = True),
			Argument('URL', keyword = True, optional = True),
			Argument('Description', keyword = True, optional = True),
			Argument('Datetime Display', keyword = True, optional = True),
			Argument('Datetime Start', keyword = True, optional = True),
			Argument('Datetime Finish', keyword = True, optional = True),
			Argument('Auto-start', keyword = True, optional = True)
		]

class CompetitionGet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionGet'
		self.args = [
			Argument('Competition', keyword = True),
			Argument('Name', optional = True),
			Argument('URL', optional = True),
			Argument('Description', optional = True),
			Argument('Datetime Display', optional = True),
			Argument('Datetime Start', optional = True),
			Argument('Datetime Finish', optional = True),
			Argument('Auto-start', optional = True)
		]

############################################
# Competition - Team endpoints
############################################
class CompetitionTeamAdd(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionTeamAdd'
		self.args = [
			Argument('Competition', keyword = True),
			Argument('Name', keyword = True),
			Argument('Username', keyword = True),
			Argument('Password', keyword = True),
			Argument('Network CIDR', keyword = True, optional = True)
		]

class CompetitionTeamDel(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionTeamDel'
		self.args = [
			Argument('Team', keyword = True)
		]


class CompetitionTeamSet (Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionTeamSet'
		self.args = [
			Argument('Name', keyword = True, optional = True),
			Argument('Username', keyword = True, optional = True),
			Argument('Password', keyword = True, optional = True),
			Argument('Network CIDR', keyword = True, optional = True)
		]

class CompetitionTeamGet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionTeamGet'
		self.args = [
			Argument('Name', optional = True),
			Argument('Username', optional = True),
			Argument('Password', optional = True),
			Argument('Network CIDR', optional = True)
		]

############################################
# Competition - Score endpoints
############################################
class CompetitionScoreAdd(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionScoreAdd'
		self.args = [
			Argument('Competition', keyword = True),
			Argument('Team', keyword = True),
			Argument('Datetime', keyword = True),
			Argument('Value', keyword = True),
			Argument('Message', keyword = True, optional = True)
		]

class CompetitionScoreDel(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionScoreDel'
		self.args = [
			Argument('Score', keyword = True)
		]

class CompetitionScoreSet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionScoreSet'
		self.args = [
			Argument('Datetime', keyword = True, optional = True),
			Argument('Value', keyword = True, optional = True),
			Argument('Message', keyword = True, optional =True)
		]

class CompetitionScoreGet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionScoreGet'
		self.args = [
			Argument('Datetime', optional = True),
			Argument('Value', optional = True),
			Argument('Message', optional = True)
		]

############################################
# Competition - Inject endpoints
############################################
class CompetitionInjectAdd(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionInjectAdd'
		self.args = [
			Argument('Competition', keyword = True),
			Argument('Require Response', keyword = True),
			Argument('Manual Delivery', keyword = True),
			Argument('Datetime Delivery', keyword = True),
			Argument('Datetime Response Due', keyword = True),
			Argument('Datetime Response Close', keyword = True),
			Argument('Title', keyword = True),
			Argument('Body', keyword = True)
		]

class CompetitionInjectDel(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionInjectDel'
		self.args = [
			Argument('Inject', keyword = True)
		]

class CompetitionInjectSet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionInjectSet'
		self.args = [
			Argument('Require Response', keyword = True, optional = True),
			Argument('Manual Delivery', keyword = True, optional = True),
			Argument('Datetime Delivery', keyword = True, optional = True),
			Argument('Datetime Response Due', keyword = True, optional = True),
			Argument('Datetime Response Close', keyword = True, optional = True),
			Argument('Title', keyword = True, optional = True),
			Argument('Body', keyword = True, optional = True)
		]

class CompetitionInjectGet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionInjectGet'
		self.args = [
			Argument('Require Response', optional = True),
			Argument('Manual Delivery', optional = True),
			Argument('Datetime Delivery', optional = True),
			Argument('Datetime Response Due', optional = True),
			Argument('Datetime Response Close', optional = True),
			Argument('Title', optional = True),
			Argument('Body', optional = True)
		]

############################################
# Competition - Inject Response endpoints
############################################
class CompetitionInjectResponseAdd(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionInjectResponseAdd'
		self.args = [
			Argument('Competition', keyword = True),
			Argument('Team', keyword = True),
			Argument('Inject', keyword = True),
			Argument('Datetime', keyword = True),
			Argument('Content', keyword = True)
		]

class CompetitionInjectResponseDel(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionInjectResponseDel'
		self.args = [
			Argument('Inject Response', keyword = True)
		]

class CompetitionInjectResponseSet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionInjectResponseSet'
		self.args = [
			Argument('Competition', keyword = True, optional = True),
			Argument('Team', keyword = True, optional = True),
			Argument('Inject', keyword = True, optional = True),
			Argument('Datetime', keyword = True, optional = True),
			Argument('Content', keyword = True, optional = True)
		]

class CompetitionInjectResponseGet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionInjectResponseGet'
		self.args = [
			Argument('Competition', optional = True),
			Argument('Team', optional = True),
			Argument('Inject', optional = True),
			Argument('Datetime', optional = True),
			Argument('Content', optional = True)
		]

############################################
# Competition - Incident endpoints
############################################
class CompetitionIncidentAdd(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionIncidentAdd'
		self.args = [
			Argument('Competition', keyword = True),
			Argument('Team', keyword = True),
			Argument('Datetime', keyword = True),
			Argument('Subject', keyword = True),
			Argument('Content', keyword = True)
		]

class CompetitionIncidentDel(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionIncidentDel'
		self.args = [
			Argument('Incident', keyword = True)
		]

class CompetitionIncidentSet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionIncidentSet'
		self.args = [
			Argument('Competition', keyword = True, optional = True),
			Argument('Team', keyword = True, optional = True),
			Argument('Datetime', keyword = True, optional = True),
			Argument('Subject', keyword = True, optional = True),
			Argument('Content', keyword = True, optional = True)
		]

class CompetitionIncidentGet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionIncidentSet'
		self.args = [
			Argument('Competition', optional = True),
			Argument('Team', optional = True),
			Argument('Datetime', optional = True),
			Argument('Subject', optional = True),
			Argument('Content', optional = True)
		]

############################################
# Competition - Incident Response endpoints
############################################
class CompetitionIncidentResponseAdd(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionIncidentResponseAdd'
		self.args = [
			Argument('Competition', keyword = True),
			Argument('Team', keyword = True),
			Argument('Incident', keyword = True),
			Argument('Reply To', keyword = True),
			Argument('Datetime', keyword = True),
			Argument('Subject', keyword = True),
			Argument('Content', keyword = True)
		]

class CompetitionIncidentResponseDel(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionIncidentResponseDel'
		self.args = [
			Argument('Incident Response', keyword = True)
		]

class CompetitionIncidentResponseSet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionIncidentResponseSet'
		self.args = [
			Argument('Competition', keyword = True, optional = True),
			Argument('Team', keyword = True, optional = True),
			Argument('Incident', keyword = True, optional = True),
			Argument('Reply To', keyword = True, optional = True),
			Argument('Datetime', keyword = True, optional = True),
			Argument('Subject', keyword = True, optional = True),
			Argument('Content', keyword = True, optional = True)
		]

class CompetitionIncidentResponseGet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'competitionIncidentResponseGet'
		self.args = [
			Argument('Competition', optional = True),
			Argument('Team', optional = True),
			Argument('Incident', optional = True),
			Argument('Reply To', optional = True),
			Argument('Datetime', optional = True),
			Argument('Subject', optional = True),
			Argument('Content', optional = True)
		]

############################################
# Organization endpoints
############################################
class OrganizationGet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'organizationGet'
		self.args = [
			Argument('Name', optional = True),
			Argument('URL', optional = True),
			Argument('Description', optional = True),
			Argument('Max Members', optional = True),
			Argument('Max Competitions', optional = True)
		]

class OrganizationSet(Endpoint):
	def __init__ (self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'organizationSet'
		args = [
			Argument('Name', keyword = True, optional = True),
			Argument('URL', keyword = True, optional = True),
			Argument('Description', keyword = True, optional = True),
			Argument('Max Members', keyword = True, optional = True),
			Argument('Max Competitions', keyword = True, optional = True)
		]

class OrganizationAdd(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'organizationAdd'
		self.args = [
			Argument('Name', keyword = True),
			Argument('URL', keyword = True),
			Argument('Description', keyword = True),
			Argument('Max Members', keyword = True, optional = True),
			Argument('Max Competitions', keyword = True, optional = True)
		]

class OrganizationDel(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'organizationDel'
		args = [
			Argument('Organization', keyword = True)
		]

############################################
# User endpoints
############################################
class UserAdd(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'userAdd'
		self.args = [
			Argument('Organization', keyword = True),
			Argument('Name', keyword = True),
			Argument('Username', keyword = True),
			Argument('Password', keyword = True),
			Argument('Description', keyword = True, optional = True)
		]

class UserDel(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'userDel'
		self.args = [
			Argument('User', keyword = True)
		]

class UserSet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'userSet'
		self.args = [
			Argument('Organization', keyword = True, optional = True),
			Argument('Name', keyword = True, optional = True),
			Argument('Username', keyword = True, optional = True),
			Argument('Password', keyword = True, optional = True),
			Argument('Description', keyword = True, optional = True)
		]

class UserGet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'userGet'
		self.args = [
			Argument('Organization', optional = True),
			Argument('Name', optional = True),
			Argument('Username', optional = True),
			Argument('Password', optional = True),
			Argument('Description', optional = True)
		]

############################################
# Document endpoints
############################################
class DocumentAdd(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'documentAdd'
		self.args = []

class DocumentDel(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'documentDel'
		self.args = []

class DocumentSet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'documentSet'
		self.args = []

class DocumentGet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'documentGet'
		self.args = []

############################################
# Scoring Engine endpoints
############################################
class ScoringEngineAdd(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'scoringEngineAdd'
		self.args = [
			Argument("Name", keyword = True, optional = False),
			Argument("Package Name", keyword = True, optional = False),
		]

class ScoringEngineDel(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'scoringEngineDel'
		self.args = [
			Argument("Scoring Engine", keyword = True, optional = False)
		]

class ScoringEngineSet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'scoringEngineSet'
		self.args = [
			Argument('Name', keyword = True, optional = True),
			Argument('Package Name', keyword = True, optional = True),
			Argument('Disabled', keyword = True, optional = True)
		]

class ScoringEngineGet(Endpoint):
	def __init__(self, apiConn = None):
		self.apiConn = apiConn
		self.celeryName = 'scoringEngineGet'
		args = [
			Argument('Name', optional = True),
			Argument('Package Name', optional = True),
			Argument('Disabled', optional = True)
		]