from django.http import StreamingHttpResponse
from django.http import HttpResponse
from models import IncidentResponse
from models import InjectResponse
from models import Document
from models import Inject
from utils import getAuthValues
from urllib import unquote

from django.core.servers.basehttp import FileWrapper

def verify_user(ad, id_name):
	c = getAuthValues(ad['request'], {})
	# Only white team and blue team may access these files
	if c["auth_name"] != "auth_team_white" and c["auth_name"] != "auth_team_blue":
		print "you're not properly authenticated"
		return HttpResponse()
	# Limits blue teams to accessing only their own inject files
	if c["auth_name"] == "auth_team_blue" and ad['request'].user.compid != int(ad['compid']):
		print "you're blue team, trying to access other peoples documents"
		return HttpResponse()

def inject(request, compid = None, ijctid = None, filename = None):
	verify_user(locals(), 'ijctid')
	filename = unquote(filename)
	ijct_obj = Inject.objects.get(compid = compid, ijctid = ijctid)
	doc_obj = Document.objects.get(inject = ijct_obj, filename = filename)
	rfile = open(doc_obj.filepath, 'r')
	return StreamingHttpResponse(rfile, content_type = doc_obj.get_cleaned_content_type())

def injectresponse(request, compid = None, teamid = None, ijctrespid = None, filename = None):
	verify_user(locals(), 'ijctrespid')
	filename = unquote(filename)
	ijct_resp_obj = InjectResponse.objects.get(compid = compid, teamid = teamid, ijctrespid = ijctrespid)
	doc_obj = Document.objects.get(injectresponse = ijct_resp_obj, filename = filename)
	rfile = open(doc_obj.filepath, 'r')
	return HttpResponse(rfile, content_type = doc_obj.get_cleaned_content_type())

def incidentresponse(request, compid = None, teamid = None, intrspid = None, filename = None):
	verify_user(locals(), 'intrspid')
	filename = unquote(filename)
	icdt_resp_obj = IncidentResponse.objects.get(compid = compid, teamid = teamid, intrspid = intrspid)
	doc_obj = Document.objects.get(incidentresponse = icdt_resp_obj, filename = filename)
	rfile = open(doc_obj.filepath, 'r')
	return StreamingHttpResponse(rfile, content_type = doc_obj.get_cleaned_content_type())

