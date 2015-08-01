# This runs the entire service, and will be the backbone after splitting away from Web API
from celery import task
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from models import Competition
from ScoringEngine import startScoringCompetition

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