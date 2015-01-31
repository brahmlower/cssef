# Imports required for django modules
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cssefwebfront.settings'
from django.conf import settings

# Imports required for base pluggin
from cssefwebfront.models import Score
from cssefwebfront.ScoringUtils import Pluggin
from cssefwebfront.ScoringUtils import PlugginTest

# Imports required for specific pluggin
from django.utils.html import escape
from email.mime.text import MIMEText
import socket
import smtplib
import traceback

class SMTP(Pluggin):
	team_config_type_dict = {
		"to_user": str,
		"from_user": str,
		"port": int,
		"timeout": int,
	}

	def __init__(self, service_obj):
		Pluggin.__init__(self, service_obj)

	def score(self, team_obj):
		self.update_configuration(team_obj)
		address = self.build_address()

		msg = MIMEText('This is the text body')
		msg['Subject'] = 'Testing email'
		msg['From'] = self.from_user + '@galactica.fleet'
		msg['To'] = self.to_user + '@galactica.fleet'

		try:
			s = smtplib.SMTP(address, self.port, timeout = self.timeout)
			s.sendmail(self.from_address, [self.to_address], msg.as_string())
			s.quit()
		except smtplib.SMTPException:
			new_score = Score()
			new_score.value = 0
			new_score.message = "Address: %s<br>Traceback: %s" % (address, escape(traceback.format_exc().splitlines()[-1]))
			return new_score
		except socket.timeout:
			new_score = Score()
			new_score.value = 0
			new_score.message = "Address: %s<br>Traceback: %s" % (address, escape(traceback.format_exc().splitlines()[-1]))
			return new_score
		except socket.gaierror:
			new_score = Score()
			new_score.value = 0
			new_score.message = "Address: %s<br>Traceback: %s" % (address, escape(traceback.format_exc().splitlines()[-1]))
			return new_score
		new_score = Score()
		new_score.value = self.points
		new_score.message = ""
		return new_score
