from smb.SMBConnection import SMBConnection
from socket import gethostname

# This requires pysmb:
# sudo pip install pysmb
#
# Some resources I used:
# http://stackoverflow.com/questions/10248796/example-of-pysmb
# https://pythonhosted.org/pysmb/api/smb_SharedFile.html

class SMB:
	def __init__(self, conf_dict):
		self.id = conf_dict["id"]
		self.name = conf_dict["name"]
		self.port = conf_dict["port"]
		self.username = conf_dict["username"]
		self.password = conf_dict["password"]
		self.points = conf_dict["points"]

		self.localhostname = gethostname()

	def score(self, team):
		#host = team.net_addr
		host = "192.168.0.100"
		conn = SMBConnection(self.username, self.password, self.localhostname, host, use_ntlm_v2=True)
		x = conn.connect(host, int(self.port))
		if x:
			conn.close()
			return self.points
		else:
			conn.close()
			return 0
