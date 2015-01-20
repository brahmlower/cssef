# Imports required for django modules
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cssefwebfront.settings'
from django.conf import settings

# Imports required for base pluggin
from cssefwebfront.models import Score
from cssefwebfront.ScoringUtils import Pluggin
from cssefwebfront.ScoringUtils import PlugginTest
import json

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
	}
		#"timeout":int}

	def __init__(self, service_obj):
		Pluggin.__init__(self, service_obj)

	def score(self, team_obj, service_name):
		self.update_configuration(team_obj)

		bproc = "smbclient -L "+ self.build_address()
		bproc += " -U " + self.username + "%" + self.password
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