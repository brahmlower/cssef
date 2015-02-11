# Imports required for django modules
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cssefwebfront.settings'
from django.conf import settings

# Imports required for base plugin
from cssefwebfront.models import Score
from cssefwebfront.ScoringUtils import Plugin
from cssefwebfront.ScoringUtils import PluginTest

# Imports required for specific plugin
from django.utils.html import escape
from urllib2 import urlopen
import traceback


class HTTP(Plugin):
	plugin_config = {
		"fields": [
			{"name": "port", "instance": Plugin.Integer(label="Port", default_value=80, required=True)},
			{"name": "timeout", "instance": Plugin.Integer(label="Timeout", required=True)},
			{"name": "str_match", "instance": Plugin.Boolean(label="Match String", required=False)},
			{"name": "str_value", "instance": Plugin.String(label="String", depends="str_match", required = True)},
			{"name": "md5_match", "instance": Plugin.Boolean(label="Match MD5", required=False)},
			{"name": "md5_value", "instance": Plugin.String(label="MD5", depends="md5_match", required = False)}
		]
	}

	# team_config_type_dict = {
	# 	"port": int,
	# 	"timeout": int
	# }

	def __init__(self, service_obj):
		Plugin.__init__(self, service_obj)

	def score(self, team_obj):
		self.update_configuration(team_obj)
		address = "http://" + self.build_address(withport = True)
		new_score = Score()
		try:
			timeout
			use_timeout = True
		except NameError:
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