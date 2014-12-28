# Imports required for django modules
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cssefwebfront.settings'
from django.conf import settings

# Imports required for base pluggin
from cssefwebfront.models import Score
from ScoringUtils import Pluggin
from ScoringUtils import PlugginTest

# Imports required for specific pluggin
import paramiko
import traceback

# TODO: This should eventually support keys

class SSH(Pluggin):
	team_config_type_dict = {
		"port": int,
		"username": str,
		"password": str,
		"network": str,
		"timeout": int
	}

	def __init__(self, conf_dict):
		Pluggin.__init__(self, conf_dict)

	def score(self, team):
		team_config = team.score_configs[self.__class__.__name__]
		address = self.build_address(team_config)

		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		new_score = Score()
		try:
			client.connect(
				address,
				team_config["port"],
				team_config["username"],
				team_config["password"],
				timeout=team_config["timeout"])
			client.close()
			new_score.value = self.points
			new_score.message = ""
		except:
			new_score.value = 0
			new_score.message = traceback.format_exc()
		return new_score

class Test(PlugginTest):
	def __init__(self):
		PlugginTest.__init__(self, SSH)