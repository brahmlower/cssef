from cssefserver.framework.utils import databaseConnection
from cssefserver.framework.utils import handleException
from cssefserver.framework.utils import getEmptyReturnDict
from cssefserver.framework.utils import modelDel
from cssefserver.framework.utils import modelSet
from cssefserver.framework.utils import modelGet
from cssefserver.framework import CssefCeleryApp
from cssefserver.framework import dbPath
from cssefserver.modules.organization import Organization
from cssefserver.modules.user import User

@task()
def startScoringCompetition(competition):
	# This function is only called if scoring is enabled for the competition
	print 'starting the scheduled competition'
	thread = Thread(target = competition.startScoring, args = ())
	thread.start()
	thread.join()
	print "thread finished...exiting"

@receiver(post_save, sender = Competition)
def scheduleCompetitionStart(sender, **kwargs):
	if sender.autoStart:
		deltaUntilStart = sender.datetimeStart - timezone.now()
		secondsUntilStart = int(deltaUntilStart.seconds)
		result = startScoringCompetition.apply_async((sender,), countdown = secondsUntilStart)
		print 'finished scheduling the competition'