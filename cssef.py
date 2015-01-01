#!/usr/bin/python

import os
import sys
from time import sleep
from random import randrange
from django.utils import timezone
from json import loads as json_loads
import ConfigParser

# Required to use django models
os.environ['DJANGO_SETTINGS_MODULE'] = 'cssefwebfront.settings'
from django.conf import settings

from cssefwebfront.models import Competition
from cssefwebfront.models import Team
from cssefwebfront.models import Service
from cssefwebfront.models import Score
from cssefwebfront.models import Document

class Config:
    def __init__(self, config_path):
        self.general_config_path = config_path
        self.general = self.file_map()

    def file_map(self):
        dict1 = {}
        config_obj = self.load_file()
        for i in config_obj.sections():
            dict1[i] = self.section_map(config_obj, i)
        return dict1

    def load_file(self):
        conf = ConfigParser.ConfigParser()
        conf.readfp(open(self.general_config_path))
        return conf

    def section_map(self, config_obj, section):
        dict1 = {}
        options = config_obj.options(section)
        for option in options:
            try:
                dict1[option] = config_obj.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

class SetConfigurations():
    @staticmethod
    def dump_teams():
        team_objs = Team.objects.all()
        for i in team_objs:
            print i.teamid, i.teamname

    @staticmethod
    def dump_competitions():
        comp_objs = Competition.objects.all()
        for i in comp_objs:
            print i.compid, i.compname

    @staticmethod
    def dump_services():
        serv_objs = Service.objects.all()
        for i in serv_objs:
            print i.servid, i.name

    @staticmethod
    def delete(table, obj_id):
        if table == "team":     db_obj = Team.objects.get(teamid = obj_id)
        elif table == "comp":   db_obj = Competition.objects.get(compid = obj_id)
        elif table == "serv":   db_obj = Service.objects.get(servid = obj_id)
        db_obj.save()

    @staticmethod
    def edit(table, obj_id, arg_list):
        if table == "team":     db_obj = Team.objects.get(teamid = obj_id)
        elif table == "comp":   db_obj = Competition.objects.get(compid = obj_id)
        elif table == "serv":   db_obj = Service.objects.get(servid = obj_id)
        for i in args_list:
            x = i.split("=")
            db_obj[x[0]] = x[1]
        db_obj.save()

    @staticmethod
    def create(table, args_list):
        args_dict = arg_list_dict(args_list)
        if table == "team":     db_obj = Team(**args_dict)
        elif table == "comp":   db_obj = Competition(**args_dict)
        elif table == "serv":   db_obj = Service(**args_dict)
        db_obj.save()

class ServiceModule:
    def __init__(self, serv_obj):
        self.serv_obj = serv_obj
        self.instance = self.load_pluggin(serv_obj)

    def load_pluggin(self, serv_obj):
        module_name = Document.objects.get(servicemodule = serv_obj.servicemodule).filename.split(".")[0]
        module = __import__('pluggins.' + module_name, fromlist=[module_name])
        return getattr(module, module_name)(serv_obj)

    def score(self, team_obj):
        score_obj = self.instance.score(team_obj, self.serv_obj.name)
        score_obj.datetime = timezone.now()
        return score_obj

def LoadComp(compid):
    try:
        comp_obj = Competition.objects.get(compid = compid)
        return comp_obj
    except:
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

def arg_list_dict(args):
    value_dict = {}
    for i in args:
        x = i.split("=")
        if len(x) != 2:
            sys.exit("Argument parsing error, bad argument: '%s'" % i)
        value_dict[x[0]] = x[1]
    return value_dict

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

def run_loop(comp, team_list, serv_list):
    condition = True
    while(condition):
        rand_sleep(comp.score_delay, comp.score_delay_uncert)
        for serv in serv_list:
            for team in team_list:
                # Build the score object
                score_obj = serv.score(team)
                score_obj.compid = comp.compid
                score_obj.teamid = team.teamid
                score_obj.servid = serv.serv_obj.servid
                score_obj.datetime = timezone.now()
                # Save the score object
                score_obj.save()
                # Log the score object
                log(score_obj)
        #break #This is here just for testing!!

def manage():
    if sys.argv[1] in ["team", "competition", "service"] and len(sys.argv) == 2:
        sys.exit("Did not match {dump|delete|create}")
    if sys.argv[1] == "team":
        if sys.argv[2] == "dump":
            SetConfigurations.dump_teams()
        elif sys.argv[2] == "delete":
            SetConfigurations.delete("team", sys.argv[3])
        elif sys.argv[2] == "create":
            SetConfigurations.create("team", sys.argv[3:])
        elif sys.argv[2] == "edit":
            SetConfigurations.create("team", sys.argv[3:])
    elif sys.argv[1] == "competition":
        if sys.argv[2] == "dump":
            SetConfigurations.dump_competitions()
        elif sys.argv[2] == "delete":
            SetConfigurations.delete("comp", sys.argv[3])
        elif sys.argv[2] == "create":
            SetConfigurations.create("comp", sys.argv[3:])
        elif sys.argv[2] == "edit":
            SetConfigurations.create("comp", sys.argv[3:])
    elif sys.argv[1] == "service":
        if sys.argv[2] == "dump":
            SetConfigurations.dump_services()
        elif sys.argv[2] == "delete":
            SetConfigurations.delete("serv", sys.argv[3])
        elif sys.argv[2] == "create":
            SetConfigurations.create("serv", sys.argv[3:])
        elif sys.argv[2] == "edit":
            SetConfigurations.create("serv", sys.argv[3:])

def run_comp(compid):
    comp = LoadComp(compid)
    teams = LoadTeams(compid)
    servs = LoadServs(compid)
    run_loop(comp, teams, servs)

def main():
    config = Config("cssef.conf")
    if len(sys.argv) == 1:
        sys.exit("Must provide an action {run|team|competition|service}")
    if sys.argv[1] != "run":
        manage()
    if len(sys.argv) != 3:
        sys.exit("Usage: %s run <competition id>" % sys.argv[0])
    try:
        compid = int(sys.argv[2])
    except:
        sys.exit("Competition ID must be an integer.")
    run_comp(compid)

if __name__ == "__main__":
	main()
