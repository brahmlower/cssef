from celery import task
from threading import Thread

def isSlaViolation(competition):
	slaThreashold = competition.scoringSlaThreashold
	lastScores = Score.objects.filter(competitionId = competition.competitionId,
		serviceId = serviceId, teamId = teamId).order_by('-scoreId')[:slaThreashold]
	if len(lastScores) < slaThreashold:
		return False
	for score in lastScores:
		if score.value > 0:
			return False
	return True

def scoreService(competition, service, team):
	print "Thread for scoring service '%s' for team '%s'" % (service.name, team.teamname)
	score = service.score(team)
	if score.value == 0 and competition.scoringSlaEnabled and isSlaViolation(competition):
		score.value = -1 * competition.scoringSlaPenalty
	score.save()

@task()
def startScoringCompetition(competition):
	print 'starting the scheduled competition'
	if not competition.scoringEnabled:
		# Scoring has been disabled for this competition - raise an error/log an error
		print "scoring has been disabled"
		return None
	while timezone.now() < competition.datetimeFinish:
		services = competition.getServices()
		teams = competition.getTeams()
		for service in services:
			for team in teams:
				scoreThread = Thread(target = scoreService, args = (competition, service, team))
				scoreThread.run()
		competition.sleepScoreInterval()
