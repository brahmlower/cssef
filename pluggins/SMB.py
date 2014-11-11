#from smb.SMBConnection import SMBConnection
#from socket import gethostname
import subprocess
import os

import traceback
from ScoringUtils import Score
from ScoringUtils import Pluggin
from ScoringUtils import PlugginTest

# This requires pysmb:
# sudo pip install pysmb
#
# Some resources I used:
# http://stackoverflow.com/questions/10248796/example-of-pysmb
# https://pythonhosted.org/pysmb/api/smb_SharedFile.html

class SMB(Pluggin):
	team_config_type_dict = {
		#"port":int,
		"username":str,
		"password":str,
		"network":str,
		#"timeout":int}

	def __init__(self, conf_dict):
		Pluggin.__init__(self, conf_dict)

	def score(self, team):
		team_config = team.score_configs[self.__class__.__name__]
		address = self.build_address(team_config)

		bproc = "smbclient -L "+address
		bproc += " -U " + team_config["username"] + "%" + team_config["password"]
		FNULL = open(os.devnull, "w")
		proc = subprocess.Popen(bproc.split(), stdout=subprocess.PIPE, stderr=FNULL)
		output = proc.communicate()[0]
		rt = proc.returncode
		FNULL.close()
		if rt == "0" or rt == 0:
			return Score(True, self.points, success_msg="")
		else:
			return Score(False, 0, error_msg="")

class Test(PlugginTest):
	def __init__(self):
		PlugginTest.__init__(self, SMB)