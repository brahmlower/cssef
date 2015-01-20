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
from urllib2 import urlopen
import traceback


class HTTP(Pluggin):
	team_config_type_dict = {
		"port":int,
		"timeout":int
	}

	def __init__(self, service_obj):
		Pluggin.__init__(self, service_obj)

	def score(self, team_obj):
		self.update_configuration(team_obj)
		address = "http://" + self.build_address(withport = True)
		new_score = Score()
		try:
			request = urlopen(address)
			html = request.read()
			new_score.value = self.points
			new_score.message = ""
		except:
			new_score.value = 0
			new_score.message = "Address: %s<br>Traceback: %s" % (address,escape(traceback.format_exc().splitlines()[-1]))
		return new_score