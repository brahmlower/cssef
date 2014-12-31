# Imports required for django modules
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cssefwebfront.settings'
from django.conf import settings

# Imports required for base pluggin
from cssefwebfront.models import Score
from ScoringUtils import Pluggin
from ScoringUtils import PlugginTest
import json

# Imports required for specific pluggin
from ftplib import FTP as ftp
from ftplib import error_perm as ftp_error_perm
import traceback

class FTP(Pluggin):
	team_config_type_dict = {
		"port":int,
		"username":str,
		"password":str,
		"network":str,
		"timeout":int}

	def __init__(self, conf_dict):
		Pluggin.__init__(self, conf_dict)

	def score(self, team, service_name):
		team_config = json.loads(team.score_configs)[service_name]
		address = self.build_address(team_config)
		new_score = Score()
		try:
			client = ftp.connect(
				address,
				team_config["port"],
				team_config["timeout"])
			client.login(
				team_config["username"],
				team_config["password"])
			client.close()
			new_score.value = self.points
			new_score.message = ""
		except:
			new_score.value = 0
			new_score.message = "Address: %s<br>Port: %s<br>Traceback: %s" % \
				(address,str(team_config["port"]),escape(traceback.format_exc().splitlines()[-1]))
		return new_score

class Test(PlugginTest):
	def __init__(self):
		PlugginTest.__init__(self, FTP)
