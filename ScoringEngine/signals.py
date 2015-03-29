from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from models import Competition
from ScoringEngine import startScoringCompetition

@receiver(post_save, sender = Competition)
def scheduleCompetitionStart(sender, **kwargs):
	if sender.autoStart:
		deltaUntilStart = sender.datetimeStart - timezone.now()
		secondsUntilStart = int(deltaUntilStart.seconds)
		result = startScoringCompetition.apply_async((sender,), countdown = secondsUntilStart)
		print 'finished scheduling the competition'