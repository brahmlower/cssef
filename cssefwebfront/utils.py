import json
from models import Service
from models import Team
from models import Inject
from hashlib import md5
import settings
from django.core.files.uploadedfile import UploadedFile
from models import Document
from urllib import quote


def getAuthValues(request, c):
	c["auth"] = request.user.is_authenticated
	if request.user.is_authenticated:
		team = request.user.__class__.__name__
		if team == "Team":
			c["auth_name"] = "auth_team_blue"
			c["auth_name_display"] = "Blue Team (%s)" % request.user.teamname
		elif team == "Admin":
			c["auth_name"] = "auth_team_white"
			c["auth_name_display"] = "White Team"
		else:
			c["auth_name"] = "auth_team_red"
			c["auth_name_display"] = "Red Team"
	return c

class UserMessages:
	def __init__(self):
		self.info = []
		self.error = []
		self.success = []
	def new_info(self, string, num):
		self.info.append({"string":string, "num":num})

	def new_error(self, string, num):
		self.error.append({"string":string, "num":num})

	def new_success(self, string, num):
		self.success.append({"string":string, "num":num})

	def clear(self):
		self.info = []
		self.error = []
		self.success = []

def save_document(request_file, content_subdir, related_obj):
	uploadedfile = UploadedFile(request_file)
	file_content = uploadedfile.read()
	doc_obj = Document()
	doc_obj.filehash = md5(file_content).hexdigest()
	doc_obj.filepath = settings.BASE_DIR + content_subdir + doc_obj.filehash
	doc_obj.filename = uploadedfile.name
	doc_obj.urlencfilename = quote(uploadedfile.name)
	if related_obj.__class__.__name__.lower() == "queryset":
		if len(related_obj) == 1:
			setattr(doc_obj, related_obj[0].__class__.__name__.lower(), related_obj[0])
		else:
			print "ERROR: The queryset object had %s elements to it" % str(len(related_obj))
	else:
		setattr(doc_obj, related_obj.__class__.__name__.lower(), related_obj)
	doc_obj.save()

	wfile = open(doc_obj.filepath, "w")
	wfile.write(file_content)
	wfile.close()

def add_teams_scoreconfigs(compid):
	# Add service scoring configuration objects to each team
	services = Service.objects.filter(compid = compid)
	teams = Team.objects.filter(compid = compid)
	for t in teams:
		score_configs = json.loads(t.score_configs)
		for s in services:
			try:
				x = score_configs[s.module]
			except KeyError:
				score_configs[s.module] = {}
		target_team = Team.objects.filter(compid = compid, teamid = t.teamid)
		target_team.update(score_configs = json.dumps(score_configs))

def clean_teams_scoreconfigs(compid, module_str):
	# Removes the scoring configuration object from teams for services
	# that have been deleted
	services = Service.objects.filter(compid = compid)
	teams = Team.objects.filter(compid = compid)
	for t in teams:
		score_configs = json.loads(t.score_configs)
		score_configs.pop(module_str, None)
		target_team = Team.objects.filter(compid = compid, teamid = t.teamid)
		target_team.update(score_configs = score_configs)