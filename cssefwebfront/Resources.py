from django.http import StreamingHttpResponse
from django.http import HttpResponse
from models import IncidentResponse
from models import InjectResponse
from utils import getAuthValues

def verify_user(ad, id_name):
	c = getAuthValues(ad['request'], {})
	# Malformed url (this shouldn't happen, now that I think about it...)
	if ad['compid'] == None or ad['teamid'] == None or ad['filename'] == None or ad[id_name] == None:
		print "you didn't provide all the things"
		return HttpResponse()
	# Only white team and blue team may access these files
	if c["auth_name"] != "auth_team_white" and c["auth_name"] != "auth_team_blue":
		print "you're not properly authenticated"
		return HttpResponse()
	# Limits blue teams to accessing only their own inject files
	if c["auth_name"] == "auth_team_blue" and (ad['request'].user.compid != int(ad['compid']) or ad['request'].user.teamid != int(ad['teamid'])):
		print "you're blue team, trying to access other peoples documents"
		return HttpResponse()

def injectresponse(request, compid = None, teamid = None, ijctrespid = None, filename = None):
	verify_user(locals(), 'ijctrespid')
	ijct_resp_obj = InjectResponse.objects.get(compid = compid, teamid = teamid, ijctrespid = ijctrespid, filename = filename)
	rfile = open(ijct_resp_obj.filepath, 'r')
	return StreamingHttpResponse(rfile, content_type='application/force-download')

def incidentresponse(request, compid = None, teamid = None, intrspid = None, filename = None):
	verify_user(locals(), 'intrspid')
	ijct_resp_obj = IncidentResponse.objects.get(compid = compid, teamid = teamid, intrspid = intrspid, filename = filename)
	rfile = open(ijct_resp_obj.filepath, 'r')
	return StreamingHttpResponse(rfile, content_type='application/force-download')

