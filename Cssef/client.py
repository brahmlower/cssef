#!/usr/bin/python
# ./client.py competition-add organization=1 name="Competition One" url="comp_one" autostart=True
#
from celery import Celery
import sys
from time import sleep

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
	def __init__(self, path, args):
		self.conn = None
		self.path = path
		self.args = None

	def __call__(self, *args, **kwargs):
		x = self.conn.send_task(self.path, args = args, kwargs = kwargs)
		while not x.ready():
			# this will loop VERY ungracefully...
			pass
		return x.result

	def usage(self):
		for i in self.args:
			print i.name, i.keyword, i.optional

class CssefClient(object):
	versionMajor = '0'
	versionMinor = '0'
	versionRelease = '1'
	version = ".".join([versionMajor, versionMinor, versionRelease])

	competitionAdd = Endpoint(
		'competitionAdd',
		args = (
			Argument('Organization', keyword = True),
			Argument('Name', keyword = True),
			Argument('URL', keyword = True, optional = True),
			Argument('Description', keyword = True, optional = True),
			Argument('Datetime Display', keyword = True, optional = True),
			Argument('Datetime Start', keyword = True, optional = True),
			Argument('Datetime Finish', keyword = True, optional = True),
			Argument('Auto-start', keyword = True, optional = True),
		)
	)
	competition_del = Endpoint(
		'competitionDel',
		args = (
			Argument('Competition', keyword = True),
		)
	)
	competition_set = Endpoint(
		'competitionSet',
		args = (
			Argument('Competition', keyword = True),
			Argument('Name', keyword = True, optional = True),
			Argument('URL', keyword = True, optional = True),
			Argument('Description', keyword = True, optional = True),
			Argument('Datetime Display', keyword = True, optional = True),
			Argument('Datetime Start', keyword = True, optional = True),
			Argument('Datetime Finish', keyword = True, optional = True),
			Argument('Auto-start', keyword = True, optional = True),
		)
	)
	competition_get = Endpoint(
		'competitionGet',
		args = (
			Argument('Competition', keyword = True),
			Argument('Name', optional = True),
			Argument('URL', optional = True),
			Argument('Description', optional = True),
			Argument('Datetime Display', optional = True),
			Argument('Datetime Start', optional = True),
			Argument('Datetime Finish', optional = True),
			Argument('Auto-start', optional = True),
		)
	)

	competition_TeamAdd = Endpoint(
		'competitionTeamAdd',
		args = (
			Argument('Competition', keyword = True),
			Argument('Name', keyword = True),
			Argument('Username', keyword = True),
			Argument('Password', keyword = True),
			Argument('Network CIDR', keyword = True, optional = True)
		)
	)
	competition_TeamDel = Endpoint(
		'competitionTeamDel',
		args = (
			Argument('Team', keyword = True),
		)
	)
	competition_TeamSet = Endpoint(
		'competitionTeamSet',
		args = (
			Argument('Name', keyword = True, optional = True),
			Argument('Username', keyword = True, optional = True),
			Argument('Password', keyword = True, optional = True),
			Argument('Network CIDR', keyword = True, optional = True)
		)
	)
	competition_TeamGet = Endpoint(
		'competitionTeamGet',
		args = (
			Argument('Name', optional = True),
			Argument('Username', optional = True),
			Argument('Password', optional = True),
			Argument('Network CIDR', optional = True)
		)
	)

	competition_ScoreAdd = Endpoint(
		'competitionScoreAdd',
		args = (
			Argument('Competition', keyword = True),
			Argument('Team', keyword = True),
			Argument('Datetime', keyword = True),
			Argument('Value', keyword = True),
			Argument('Message', keyword = True, optional = True)
		)
	)
	competition_ScoreDel = Endpoint(
		'competitionScoreDel',
		args = (
			Argument('Score', keyword = True)
		)
	)
	competition_ScoreSet = Endpoint(
		'competitionScoreSet',
		args = (
			Argument('Datetime', keyword = True, optional = True),
			Argument('Value', keyword = True, optional = True),
			Argument('Message', keyword = True, optional =True)
		)
	)
	competition_ScoreGet = Endpoint(
		'competitionScoreGet',
		args = (
			Argument('Datetime', optional = True),
			Argument('Value', optional = True),
			Argument('Message', optional = True)
		)
	)

	competition_InjectAdd = Endpoint(
		'competitionInjectAdd',
		args = (
			Argument('Competition', keyword = True),
			Argument('Require Response', keyword = True),
			Argument('Manual Delivery', keyword = True),
			Argument('Datetime Delivery', keyword = True),
			Argument('Datetime Response Due', keyword = True),
			Argument('Datetime Response Close', keyword = True),
			Argument('Title', keyword = True),
			Argument('Body', keyword = True)
		)
	)
	competition_InjectDel = Endpoint(
		'competitionInjectDel',
		args = (
			Argument('Inject', keyword = True)
		)
	)
	competition_InjectSet = Endpoint(
		'competitionInjectSet',
		args = (
			Argument('Require Response', keyword = True, optional = True),
			Argument('Manual Delivery', keyword = True, optional = True),
			Argument('Datetime Delivery', keyword = True, optional = True),
			Argument('Datetime Response Due', keyword = True, optional = True),
			Argument('Datetime Response Close', keyword = True, optional = True),
			Argument('Title', keyword = True, optional = True),
			Argument('Body', keyword = True, optional = True)
		)
	)
	competition_InjectGet = Endpoint(
		'competitionInjectGet',
		args = (
			Argument('Require Response', optional = True),
			Argument('Manual Delivery', optional = True),
			Argument('Datetime Delivery', optional = True),
			Argument('Datetime Response Due', optional = True),
			Argument('Datetime Response Close', optional = True),
			Argument('Title', optional = True),
			Argument('Body', optional = True)
		)
	)

	competition_InjectResponseAdd = Endpoint(
		'competitionInjectResponseAdd',
		args = (
			Argument('Competition', keyword = True),
			Argument('Team', keyword = True),
			Argument('Inject', keyword = True),
			Argument('Datetime', keyword = True),
			Argument('Content', keyword = True)
		)
	)
	competition_InjectResponseDel = Endpoint(
		'competitionInjectResponseDel',
		args = (
			Argument('Inject Response', keyword = True)
		)
	)
	competition_InjectResponseSet = Endpoint(
		'competitionInjectResponseSet',
		args = (
			Argument('Competition', keyword = True, optional = True),
			Argument('Team', keyword = True, optional = True),
			Argument('Inject', keyword = True, optional = True),
			Argument('Datetime', keyword = True, optional = True),
			Argument('Content', keyword = True, optional = True)
		)
	)
	competition_InjectResponseGet = Endpoint(
		'competitionInjectResponseGet',
		args = (
			Argument('Competition', optional = True),
			Argument('Team', optional = True),
			Argument('Inject', optional = True),
			Argument('Datetime', optional = True),
			Argument('Content', optional = True)
		)
	)

	competition_IncidentAdd = Endpoint(
		'competitionIncidentAdd',
		args = (
			Argument('Competition', keyword = True),
			Argument('Team', keyword = True),
			Argument('Datetime', keyword = True),
			Argument('Subject', keyword = True),
			Argument('Content', keyword = True),
		)
	)
	competition_IncidentDel = Endpoint(
		'competitionIncidentDel',
		args = (
			Argument('Incident', keyword = True)
		)
	)
	competition_IncidentSet = Endpoint(
		'competitionIncidentSet',
		args = (
			Argument('Competition', keyword = True, optional = True),
			Argument('Team', keyword = True, optional = True),
			Argument('Datetime', keyword = True, optional = True),
			Argument('Subject', keyword = True, optional = True),
			Argument('Content', keyword = True, optional = True),
		)
	)
	competition_IncidentGet = Endpoint(
		'competitionIncidentSet',
		args = (
			Argument('Competition', optional = True),
			Argument('Team', optional = True),
			Argument('Datetime', optional = True),
			Argument('Subject', optional = True),
			Argument('Content', optional = True)
		)
	)

	competition_IncidentResponseAdd = Endpoint(
		'competitionIncidentResponseAdd',
		args = (
			Argument('Competition', keyword = True),
			Argument('Team', keyword = True),
			Argument('Incident', keyword = True),
			Argument('Reply To', keyword = True),
			Argument('Datetime', keyword = True),
			Argument('Subject', keyword = True),
			Argument('Content', keyword = True)
		)
	)
	competition_IncidentResponseDel = Endpoint(
		'competitionIncidentResponseDel',
		args = (
			Argument('Incident Response', keyword = True)
		)
	)
	competition_IncidentResponseSet = Endpoint(
		'competitionIncidentResponseSet',
		args = (
			Argument('Competition', keyword = True, optional = True),
			Argument('Team', keyword = True, optional = True),
			Argument('Incident', keyword = True, optional = True),
			Argument('Reply To', keyword = True, optional = True),
			Argument('Datetime', keyword = True, optional = True),
			Argument('Subject', keyword = True, optional = True),
			Argument('Content', keyword = True, optional = True)
		)
	)
	competition_IncidentResponseGet = Endpoint(
		'competitionIncidentResponseGet',
		args = (
			Argument('Competition', optional = True),
			Argument('Team', optional = True),
			Argument('Incident', optional = True),
			Argument('Reply To', optional = True),
			Argument('Datetime', optional = True),
			Argument('Subject', optional = True),
			Argument('Content', optional = True)
		)
	)

	organization_Add = Endpoint(
		'organizationAdd',
		args = (
			Argument('Name', keyword = True),
			Argument('URL', keyword = True),
			Argument('Description', keyword = True),
			Argument('Max Members', keyword = True, optional = True),
			Argument('Max Competitions', keyword = True, optional = True)
		)
	)
	organization_Del = Endpoint(
		'organizationDel',
		args = (
			Argument('Organization', keyword = True)
		)
	)
	organization_Set = Endpoint(
		'organizationSet',
		args = (
			Argument('Name', keyword = True, optional = True),
			Argument('URL', keyword = True, optional = True),
			Argument('Description', keyword = True, optional = True),
			Argument('Max Members', keyword = True, optional = True),
			Argument('Max Competitions', keyword = True, optional = True)
		)
	)
	organization_Get = Endpoint(
		'organizationGet',
		args = (
			Argument('Name', optional = True),
			Argument('URL', optional = True),
			Argument('Description', optional = True),
			Argument('Max Members', optional = True),
			Argument('Max Competitions', optional = True)
		)
	)

	user_Add = Endpoint(
		'userAdd',
		args = (
			Argument('Organization', keyword = True),
			Argument('Name', keyword = True),
			Argument('Username', keyword = True),
			Argument('Password', keyword = True),
			Argument('Description', keyword = True, optional = True)
		)
	)
	user_Del = Endpoint(
		'userDel',
		args = (
			Argument('User', keyword = True),
		)
	)
	user_Set = Endpoint(
		'userSet',
		args = (
			Argument('Organization', keyword = True, optional = True),
			Argument('Name', keyword = True, optional = True),
			Argument('Username', keyword = True, optional = True),
			Argument('Password', keyword = True, optional = True),
			Argument('Description', keyword = True, optional = True)
		)
	)
	user_Get = Endpoint(
		'userGet',
		args = (
			Argument('Organization', optional = True),
			Argument('Name', optional = True),
			Argument('Username', optional = True),
			Argument('Password', optional = True),
			Argument('Description', optional = True)
		)
	)

	document_Add = Endpoint(
		'documentAdd',
		args = ())
	document_Del = Endpoint(
		'documentDel',
		args = ())
	document_Set = Endpoint(
		'documentSet',
		args = ())
	document_Get = Endpoint(
		'documentGet',
		args = ())

	scoringEngine_Add = Endpoint(
		'scoringEngineAdd',
		args = (
			Argument("Name", keyword = True, optional = False),
			Argument("Package Name", keyword = True, optional = False),
		)
	)
	scoringEngine_Del = Endpoint(
		'scoringEngineDel',
		args = (
			Argument("Scoring Engine", keyword = True, optional = False)
		)
	)
	scoringEngine_Set = Endpoint(
		'scoringEngineSet',
		args = (
			Argument('Name', keyword = True, optional = True),
			Argument('Package Name', keyword = True, optional = True),
			Argument('Disabled', keyword = True, optional = True)
		)
	)
	scoringEngine_Get = Endpoint(
		'scoringEngineGet',
		args = (
			Argument('Name', optional = True),
			Argument('Package Name', optional = True),
			Argument('Disabled', optional = True)
		)
	)

