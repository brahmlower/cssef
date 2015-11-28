#!/usr/bin/python
from celery import Celery
import sys
from time import sleep
from prettytable import PrettyTable

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
		self.conn = None
		self.celeryName = celeryName
		self.args = None

	def __call__(self, *args, **kwargs):
		x = self.conn.send_task(self.celeryName, args = args, kwargs = kwargs)
		return x.get()

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
	competitionDel = Endpoint(
		'competitionDel',
		args = (
			Argument('Competition', keyword = True),
		)
	)
	competitionSet = Endpoint(
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
	competitionGet = Endpoint(
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

	competitionTeamAdd = Endpoint(
		'competitionTeamAdd',
		args = (
			Argument('Competition', keyword = True),
			Argument('Name', keyword = True),
			Argument('Username', keyword = True),
			Argument('Password', keyword = True),
			Argument('Network CIDR', keyword = True, optional = True)
		)
	)
	competitionTeamDel = Endpoint(
		'competitionTeamDel',
		args = (
			Argument('Team', keyword = True),
		)
	)
	competitionTeamSet = Endpoint(
		'competitionTeamSet',
		args = (
			Argument('Name', keyword = True, optional = True),
			Argument('Username', keyword = True, optional = True),
			Argument('Password', keyword = True, optional = True),
			Argument('Network CIDR', keyword = True, optional = True)
		)
	)
	competitionTeamGet = Endpoint(
		'competitionTeamGet',
		args = (
			Argument('Name', optional = True),
			Argument('Username', optional = True),
			Argument('Password', optional = True),
			Argument('Network CIDR', optional = True)
		)
	)

	competitionScoreAdd = Endpoint(
		'competitionScoreAdd',
		args = (
			Argument('Competition', keyword = True),
			Argument('Team', keyword = True),
			Argument('Datetime', keyword = True),
			Argument('Value', keyword = True),
			Argument('Message', keyword = True, optional = True)
		)
	)
	competitionScoreDel = Endpoint(
		'competitionScoreDel',
		args = (
			Argument('Score', keyword = True)
		)
	)
	competitionScoreSet = Endpoint(
		'competitionScoreSet',
		args = (
			Argument('Datetime', keyword = True, optional = True),
			Argument('Value', keyword = True, optional = True),
			Argument('Message', keyword = True, optional =True)
		)
	)
	competitionScoreGet = Endpoint(
		'competitionScoreGet',
		args = (
			Argument('Datetime', optional = True),
			Argument('Value', optional = True),
			Argument('Message', optional = True)
		)
	)

	competitionInjectAdd = Endpoint(
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
	competitionInjectDel = Endpoint(
		'competitionInjectDel',
		args = (
			Argument('Inject', keyword = True)
		)
	)
	competitionInjectSet = Endpoint(
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
	competitionInjectGet = Endpoint(
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

	competitionInjectResponseAdd = Endpoint(
		'competitionInjectResponseAdd',
		args = (
			Argument('Competition', keyword = True),
			Argument('Team', keyword = True),
			Argument('Inject', keyword = True),
			Argument('Datetime', keyword = True),
			Argument('Content', keyword = True)
		)
	)
	competitionInjectResponseDel = Endpoint(
		'competitionInjectResponseDel',
		args = (
			Argument('Inject Response', keyword = True)
		)
	)
	competitionInjectResponseSet = Endpoint(
		'competitionInjectResponseSet',
		args = (
			Argument('Competition', keyword = True, optional = True),
			Argument('Team', keyword = True, optional = True),
			Argument('Inject', keyword = True, optional = True),
			Argument('Datetime', keyword = True, optional = True),
			Argument('Content', keyword = True, optional = True)
		)
	)
	competitionInjectResponseGet = Endpoint(
		'competitionInjectResponseGet',
		args = (
			Argument('Competition', optional = True),
			Argument('Team', optional = True),
			Argument('Inject', optional = True),
			Argument('Datetime', optional = True),
			Argument('Content', optional = True)
		)
	)

	competitionIncidentAdd = Endpoint(
		'competitionIncidentAdd',
		args = (
			Argument('Competition', keyword = True),
			Argument('Team', keyword = True),
			Argument('Datetime', keyword = True),
			Argument('Subject', keyword = True),
			Argument('Content', keyword = True),
		)
	)
	competitionIncidentDel = Endpoint(
		'competitionIncidentDel',
		args = (
			Argument('Incident', keyword = True)
		)
	)
	competitionIncidentSet = Endpoint(
		'competitionIncidentSet',
		args = (
			Argument('Competition', keyword = True, optional = True),
			Argument('Team', keyword = True, optional = True),
			Argument('Datetime', keyword = True, optional = True),
			Argument('Subject', keyword = True, optional = True),
			Argument('Content', keyword = True, optional = True),
		)
	)
	competitionIncidentGet = Endpoint(
		'competitionIncidentSet',
		args = (
			Argument('Competition', optional = True),
			Argument('Team', optional = True),
			Argument('Datetime', optional = True),
			Argument('Subject', optional = True),
			Argument('Content', optional = True)
		)
	)

	competitionIncidentResponseAdd = Endpoint(
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
	competitionIncidentResponseDel = Endpoint(
		'competitionIncidentResponseDel',
		args = (
			Argument('Incident Response', keyword = True)
		)
	)
	competitionIncidentResponseSet = Endpoint(
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
	competitionIncidentResponseGet = Endpoint(
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

	organizationAdd = Endpoint(
		'organizationAdd',
		args = (
			Argument('Name', keyword = True),
			Argument('URL', keyword = True),
			Argument('Description', keyword = True),
			Argument('Max Members', keyword = True, optional = True),
			Argument('Max Competitions', keyword = True, optional = True)
		)
	)
	organizationDel = Endpoint(
		'organizationDel',
		args = (
			Argument('Organization', keyword = True)
		)
	)
	organizationSet = Endpoint(
		'organizationSet',
		args = (
			Argument('Name', keyword = True, optional = True),
			Argument('URL', keyword = True, optional = True),
			Argument('Description', keyword = True, optional = True),
			Argument('Max Members', keyword = True, optional = True),
			Argument('Max Competitions', keyword = True, optional = True)
		)
	)
	organizationGet = Endpoint(
		'organizationGet',
		args = (
			Argument('Name', optional = True),
			Argument('URL', optional = True),
			Argument('Description', optional = True),
			Argument('Max Members', optional = True),
			Argument('Max Competitions', optional = True)
		)
	)

	userAdd = Endpoint(
		'userAdd',
		args = (
			Argument('Organization', keyword = True),
			Argument('Name', keyword = True),
			Argument('Username', keyword = True),
			Argument('Password', keyword = True),
			Argument('Description', keyword = True, optional = True)
		)
	)
	userDel = Endpoint(
		'userDel',
		args = (
			Argument('User', keyword = True),
		)
	)
	userSet = Endpoint(
		'userSet',
		args = (
			Argument('Organization', keyword = True, optional = True),
			Argument('Name', keyword = True, optional = True),
			Argument('Username', keyword = True, optional = True),
			Argument('Password', keyword = True, optional = True),
			Argument('Description', keyword = True, optional = True)
		)
	)
	userGet = Endpoint(
		'userGet',
		args = (
			Argument('Organization', optional = True),
			Argument('Name', optional = True),
			Argument('Username', optional = True),
			Argument('Password', optional = True),
			Argument('Description', optional = True)
		)
	)

	documentAdd = Endpoint(
		'documentAdd',
		args = ())
	documentDel = Endpoint(
		'documentDel',
		args = ())
	documentSet = Endpoint(
		'documentSet',
		args = ())
	documentGet = Endpoint(
		'documentGet',
		args = ())

	scoringEngineAdd = Endpoint(
		'scoringEngineAdd',
		args = (
			Argument("Name", keyword = True, optional = False),
			Argument("Package Name", keyword = True, optional = False),
		)
	)
	scoringEngineDel = Endpoint(
		'scoringEngineDel',
		args = (
			Argument("Scoring Engine", keyword = True, optional = False)
		)
	)
	scoringEngineSet = Endpoint(
		'scoringEngineSet',
		args = (
			Argument('Name', keyword = True, optional = True),
			Argument('Package Name', keyword = True, optional = True),
			Argument('Disabled', keyword = True, optional = True)
		)
	)
	scoringEngineGet = Endpoint(
		'scoringEngineGet',
		args = (
			Argument('Name', optional = True),
			Argument('Package Name', optional = True),
			Argument('Disabled', optional = True)
		)
	)

def help():
	print "competition team"
	print "\tcompetition-team-add\n\tcompetition-team-del"
	print "\tcompetition-team-set\n\tcompetition-team-get"

	print "competition score"
	print "\tcompetition-score-add\n\tcompetition-score-del"
	print "\tcompetition-score-set\n\tcompetition-score-get"

	print "competition inject"
	print "\tcompetition-inject-add\n\tcompetition-inject-del"
	print "\tcompetition-inject-set\n\tcompetition-inject-get"

	print "competition inject response"
	print "\tcompetition-injectresponse-add\n\tcompetition-injectresponse-del"
	print "\tcompetition-injectresponse-set\n\tcompetition-injectresponse-get"

	print "competition incident"
	print "\tcompetition-incident-add\n\tcompetition-incident-del"
	print "\tcompetition-incident-set\n\tcompetition-incident-get"

	print "competition incident response"
	print "\tcompetition-incidentresponse-add\n\tcompetition-incidentresponse-del"
	print "\tcompetition-incidentresponse-set\n\tcompetition-incidentresponse-get"
	exit()

def getConn():
	rpcUsername = "cssefd"
	rpcPassword = "cssefd-pass"
	rpcHost = "localhost"

	amqpUsername = "cssefd"
	amqpPassword = "cssefd-pass"
	amqpHost = "localhost"
	
	conn = Celery(
		'api',
		backend = "rpc://%s:%s@%s//" % (rpcUsername, rpcPassword, rpcHost),
		broker = "amqp://%s:%s@%s//" % (amqpUsername, amqpPassword, amqpHost)
	)
	return conn

if __name__ == "__main__":
	commands = {
		"competition-add": CssefClient.competitionAdd,
		"competition-del": CssefClient.competitionDel,
		"competition-set": CssefClient.competitionSet,
		"competition-get": CssefClient.competitionGet,
		"competition-team-add": CssefClient.competitionTeamAdd,
		"competition-team-del": CssefClient.competitionTeamDel,
		"competition-team-set": CssefClient.competitionTeamSet,
		"competition-team-get": CssefClient.competitionTeamGet,
		"competition-score-add": CssefClient.competitionScoreAdd,
		"competition-score-del": CssefClient.competitionScoreDel,
		"competition-score-set": CssefClient.competitionScoreSet,
		"competition-score-get": CssefClient.competitionScoreGet,
		"competition-inject-add": CssefClient.competitionInjectAdd,
		"competition-inject-del": CssefClient.competitionInjectDel,
		"competition-inject-set": CssefClient.competitionInjectSet,
		"competition-inject-get": CssefClient.competitionInjectGet,
		"competition-injectresponse-add": CssefClient.competitionInjectResponseAdd,
		"competition-injectresponse-del": CssefClient.competitionInjectResponseDel,
		"competition-injectresponse-set": CssefClient.competitionInjectResponseSet,
		"competition-injectresponse-get": CssefClient.competitionInjectResponseGet,
		"competition-incident-add": CssefClient.competitionIncidentAdd,
		"competition-incident-del": CssefClient.competitionIncidentDel,
		"competition-incident-set": CssefClient.competitionIncidentSet,
		"competition-incident-get": CssefClient.competitionIncidentGet,
		"competition-incidentresponse-add": CssefClient.competitionIncidentResponseAdd,
		"competition-incidentresponse-del": CssefClient.competitionIncidentResponseDel,
		"competition-incidentresponse-set": CssefClient.competitionIncidentResponseSet,
		"competition-incidentresponse-get": CssefClient.competitionIncidentResponseGet,
		"organization-add": CssefClient.organizationAdd,
		"organization-del": CssefClient.organizationDel,
		"organization-set": CssefClient.organizationSet,
		"organization-get": CssefClient.organizationGet,
		"user-add": CssefClient.userAdd,
		"user-del": CssefClient.userDel,
		"user-set": CssefClient.userSet,
		"user-get": CssefClient.userGet,
		"document-add": CssefClient.documentAdd,
		"document-del": CssefClient.documentDel,
		"document-set": CssefClient.documentSet,
		"document-get": CssefClient.documentGet,
		"scoringengine-add": CssefClient.scoringEngineAdd,
		"scoringengine-del": CssefClient.scoringEngineDel,
		"scoringengine-set": CssefClient.scoringEngineSet,
		"scoringengine-get": CssefClient.scoringEngineGet,
	}

	DEBUG = True

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
	if output['value'] == 0:
		# No error
		if len(output['content']) > 0:
			outputTable = PrettyTable(output['content'][0].keys())
			outputTable.padding_width = 1
			for i in output['content']:
				outputTable.add_row(i.values())
			print outputTable
	else:
		# Error!
		print "Error code: %d" % output['value']
		print "The server returned:"
		if DEBUG:
			for i in output['message']:
				print i
		else:
			print output['message']
		print "Please see /var/log/cssef/logging on the server for the full stack trace."