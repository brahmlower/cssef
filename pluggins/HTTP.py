# Imports required for django modules
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cssefwebfront.settings'
from django.conf import settings

# Imports required for base pluggin
from cssefwebfront.models import Score
from ScoringUtils import Pluggin
from ScoringUtils import PlugginTest

# Imports required for specific pluggin
from urllib2 import urlopen
import traceback

class HTTP(Pluggin):
	team_config_type_dict = {
		"port":int,
		"network":str,
		"timeout":int
		}

	def __init__(self, conf_dict):
		Pluggin.__init__(self, conf_dict)

	def score(self, team):
		team_config = team.score_configs[self.__class__.__name__]
		address = "http://%s:%s" %(self.build_address(team_config), str(team_config["port"]))
		new_score = Score()
		try:
			request = urlopen(address)
			html = request.read()
			new_score.value = self.points
			new_score.message = ""
		except:
			new_score.value = 0
			new_score.message = traceback.format_exc()
		return new_score

class Test(PlugginTest):
	def __init__(self):
		PlugginTest.__init__(self, HTTP)
