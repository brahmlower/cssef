#!/usr/local/bin/python
# ./client.py competition-add organization=1 name="Competition One" url="comp_one" autostart=True
#
from celery import Celery
import sys

class Argument:
	def __init__(self, displayName, name = None, keyword = False, optional = False):
		self.displayName = displayName
		if not name:
			self.name = self.displayName.lower()
		else:
			self.name = name
		self.keyword = keyword
		self.optional = optional

class Endpoint:
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

class CssefClient:
	versionMajor = '0'
	versionMinor = '0'
	versionRelease = '1'
	version = ".".join([versionMajor, versionMinor, versionRelease])

	competition_add = Endpoint(
		'api.competitionAdd',
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
		'api.competitionDel',
		args = (
			Argument('Competition', keyword = True),
		)
	)
	competition_set = Endpoint(
		'api.competitionSet',
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
		'api.competitionGet',
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
		'api.competitionTeamAdd',
		args = (
			Argument('Competition', keyword = True),
			Argument('Name', keyword = True),
			Argument('Username', keyword = True),
			Argument('Password', keyword = True),
			Argument('Network CIDR', keyword = True, optional = True)
		)
	)
	competition_TeamDel = Endpoint(
		'api.competitionTeamDel',
		args = (
			Argument('Team', keyword = True),
		)
	)
	competition_TeamSet = Endpoint(
		'api.competitionTeamSet',
		args = (
			Argument('Name', keyword = True, optional = True),
			Argument('Username', keyword = True, optional = True),
			Argument('Password', keyword = True, optional = True),
			Argument('Network CIDR', keyword = True, optional = True)
		)
	)
	competition_TeamGet = Endpoint(
		'api.competitionTeamGet',
		args = (
			Argument('Name', optional = True),
			Argument('Username', optional = True),
			Argument('Password', optional = True),
			Argument('Network CIDR', optional = True)
		)
	)

	competition_ScoreAdd = Endpoint(
		'api.competitionScoreAdd',
		args = (
			Argument('Competition', keyword = True),
			Argument('Team', keyword = True),
			Argument('Datetime', keyword = True),
			Argument('Value', keyword = True),
			Argument('Message', keyword = True, optional = True)
		)
	)
	competition_ScoreDel = Endpoint(
		'api.competitionScoreDel',
		args = (
			Argument('Score', keyword = True)
		)
	)
	competition_ScoreSet = Endpoint(
		'api.competitionScoreSet',
		args = (
			Argument('Datetime', keyword = True, optional = True),
			Argument('Value', keyword = True, optional = True),
			Argument('Message', keyword = True, optional =True)
		)
	)
	competition_ScoreGet = Endpoint(
		'api.competitionScoreGet',
		args = (
			Argument('Datetime', optional = True),
			Argument('Value', optional = True),
			Argument('Message', optional = True)
		)
	)

	competition_InjectAdd = Endpoint(
		'api.competitionInjectAdd',
		args = (
			Argument('Competition', keyword = True),
			Argument('Require Response', keyword = True),
			Argument('Manuel Delivery', keyword = True),
			Argument('Datetime Delivery', keyword = True),
			Argument('Datetime Response Due', keyword = True),
			Argument('Datetime Response Close', keyword = True),
			Argument('Title', keyword = True),
			Argument('Body', keyword = True)
		)
	)
	competition_InjectDel = Endpoint(
		'api.competitionInjectDel',
		args = (
			Argument('Inject', keyword = True)
		)
	)
	competition_InjectSet = Endpoint(
		'api.competitionInjectSet',
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
		'api.competitionInjectGet',
		args = ())

	competition_InjectResponseAdd = Endpoint(
		'api.competitionInjectResponseAdd',
		args = ())
	competition_InjectResponseDel = Endpoint(
		'api.competitionInjectResponseDel',
		args = ())
	competition_InjectResponseSet = Endpoint(
		'api.competitionInjectResponseSet',
		args = ())
	competition_InjectResponseGet = Endpoint(
		'api.competitionInjectResponseGet',
		args = ())

	competition_IncidentAdd = Endpoint(
		'api.competitionIncidentAdd',
		args = ())
	competition_IncidentDel = Endpoint(
		'api.competitionIncidentDel',
		args = ())
	competition_IncidentSet = Endpoint(
		'api.competitionIncidentSet',
		args = ())
	competition_IncidentGet = Endpoint(
		'api.competitionIncidentSet',
		args = ())

	competition_IncidentResponseAdd = Endpoint(
		'api.competitionIncidentResponseAdd',
		args = ())
	competition_IncidentResponseDel = Endpoint(
		'api.competitionIncidentResponseDel',
		args = ())
	competition_IncidentResponseSet = Endpoint(
		'api.competitionIncidentResponseSet',
		args = ())
	competition_IncidentResponseGet = Endpoint(
		'api.competitionIncidentResponseGet',
		args = ())

	organization_Add = Endpoint(
		'api.organizationAdd',
		args = ())
	organization_Del = Endpoint(
		'api.organizationDel',
		args = ())
	organization_Set = Endpoint(
		'api.organizationSet',
		args = ())
	organization_Get = Endpoint(
		'api.organizationGet',
		args = ())

	user_Add = Endpoint(
		'api.userAdd',
		args = ())
	user_Del = Endpoint(
		'api.userDel',
		args = ())
	user_Set = Endpoint(
		'api.userSet',
		args = ())
	user_get = Endpoint(
		'api.userGet',
		args = ())

	document_Add = Endpoint(
		'api.documentAdd',
		args = ())
	document_Del = Endpoint(
		'api.documentDel',
		args = ())
	document_Set = Endpoint(
		'api.documentSet',
		args = ())
	document_Get = Endpoint(
		'api.documentGet',
		args = ())

	scoringEngine_Add = Endpoint(
		'api.scoringEngineAdd',
		args = ())
	scoringEngine_Del = Endpoint(
		'api.scoringEngineDel',
		args = ())
	scoringEngine_Set = Endpoint(
		'api.scoringEngineSet',
		args = ())
	scoringEngine_Get = Endpoint(
		'api.scoringEngineGet',
		args = ())

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
	rpcUsername = "guest"
	rpcPassword = "guest"
	rpcHost = "localhost"
	amqpUsername = "guest"
	amqpPassword = "guest"
	amqpHost = "localhost"
	conn = Celery( \
		'tasks', \
		backend = "rpc://%s:%s@%s//" % (rpcUsername, rpcPassword, rpcHost), \
		broker = "amqp://%s:%s@%s//" % (amqpUsername, amqpPassword, amqpHost))
	return conn

if __name__ == "__main__":
	if len(sys.argv) == 1:
		help()
	commandStr = sys.argv[1]
	try:
		command = getattr(CssefClient, commandStr.replace('-','_'))
	except AttributeError:
		sys.exit("No such option: %s" % commandStr)
	command.conn = getConn()
	output = command(sys.argv[2:])