# Imports required for django modules
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cssefwebfront.settings'
from django.conf import settings

# Imports required for base pluggin
from cssefwebfront.models import Score
from cssefwebfront.ScoringUtils import Pluggin
from cssefwebfront.ScoringUtils import PlugginTest

# Imports required for specific pluggin
from django.utils.html import escape
from ftplib import FTP as ftp
from ftplib import error_perm as ftp_error_perm
import traceback

class FTP(Pluggin):
	team_config_type_dict = {
		"port":int,
		"username":str,
		"password":str,
		"timeout":int
	}

	def __init__(self, service_obj):
		Pluggin.__init__(self, service_obj)

	def score(self, team_obj):
		self.update_configuration(team_obj)
		new_score = Score()
		try:
			client = ftp.connect(
				self.build_address(),
				self.port,
				self.timeout)
			client.login(
				self.username,
				self.password)
			client.close()
			new_score.value = self.points
			new_score.message = ""
		except:
			new_score.value = 0
			new_score.message = "Address: %s<br>Port: %s<br>Traceback: %s" % \
				(self.build_address(),str(self.port),escape(traceback.format_exc().splitlines()[-1]))
		return new_score