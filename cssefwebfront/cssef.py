#!/usr/bin/python

# Required to use django models
import os
import django 
os.environ['DJANGO_SETTINGS_MODULE'] = 'cssefwebfront.settings'
django.setup()
from cssefwebfront import settings

import sys
from time import sleep
from random import randrange
from django.utils import timezone
from cssefwebfront.settings import logger
from django.core.exceptions import ObjectDoesNotExist
from cssefwebfront.models import Competition
from cssefwebfront.models import Team
from cssefwebfront.models import Service
from cssefwebfront.models import Score
from cssefwebfront.models import Document

def LoadComp(compid = None, compname = None):
    try:
        if compid != None:
            return Competition.objects.get(compid = compid)
        elif compid == None and compname != None:
            return Competition.objects.get(compname = compname)
        else:
            sys.exit("LoadComp: Must provide either 'compid' or 'compname'.")
    except ObjectDoesNotExist:
        sys.exit("No competition with id: '%s'" % str(compid))

def LoadTeams(compid):
    try:
        team_objs = Team.objects.filter(compid = compid)
        return team_objs
    except:
        sys.exit("No teams were associated with competition with id '%s' in table 'teams'" % str(compid))

def LoadServs(compid):
    try:
        serv_objs = Service.objects.filter(compid = compid)
    except:
        sys.exit("No services were associated with competition with id '%s' in table 'services'" % str(compid))
    return serv_objs

def rand_sleep(score_delay, score_delay_uncert):
    min_seconds = score_delay - score_delay_uncert
    max_seconds = score_delay + score_delay_uncert
    sleep_time = randrange(min_seconds, max_seconds)
    print "[INFO] Sleeping for %s seconds." % str(sleep_time)
    sleep(sleep_time)

def log(score_obj):
    # Temporary logging
    print "[SCORE] (%s) Team:%s Service:%s Value:%s Messages:%s" % \
        (score_obj.datetime, score_obj.teamid, score_obj.servid, score_obj.value, score_obj.message)

def run_loop(comp_obj, team_list, serv_list):
    if timezone.now() < comp_obj.datetime_start:
        time_until_start = (comp_obj.datetime_start - timezone.now()).total_seconds()
        print "[INFO] Waiting until competition starts: ~%s seconds" % str(int(time_until_start))
        sleep(time_until_start)
    while timezone.now() < comp_obj.datetime_finish:
        for serv_obj in serv_list:
            for team_obj in team_list:
                # Build the score object
                score_obj = serv_obj.score(team_obj)
                score_obj.compid = comp_obj.compid
                score_obj.teamid = team_obj.teamid
                score_obj.servid = serv_obj.servid
                score_obj.datetime = timezone.now()
                # Save the score object
                score_obj.save()
                # Log the score object
                log(score_obj)
        rand_sleep(comp_obj.scoring_interval, comp_obj.scoring_interval_uncty)
    print "[INFO] Competition finished. Scoring stopped."

def run_comp(compid = None, compname = None):
    logger.debug("Scoring engine execution has started.")
    # Get the competition object based on provided input
    comp_obj = LoadComp(compid = compid, compname = compname)
    # Check if the competition hasn't passed
    if timezone.now() >= comp_obj.datetime_finish:
        logger.debug("[ERROR] This competition cannot be started. It has already finished.")
        return "[ERROR] This competition cannot be started. It has already finished."
    # Check if scoring is enabled before continuing
    if not comp_obj.scoring_enabled:
        logger.debug("[ERROR] Scoring is not enabled for this competition.")
        return "[ERROR] Scoring is not enabled for this competition."
    else:
        # Just checking the required fields are available
        if not comp_obj.scoring_interval:
            logger.debug("[ERROR] Scoring is enabled, but 'scoring_interval' is invalid.")
            return "[ERROR] Scoring is enabled, but 'scoring_interval' is invalid."
        if not comp_obj.scoring_interval_uncty:
            logger.debug("[ERROR] Scoring is enabled, but 'scoring_interval_uncty' is invalid.")
            return "[ERROR] Scoring is enabled, but 'scoring_interval_uncty' is invalid."
        # This will eventually need to check if it's a valid CIDR or domain name (todo)
        if not comp_obj.scoring_method:
            logger.debug("[ERROR] Scoring is enabled, but 'scoring_method' is invalid.")
            return "[ERROR] Scoring is enabled, but 'scoring_method' is invalid."
    teams = LoadTeams(comp_obj.compid)
    servs = LoadServs(comp_obj.compid)
    run_loop(comp_obj, teams, servs)
    return None

def main():
    if len(sys.argv) == 1 or len(sys.argv) > 2:
        sys.exit("Usage:\n\t%s <competition id (integer)>\n\t%s <competition name (string)>" % (sys.argv[0], sys.argv[0]))
    if sys.argv[1].isdigit():
        run_comp(int(sys.argv[1]))
    else:
        run_comp(compname = sys.argv[1])

if __name__ == "__main__":
	ret_val = main()
	if ret_val != None:
		sys.exit(ret_val)
