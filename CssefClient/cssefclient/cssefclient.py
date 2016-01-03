import sys
from time import sleep
from celery import Celery
import ConfigParser

versionMajor = '0'
versionMinor = '0'
versionPatch = '2'
version = ".".join([versionMajor, versionMinor, versionPatch])

def getConn(config):
	return Celery(
		'api',
		backend = config.rpcUrl,
		broker = config.amqpUrl)

class Configuration(object):
	def __init__(self, configFilePath):
		self.rawConfig = ConfigParser.ConfigParser()
		self.rawConfig.read(configFilePath)

	@property
	def amqpUrl(self):
		username = self.rawConfig.get('celery', 'amqp_username')
		password = self.rawConfig.get('celery', 'amqp_password')
		host = self.rawConfig.get('celery', 'amqp_host')
		return 'amqp://%s:%s@%s//' % (username, password, host)

	@property
	def rpcUrl(self):
		username = self.rawConfig.get('celery', 'rpc_username')
		password = self.rawConfig.get('celery', 'rpc_password')
		host = self.rawConfig.get('celery', 'rpc_host')
		return 'rpc://%s:%s@%s//' % (username, password, host)

class Argument(object):
	def __init__(self, displayName, name = None, keyword = False, optional = False):
		self.displayName = displayName
		if not name:
			self.name = self.displayName.lower()
		else:
			self.name = name
		self.keyword = keyword
		self.optional = optional

	def helpFormat(self, *args, **kwargs):
		return '--%s' % self.name

class Endpoint(object):
	def __init__(self, name):
		self.name = name.lower()
		self.args = []

	def help(self, *args, **kwargs):
		helpRows = []
		helpRows.append('Endpoint: %s' % self.name)
		for i in self.args:
			helpRows.append(i.helpFormat(*args, **kwargs))
		return helpRows

class CeleryEndpoint(Endpoint):
	def __init__(self, celeryName, args):
		super(CeleryEndpoint, self).__init__(self, celeryName)
		self.apiConn = None
		self.celeryName = celeryName
		self.args = args

	def execute(self, *args, **kwargs):
		task = self.apiConn.send_task(
			self.celeryName,
			args = args,
			kwargs = kwargs)
		return task.get()


############################################
# Competition endpoints
############################################
class CompetitionAdd(CeleryEndpoint):
	def __init__(self, apiConn):
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

