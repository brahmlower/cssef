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
		"timeout": int
	}

	def __init__(self, service_obj):
		Pluggin.__init__(self, service_obj)

	def score(self, team_obj):
		self.update_configuration(team_obj)
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		new_score = Score()
		try:
			client.connect(
				self.build_address(),
				self.port,
				self.username,
				self.password,
				timeout=self.timeout)
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