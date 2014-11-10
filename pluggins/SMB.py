#from smb.SMBConnection import SMBConnection
#from socket import gethostname
import subprocess
import os

# This requires pysmb:
# sudo pip install pysmb
#
# Some resources I used:
# http://stackoverflow.com/questions/10248796/example-of-pysmb
# https://pythonhosted.org/pysmb/api/smb_SharedFile.html

class SMB:
	def __init__(self, dict_obj):
		self.username = dict_obj["username"]
		self.password = dict_obj["password"]
		self.points = dict_obj["points"]
		self.subdomain = dict_obj["subdomain"]


	def score(self, team):
		host = self.subdomain + "." + team.domainname
		bproc = "smbclient -L "+host
		bproc += " -U " + self.username + "%" + self.password
		FNULL = open(os.devnull, "w")
		proc = subprocess.Popen(bproc.split(), stdout=subprocess.PIPE, stderr=FNULL)
		output = proc.communicate()[0]
		rt = proc.returncode 
		if rt == "0" or rt == 0:
			return self.points
		else:
			return 0
