from django.http import StreamingHttpResponse
from django.http import HttpResponse
from models import InjectResponse
from utils import getAuthValues

def inject(request, compid = None, teamid = None, ijctrespid = None, filename = None):
	c = {}
	c = getAuthValues(request, c)
	# Malformed url (this shouldn't happen, now that I think about it...)
	if compid == None or teamid == None or ijctrespid == None or filename == None:
		print "you didn't provide all the things"
		return HttpResponse()
	# Only white team and blue team may access these files
	if c["auth_name"] != "auth_team_white" and c["auth_name"] != "auth_team_blue":
		print "you're not properly authenticated"
		return HttpResponse()
	# Limits blue teams to accessing only their own inject files
	if c["auth_name"] == "auth_team_blue" and (request.user.compid != int(compid) or request.user.teamid != int(teamid)):
		print "you're blue team, trying to access other peoples documents"
		return HttpResponse()
	# Now get the targeted inject response object
	ijct_resp_obj = InjectResponse.objects.get(compid = compid, teamid = teamid, ijctrespid = ijctrespid, filename = filename)
	rfile = open(ijct_resp_obj.filepath, 'r')
	return StreamingHttpResponse(rfile, content_type='application/force-download')

