from ftplib import FTP as ftp
from ftplib import error_perm as ftp_error_perm

class FTP:
	def __init__(self, conf_dict):
		self.id = conf_dict["id"]
		self.name = conf_dict["name"]
		self.port = conf_dict["port"]
		self.username = conf_dict["username"]
		self.password = conf_dict["password"]
		self.points = conf_dict["points"]

	def score(self, team):
		host = team.net_addr
		client = ftp(host)
		try:
			client.login(self.username, self.password)
			return self.points
		except ftp_error_perm:
			return 0