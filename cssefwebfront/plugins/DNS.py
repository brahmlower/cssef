# Imports required for django modules
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cssefwebfront.settings'
from django.conf import settings

# Imports required for base pluggin
from cssefwebfront.models import Score
from cssefwebfront.ScoringUtils import Plugin
from cssefwebfront.ScoringUtils import PluginTest

from django.utils.html import escape
import traceback
import socket

class DNS(Plugin):
	team_config_type_dict = {
		"domainname": str
	}
	def __init__(self, service_obj):
		Plugin.__init__(self, service_obj)

	def score(self, team_obj):
		self.update_configuration(team_obj)
		domains = self.domainname.split(",")
		for i in domains:
			addr = self.build_address(machineaddr = i)
			try:
				socket.gethostbyname(addr)
			except socket.gaierror:
				new_score = Score()
				new_score.value = 0
				new_score.message = "Domain name: %s<br>Traceback: %s" % (addr, escape(traceback.format_exc().splitlines()[-1]))
				return new_score
		new_score = Score()
		new_score.value = self.points
		new_score.message = ""
		return new_score

