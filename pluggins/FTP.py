from ftplib import FTP as ftp
from ftplib import error_perm as ftp_error_perm

class FTP:
	def __init__(self, conf_dict):
		self.name = conf_dict["name"]
		self.port = conf_dict["port"]
		self.username = conf_dict["username"]
		self.password = conf_dict["password"]
		self.points = conf_dict["points"]
		self.subdomain = conf_dict["subdomain"]

	def score(self, team):
		host = self.subdomain + "." + team.domainname
		try:
			client = ftp(host)
			client.login(self.username, self.password, timeout=3)
			return self.points
		except:
			return 0
