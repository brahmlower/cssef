from django.apps import AppConfig
import settings

class cssefwebfront(AppConfig):
	name = 'cssefwebfront'
	verbose_name = 'CSSEF Web Front'

	def ready(self):
		# Ensure '__init__.py' file lead to pluggin directory
		cur_path = settings.BASE_DIR + "/"
		for i in settings.CONTENT_PLUGGINS_PATH.split("/"):
			if i != "":
				cur_path += i + "/"
				open(cur_path + "__init__.py", 'w').close()
