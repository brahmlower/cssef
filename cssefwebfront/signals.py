from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from cssefwebfront.tasks import run_comp
from cssefwebfront.settings import logger
from cssefwebfront.models import Document
from cssefwebfront.models import Competition
import pytz
from hashlib import md5
import os


@receiver(pre_delete, sender = Document)
def delete_document(sender, **kwargs):
	# Read the file in
	instance = kwargs['instance']
	rfile = open(instance.filepath, 'r')
	content = rfile.read()
	rfile.close()
	# Get a hash of the file
	if instance.filehash != md5(content).hexdigest():
		print "[ERROR] Databased md5 did not match md5 of target file at '%s' for Document object id '%s'" % (instance.filepath, str(instance.docid))
	else:
		os.remove(instance.filepath)
