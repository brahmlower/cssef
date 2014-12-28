# Imports required for django modules
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cssefwebfront.settings'
from django.conf import settings

# Imports required for base pluggin
from cssefwebfront.models import Score
from ScoringUtils import Pluggin
from ScoringUtils import PlugginTest

# Imports required for specific pluggin
#from smb.SMBConnection import SMBConnection
#from socket import gethostname
import subprocess
import traceback

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
		"network":str}
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
		new_score = Score()
		if rt == "0" or rt == 0:
			new_score.value = self.points
			new_score.message = ""
		else:
			new_score.value = 0
			new_score.message = str(rt)
		return new_score

class Test(PlugginTest):
	def __init__(self):
		PlugginTest.__init__(self, SMB)