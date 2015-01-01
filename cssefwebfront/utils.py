import json
from models import Service
from models import Team
from models import Inject
from hashlib import md5
import settings
from django.core.files.uploadedfile import UploadedFile
from models import Document
from urllib import quote
import settings


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

def save_document(request_file, content_subdir, related_obj, ashash = True):
	uploadedfile = UploadedFile(request_file)
	file_content = uploadedfile.read()
	doc_obj = Document()
	doc_obj.filehash = md5(file_content).hexdigest()
	doc_obj.urlencfilename = quote(uploadedfile.name)
	doc_obj.filename = uploadedfile.name
	if ashash:
		doc_obj.filepath = settings.BASE_DIR + content_subdir + doc_obj.filehash
	else:
		doc_obj.filepath = settings.BASE_DIR + content_subdir + doc_obj.filename
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

def buildTeamServiceConfigForms(compid, team_score_dict = None):
	if team_score_dict != None:
		team_score_dict = json.loads(team_score_dict)
	tmp_list = []
	for serv_obj in Service.objects.filter(compid = compid):
		module_name = Document.objects.get(servicemodule = serv_obj.servicemodule).filename.split(".")[0]
		module_inst = getattr(__import__(settings.CONTENT_PLUGGINS_PATH.replace('/','.')[1:] + module_name, fromlist=[module_name]), module_name)(serv_obj)
		#module_inst = getattr(__import__('pluggins.' + module_name, fromlist=[module_name]), module_name)(serv_obj)
		config_dict = getattr(module_inst, "team_config_type_dict")
		#print config_dict
		config_list = []
		for key in config_dict:
			tmp_dict = {}
			tmp_dict["label"] = key
			tmp_dict["id_for_label"] = "%s-%s" % (serv_obj.name, key)
			if config_dict[key] == int:
				tmp_dict["type"] = "number"
			elif config_dict[key] == str:
				tmp_dict["type"] = "text"
			if team_score_dict != None and serv_obj.name in team_score_dict:
				tmp_dict["value"] = team_score_dict[serv_obj.name][key]
			config_list.append(tmp_dict)
		tmp_list.append({
			"service": serv_obj,
			"configs": config_list
		})
	return tmp_list

def buildTeamServiceConfigDict(compid, post_dict):
	tmp_dict = {}
	for serv_obj in Service.objects.filter(compid = compid):
		module_name = Document.objects.get(servicemodule = serv_obj.servicemodule).filename.split(".")[0]
		module_inst = getattr(__import__(settings.CONTENT_PLUGGINS_PATH.replace('/','.')[1:] + module_name, fromlist=[module_name]), module_name)(serv_obj)
		config_dict = getattr(module_inst, "team_config_type_dict")
		serv_dict = {}
		for key in config_dict:
			if serv_obj.name + "-" + key in post_dict:
				serv_dict[key] = post_dict.pop(serv_obj.name + "-" + key)
				# If it's in a list, pull it out of the list
				if serv_dict[key].__class__.__name__ == "list":
					serv_dict[key] = serv_dict[key][0]
				# Now cast it as its intended value type
				if len(serv_dict[key]) != 0:
					serv_dict[key] = config_dict[key](serv_dict[key])
		tmp_dict[serv_obj.name] = serv_dict
	return json.dumps(tmp_dict)