def help():
	for i in CssefClient.__dict__.keys():
		value = getattr(CssefClient, i)
		try:
			print value
			print value.__name__
			if value.__name__ == "Endpoint":
				print i.replace('-','_')
		except:
			pass
	sys.exit()

def getConn():
	rpcUsername = "butts"
	rpcPassword = "butts"
	rpcHost = "localhost"
	amqpUsername = "butts"
	amqpPassword = "butts"
	amqpHost = "localhost"
	conn = Celery(
		'api',
		backend = "rpc://%s:%s@%s//" % (rpcUsername, rpcPassword, rpcHost),
		broker = "amqp://%s:%s@%s//" % (amqpUsername, amqpPassword, amqpHost)
	)
	return conn

if __name__ == "__main__":
	commands = {
		"competition-team-add": CssefClient.competition_TeamAdd,
		"competition-team-del": CssefClient.competition_TeamDel,
		"competition-team-set": CssefClient.competition_TeamSet,
		"competition-team-get": CssefClient.competition_TeamGet,
		"competition-score-add": CssefClient.competition_ScoreAdd,
		"competition-score-del": CssefClient.competition_ScoreDel,
		"competition-score-set": CssefClient.competition_ScoreSet,
		"competition-score-get": CssefClient.competition_ScoreGet,
		"competition-inject-add": CssefClient.competition_InjectAdd,
		"competition-inject-del": CssefClient.competition_InjectDel,
		"competition-inject-set": CssefClient.competition_InjectSet,
		"competition-inject-get": CssefClient.competition_InjectGet,
		"competition-injectresponse-add": CssefClient.competition_InjectResponseAdd,
		"competition-injectresponse-del": CssefClient.competition_InjectResponseDel,
		"competition-injectresponse-set": CssefClient.competition_InjectResponseSet,
		"competition-injectresponse-get": CssefClient.competition_InjectResponseGet,
		"competition-incident-add": CssefClient.competition_IncidentAdd,
		"competition-incident-del": CssefClient.competition_IncidentDel,
		"competition-incident-set": CssefClient.competition_IncidentSet,
		"competition-incident-get": CssefClient.competition_IncidentGet,
		"competition-incidentresponse-add": CssefClient.competition_IncidentResponseAdd,
		"competition-incidentresponse-del": CssefClient.competition_IncidentResponseDel,
		"competition-incidentresponse-set": CssefClient.competition_IncidentResponseSet,
		"competition-incidentresponse-get": CssefClient.competition_IncidentResponseGet,
		"organization-add": CssefClient.organization_Add,
		"organization-del": CssefClient.organization_Del,
		"organization-set": CssefClient.organization_Set,
		"organization-get": CssefClient.organization_Get,
		"user-add": CssefClient.user_Add,
		"user-del": CssefClient.user_Del,
		"user-set": CssefClient.user_Set,
		"user-get": CssefClient.user_Get,
		"document-add": CssefClient.document_Add,
		"document-del": CssefClient.document_Del,
		"document-set": CssefClient.document_Set,
		"document-get": CssefClient.document_Get,
		"scoringengine-add": CssefClient.scoringEngine_Add,
		"scoringengine-del": CssefClient.scoringEngine_Del,
		"scoringengine-set": CssefClient.scoringEngine_Set,
		"scoringengine-get": CssefClient.scoringEngine_Get,
	}

	if len(sys.argv) == 1:
		help()
	commandStr = sys.argv[1]
	try:
		command = commands[commandStr]
	except AttributeError:
		sys.exit("No such option: %s" % commandStr)
	kwDict = {}
	for i in sys.argv[2:]:
		key = i[:i.index('=')]
		value = i[i.index('=')+1:]
		kwDict[key] = value
	command.conn = getConn()
	output = command(**kwDict)
	print output
	for i in output:
		print i['name']