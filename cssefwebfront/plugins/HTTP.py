# Imports required for django modules
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cssefwebfront.settings'
from django.conf import settings

# Imports required for base plugin
from cssefwebfront.models import Score
from cssefwebfront.ScoringUtils import Plugin
from cssefwebfront.ScoringUtils import Integer
from cssefwebfront.ScoringUtils import Boolean
from cssefwebfront.ScoringUtils import String

# Imports required for specific plugin
from django.utils.html import escape
from urllib2 import urlopen
import traceback


class HTTP(Plugin):
	plugin_config = {
		"fields": {
			"port":			{"name": "port",		"instance": Integer(label="Port", default_value=80, required=True)},
			"timeout":		{"name": "timeout",		"instance": Integer(label="Timeout", required=True)},
			"str_match":	{"name": "str_match",	"instance": Boolean(label="Match String", default_value=True, required=False)},
			"str_value":	{"name": "str_value",	"instance": String(label="String", depends="str_match", required = True)},
			"md5_match":	{"name": "md5_match",	"instance": Boolean(label="Match MD5", default_value=False, required=False)},
			"md5_value":	{"name": "md5_value",	"instance": String(label="MD5", depends="md5_match", required = False)}
		}
	}

	def score(self, team_obj):
		self.update_configuration(team_obj)
		address = "http://" + self.build_address(withport = True)
		print self.__dict__
		new_score = Score()
		try:
			self.timeout
			use_timeout = True
		except AttributeError:
			use_timeout = False
		try:
			if use_timeout:
				request = urlopen(address, timeout = self.timeout)
			else:
				request = urlopen(address)
			html = request.read()
			new_score.value = self.points
			new_score.message = ""
		except:
			new_score.value = 0
			new_score.message = "Address: %s<br>Traceback: %s" % (address, escape(traceback.format_exc().splitlines()[-1]))
		return new_score