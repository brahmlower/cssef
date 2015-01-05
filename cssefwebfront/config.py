from django.apps import AppConfig
import settings

class cssefwebfront_config(AppConfig):
	name = 'cssefwebfront'
	verbose_name = 'CSSEF Web Front'

	def ready(self):
		# Ensure '__init__.py' file lead to pluggin directory
		cur_path = settings.BASE_DIR + "/"
		for i in settings.CONTENT_PLUGGINS_PATH.split("/"):
			if i != "":
				cur_path += i + "/"
				open(cur_path + "__init__.py", 'w').close()

		# Import the signals handler as was done here: http://chriskief.com/2014/02/28/django-1-7-signals-appconfig/
		# Not really sure if this is the best way to do it...
		from cssefwebfront import signals
		

