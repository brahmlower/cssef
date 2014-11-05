# from cssef import Score
from ftplib import FTP as ftp
from ftplib import error_perm as ftp_error_perm

class Score:
    def __init__(self, val_type, val):
        # val_type should be either 'boolean' or 'integer'
        # boolean: 1 is true, 0 is false
        # integer is any integer value
        self.val_type = val_type
        self.val = val

class FTP:
	def __init__(self, conf_dict):
		self.name = conf_dict["name"]
		self.port = 20
		self.username = conf_dict["username"]
		self.password = conf_dict["password"]

	def score(self, team):
		host = team.net_addr
		client = ftp(host)
		try:
			client.login(self.username, self.password)
			return Score('boolean',1)
			#return True
		except ftp_error_perm:
			return Score('boolean',0)
			#return False
