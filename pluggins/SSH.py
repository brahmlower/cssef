import paramiko

import traceback
from ScoringUtils import Score
from ScoringUtils import Pluggin
from ScoringUtils import PlugginTest

# TODO: This should eventually support keys

class SSH(Pluggin):
	team_config_type_dict = {
		"port":int,
		"username":str,
		"password":str,
		"network":str,
		"timeout":int}

	def __init__(self, conf_dict):
		Pluggin.__init__(self, conf_dict)

	def score(self, team):
		team_config = team.score_configs[self.__class__.__name__]
		address = self.build_address(team_config)

		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			client.connect(
				address,
				team_config["port"],
				team_config["username"],
				team_config["password"],
				timeout=team_config["timeout"])
			client.close()
			return Score(True, self.points, success_msg="")
		except:
			return Score(False, 0, error_msg=traceback.format_exc())

class Test(PlugginTest):
	def __init__(self):
		PlugginTest.__init__(self, SSH)