class CompetitionDel(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'competitionDel'
		self.args = [
			Argument('Competition', keyword = True)
		]

class CompetitionSet(CeleryEndpoint):
	def __init__(self, apiConn):
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

class CompetitionGet(CeleryEndpoint):
	def __init__(self, apiConn):
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
class CompetitionTeamAdd(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'competitionTeamAdd'
		self.args = [
			Argument('Competition', keyword = True),
			Argument('Name', keyword = True),
			Argument('Username', keyword = True),
			Argument('Password', keyword = True),
			Argument('Network CIDR', keyword = True, optional = True)
		]

class CompetitionTeamDel(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'competitionTeamDel'
		self.args = [
			Argument('Team', keyword = True)
		]


class CompetitionTeamSet(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'competitionTeamSet'
		self.args = [
			Argument('Name', keyword = True, optional = True),
			Argument('Username', keyword = True, optional = True),
			Argument('Password', keyword = True, optional = True),
			Argument('Network CIDR', keyword = True, optional = True)
		]

class CompetitionTeamGet(CeleryEndpoint):
	def __init__(self, apiConn):
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
class CompetitionScoreAdd(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'competitionScoreAdd'
		self.args = [
			Argument('Competition', keyword = True),
			Argument('Team', keyword = True),
			Argument('Datetime', keyword = True),
			Argument('Value', keyword = True),
			Argument('Message', keyword = True, optional = True)
		]

class CompetitionScoreDel(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'competitionScoreDel'
		self.args = [
			Argument('Score', keyword = True)
		]

class CompetitionScoreSet(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'competitionScoreSet'
		self.args = [
			Argument('Datetime', keyword = True, optional = True),
			Argument('Value', keyword = True, optional = True),
			Argument('Message', keyword = True, optional =True)
		]

class CompetitionScoreGet(CeleryEndpoint):
	def __init__(self, apiConn):
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
class CompetitionInjectAdd(CeleryEndpoint):
	def __init__(self, apiConn):
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

class CompetitionInjectDel(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'competitionInjectDel'
		self.args = [
			Argument('Inject', keyword = True)
		]

class CompetitionInjectSet(CeleryEndpoint):
	def __init__(self, apiConn):
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

class CompetitionInjectGet(CeleryEndpoint):
	def __init__(self, apiConn):
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
class CompetitionInjectResponseAdd(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'competitionInjectResponseAdd'
		self.args = [
			Argument('Competition', keyword = True),
			Argument('Team', keyword = True),
			Argument('Inject', keyword = True),
			Argument('Datetime', keyword = True),
			Argument('Content', keyword = True)
		]

class CompetitionInjectResponseDel(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'competitionInjectResponseDel'
		self.args = [
			Argument('Inject Response', keyword = True)
		]

class CompetitionInjectResponseSet(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'competitionInjectResponseSet'
		self.args = [
			Argument('Competition', keyword = True, optional = True),
			Argument('Team', keyword = True, optional = True),
			Argument('Inject', keyword = True, optional = True),
			Argument('Datetime', keyword = True, optional = True),
			Argument('Content', keyword = True, optional = True)
		]

class CompetitionInjectResponseGet(CeleryEndpoint):
	def __init__(self, apiConn):
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
class CompetitionIncidentAdd(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'competitionIncidentAdd'
		self.args = [
			Argument('Competition', keyword = True),
			Argument('Team', keyword = True),
			Argument('Datetime', keyword = True),
			Argument('Subject', keyword = True),
			Argument('Content', keyword = True)
		]

class CompetitionIncidentDel(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'competitionIncidentDel'
		self.args = [
			Argument('Incident', keyword = True)
		]

class CompetitionIncidentSet(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'competitionIncidentSet'
		self.args = [
			Argument('Competition', keyword = True, optional = True),
			Argument('Team', keyword = True, optional = True),
			Argument('Datetime', keyword = True, optional = True),
			Argument('Subject', keyword = True, optional = True),
			Argument('Content', keyword = True, optional = True)
		]

class CompetitionIncidentGet(CeleryEndpoint):
	def __init__(self, apiConn):
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
class CompetitionIncidentResponseAdd(CeleryEndpoint):
	def __init__(self, apiConn):
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

class CompetitionIncidentResponseDel(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'competitionIncidentResponseDel'
		self.args = [
			Argument('Incident Response', keyword = True)
		]

class CompetitionIncidentResponseSet(CeleryEndpoint):
	def __init__(self, apiConn):
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

class CompetitionIncidentResponseGet(CeleryEndpoint):
	def __init__(self, apiConn):
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
class OrganizationGet(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'organizationGet'
		self.args = [
			Argument('Name', optional = True),
			Argument('URL', optional = True),
			Argument('Description', optional = True),
			Argument('Max Members', optional = True),
			Argument('Max Competitions', optional = True)
		]

class OrganizationSet(CeleryEndpoint):
	def __init__ (self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'organizationSet'
		args = [
			Argument('Name', keyword = True, optional = True),
			Argument('URL', keyword = True, optional = True),
			Argument('Description', keyword = True, optional = True),
			Argument('Max Members', keyword = True, optional = True),
			Argument('Max Competitions', keyword = True, optional = True)
		]

class OrganizationAdd(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'organizationAdd'
		self.args = [
			Argument('Name', keyword = True),
			Argument('URL', keyword = True),
			Argument('Description', keyword = True),
			Argument('Max Members', keyword = True, optional = True),
			Argument('Max Competitions', keyword = True, optional = True)
		]

class OrganizationDel(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'organizationDel'
		args = [
			Argument('Organization', keyword = True)
		]

############################################
# User endpoints
############################################
class UserAdd(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'userAdd'
		self.args = [
			Argument('Organization', keyword = True),
			Argument('Name', keyword = True),
			Argument('Username', keyword = True),
			Argument('Password', keyword = True),
			Argument('Description', keyword = True, optional = True)
		]

class UserDel(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'userDel'
		self.args = [
			Argument('User', keyword = True)
		]

class UserSet(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'userSet'
		self.args = [
			Argument('Organization', keyword = True, optional = True),
			Argument('Name', keyword = True, optional = True),
			Argument('Username', keyword = True, optional = True),
			Argument('Password', keyword = True, optional = True),
			Argument('Description', keyword = True, optional = True)
		]

class UserGet(CeleryEndpoint):
	def __init__(self, apiConn):
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
class DocumentAdd(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'documentAdd'
		self.args = []

class DocumentDel(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'documentDel'
		self.args = []

class DocumentSet(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'documentSet'
		self.args = []

class DocumentGet(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'documentGet'
		self.args = []

############################################
# Scoring Engine endpoints
############################################
class ScoringEngineAdd(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'scoringEngineAdd'
		self.args = [
			Argument("Name", keyword = True, optional = False),
			Argument("Package Name", keyword = True, optional = False),
		]

class ScoringEngineDel(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'scoringEngineDel'
		self.args = [
			Argument("Scoring Engine", keyword = True, optional = False)
		]

class ScoringEngineSet(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'scoringEngineSet'
		self.args = [
			Argument('Name', keyword = True, optional = True),
			Argument('Package Name', keyword = True, optional = True),
			Argument('Disabled', keyword = True, optional = True)
		]

class ScoringEngineGet(CeleryEndpoint):
	def __init__(self, apiConn):
		self.apiConn = apiConn
		self.celeryName = 'scoringEngineGet'
		args = [
			Argument('Name', optional = True),
			Argument('Package Name', optional = True),
			Argument('Disabled', optional = True)
		]