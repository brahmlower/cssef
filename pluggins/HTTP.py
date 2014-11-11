from urllib2 import urlopen

import traceback
from ScoringUtils import Score
from ScoringUtils import Pluggin
from ScoringUtils import PlugginTest

class HTTP(Pluggin):
	team_config_type_dict = {
		"port":str,
		"network":str,
		"timeout":int}

	def __init__(self, conf_dict):
		Pluggin.__init__(self, conf_dict)

	def score(self, team):
		team_config = team.score_configs[self.__class__.__name__]
		address = "http://%s:%s" %(self.build_address(team_config), team_config["port"])
		try:
			request = urlopen(address)
			html = request.read()
			return Score(True, self.points, success_msg="")
		except:
			return Score(False, 0, error_msg=traceback.format_exc())

class Test(PlugginTest):
	def __init__(self):
		PlugginTest.__init__(self, HTTP)
