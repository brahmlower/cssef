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

class Load:
    @staticmethod
    def comp(compid):
        try:
            comp_obj = Competition.objects.get(compid = compid)
            return comp_obj
        except:
            sys.exit("No competition with id: '%s'" % str(compid))

    @staticmethod
    def teams(compid):
        try:
            team_objs = Team.objects.filter(compid = compid)
            return team_objs
        except:
            sys.exit("No teams were associated with competition with id '%s' in table 'teams'" % str(compid))

    @staticmethod
    def servs(compid):
        try:
            serv_objs = Service.objects.filter(compid = compid)
        except:
            sys.exit("No services were associated with competition with id '%s' in table 'services'" % str(compid))
        serv_list = []
        for i in serv_objs:
            serv_list.append(ServiceModule(i))
        return serv_list

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
    def __init__(self, db_obj):
        self.db_obj = db_obj
        # try:
        self.config_json = json_loads(db_obj.config)
        # except ValueError, e:
        #     sys.exit("Error parsing configuration json object:\n%s" % db_obj.config)
        self.config_json["name"] = self.db_obj.name
        self.config_json["points"] = self.db_obj.points
	self.config_json["subdomain"] = self.db_obj.subdomain
        self.instance = self.load_pluggin()

    def load_pluggin(self):
        module_name = self.db_obj.module
        module = __import__('pluggins.' + module_name, fromlist=[module_name])
        return getattr(module, module_name)(self.config_json)

    def score(self, team_obj):
        return self.instance.score(team_obj)

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

def log(comp, team, serv, points):
    value_dict = {
        "compid": comp.compid,
        "teamid": team.teamid,
        "servid": serv.db_obj.servid,
        "datetime": timezone.now(),
        "value": points
    }
    new_score = Score(**value_dict)
    new_score.save()

def run_loop(comp, teams, servs):
    condition = True
    while(condition):
        rand_sleep(comp.score_delay, comp.score_delay_uncert)
        for i in servs:
            for t in teams:
                log(comp, t, i, i.score(t))
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

def main():
    config = Config("cssef.conf")
    if len(sys.argv) == 1:
        sys.exit("Must provide an action {run|team|competition|service}")
    if sys.argv[1] != "run":
        manage()
    else:
        compid = 1 #Temporarily hardcoded competition id
        comp = Load.comp(compid)
        teams = Load.teams(compid)
        servs = Load.servs(compid)
        run_loop(comp, teams, servs)

if __name__ == "__main__":
	main()
