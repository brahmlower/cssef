#!/usr/bin/python

import ConfigParser
import sys
from time import sleep
from random import randrange

class Configuration:
    def __init__(self):
        #self.general_config_path = "general.conf"
        self.teams_config_path = "teams.conf"
        self.pluggins_config_path = "pluggins.conf"

        #self.general = self.file_map(self.general_config_path)
        self.teams = self.file_map(self.teams_config_path)
        self.pluggins = self.file_map(self.pluggins_config_path)

    def file_map(self, config_path):
        dict1 = {}
        config_obj = self.load_file(config_path)
        for i in config_obj.sections():
            dict1[i] = self.section_map(config_obj, i)
        return dict1

    def load_file(self, config_path):
        conf = ConfigParser.ConfigParser()
        conf.readfp(open(config_path))
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

class Team:
    list = []
    def __init__(self, team_conf):
        self.id = team_conf["id"]
        self.name = team_conf["name"]
        self.net_addr = team_conf["net_addr"]

def log(team, service, status):
    if status:
        print "Service '%s' for team '%s' was marked 'up'." % (service,team)
    else:
        print "Service '%s' for team '%s' was marked 'down'." % (service,team)

def pluggin_module(pluggin_obj):
    module_string = pluggin_obj["module"]
    module = __import__('pluggins.' + module_string, fromlist=[module_string])
    return getattr(module, module_string)(pluggin_obj)

def team_factory(conf):
    teams_list = []
    for i in conf.teams:
        teams_list.append(Team(conf.teams[i]))
    return teams_list

def service_factory(conf):
    service_list = []
    for i in conf.pluggins:
        service_list.append(pluggin_module(conf.pluggins[i]))
    return service_list

def run_loop(teams, services):
    condition = True
    while(condition):
        #sleep(rand_time_range())
        for i in services:
            for t in teams:
                result = i.score(t)
                log(t.name, i.name, result)
        break

def rand_time_range():
    sleep_time = randrange(180,300)
    sleep(sleep_time)

def main():
    conf = Configuration()
    teams = team_factory(conf)
    services = service_factory(conf)

    run_loop(teams, services)

main()