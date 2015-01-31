# Imports required for django modules
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cssefwebfront.settings'
from django.conf import settings

# Imports required for base pluggin
from cssefwebfront.models import Score
from cssefwebfront.ScoringUtils import Plugin
from cssefwebfront.ScoringUtils import PluginTest

# Imports required for specific pluggin
from django.utils.html import escape
import paramiko
import traceback

# TODO: This should eventually support keys
class SSH(Plugin):
	team_config_type_dict = {
		"port": int,
		"username": str,
		"password": str,
		"timeout": int
	}

	def __init__(self, service_obj):
		Plugin.__init__(self, service_obj)

	def score(self, team_obj):
		self.update_configuration(team_obj)
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		new_score = Score()
		try:
			print "self.port: '"+str(self.port)+"'"
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
			new_score.message = "Address: %s<br>Traceback: %s" % (self.build_address(), escape(traceback.format_exc().splitlines()[-1]))
		return new_score