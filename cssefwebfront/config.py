from django.apps import AppConfig
from os.path import isfile
import settings

class cssefwebfront_config(AppConfig):
	name = 'cssefwebfront'
	verbose_name = 'CSSEF Web Front'

	def ready(self):
		# Ensure '__init__.py' file lead to plugin directory
		cur_path = settings.BASE_DIR + "/"
		for i in settings.CONTENT_PLUGGINS_PATH.split("/"):
			if i != "" and not isfile(cur_path + "/__init__.py"):
				cur_path += i + "/"
				open(cur_path + "__init__.py", 'w').close()
