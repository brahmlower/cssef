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
from django.core.exceptions import ObjectDoesNotExist
from cssefwebfront.models import Competition
from cssefwebfront.models import Team
from cssefwebfront.models import Service
from cssefwebfront.models import Score
from cssefwebfront.models import Document

class ServiceModule:
    def __init__(self, serv_obj):
        # serv_obj is used in other locations (don't remove)
        self.serv_obj = serv_obj
        self.instance = self.load_pluggin(serv_obj)

    def load_pluggin(self, serv_obj):
        module_name = Document.objects.get(servicemodule = serv_obj.servicemodule).filename.split(".")[0]
        module = __import__(settings.CONTENT_PLUGGINS_PATH.replace('/','.')[1:] + module_name, fromlist=[module_name])
        return getattr(module, module_name)(serv_obj)

    def score(self, team_obj):
        score_obj = self.instance.score(team_obj)
        score_obj.datetime = timezone.now()
        return score_obj

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
    serv_list = []
    for i in serv_objs:
        serv_list.append(ServiceModule(i))
    return serv_list

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
        for serv in serv_list:
            for team_obj in team_list:
                # Build the score object
                score_obj = serv.score(team_obj)
                score_obj.compid = comp_obj.compid
                score_obj.teamid = team_obj.teamid
                score_obj.servid = serv.serv_obj.servid
                score_obj.datetime = timezone.now()
                # Save the score object
                score_obj.save()
                # Log the score object
                log(score_obj)
        rand_sleep(comp_obj.scoring_interval, comp_obj.scoring_interval_uncty)
    print "[INFO] Competition finished. Scoring stopped."

def run_comp(compid = None, compname = None):
    # Get the competition object based on provided input
    comp = LoadComp(compid = compid, compname = compname)
    # Check if scoring is enabled before continueing
    if not comp.scoring_enabled:
        sys.exit("[ERROR] Scoring is not enabled for this competition.")
    else:
        # Just checking the required fields are available
        if not comp.scoring_interval:
            sys.exit("[ERROR] Scoring is enabled, but 'scoring_interval' is invalid.")
        if not comp.scoring_interval_uncty:
            sys.exit("[ERROR] Scoring is enabled, but 'scoring_interval_uncty' is invalid.")
        # This will eventually need to check if it's a valid CIDR or domain name (todo)
        if not comp.scoring_method:
            sys.exit("[ERROR] Scoring is enabled, but 'scoring_method' is invalid.")
    teams = LoadTeams(comp.compid)
    servs = LoadServs(comp.compid)
    run_loop(comp, teams, servs)

def main():
    if len(sys.argv) == 1 or len(sys.argv) > 2:
        sys.exit("Usage:\n\t%s <competition id (integer)>\n\t%s <competition name (string)>" % (sys.argv[0], sys.argv[0]))
    if sys.argv[1].isdigit():
        run_comp(int(sys.argv[1]))
    else:
        run_comp(compname = sys.argv[1])

if __name__ == "__main__":
	main()
