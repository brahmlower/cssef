#!/usr/bin/python

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy.exc import NoSuchTableError
from datetime import datetime
import ConfigParser
import sys
from time import sleep
from random import randrange

class Database:
    def __init__(self, conf):
        if conf["type"] == "mysql":
            database_address = "%s://%s:%s@%s:%s/%s" % (conf["type"], \
                conf["user"], conf["password"], conf["address"], conf["port"], \
                conf["db"])
        elif conf["type"] == "sqlite":
            database_address = "%s:///%s" % (conf["type"], conf["file_path"])

        self.db = create_engine(database_address)
        self.md = MetaData(self.db)
        try:
            self.tb = self.tables_load(self.md)
        except NoSuchTableError:
            self.sync()
            self.tb = self.tables_load(self.md)

    def sync(self):
        tables = self.tables_define(self.md)
        self.tables_create(tables)
        sleep(1)

    def tables_define(self, md):
        scores = Table('scores', md,
            Column('datetime', DateTime),
            Column('compid', Integer),
            Column('teamid', Integer),
            Column('servid', Integer),
            Column('points', Integer)
        )
        tables = {}
        tables["scores"] = scores
        return tables

    def tables_load(self, md):
        tables = {}
        tables["scores"] = Table('scores', md, autoload=True)
        return tables

    def tables_create(self, tables_dict):
        for i in tables_dict:
            tables_dict[i].create()

    def new_score(self, comp_id, team_id, serv_id, points):
        insert = self.tb["scores"].insert()
        fields = {
            'datetime': datetime.now(),
            'compid': comp_id,
            'teamid': team_id,
            'servid': serv_id,
            'points': points
        }
        insert.execute(fields)

    def new_serv(self):
        insert = self.tb["services"].insert()
        fields = {
            ''
        }
        insert.execute(fields)

class Configuration:
    def __init__(self):
        self.general_config_path = "cssef.conf"
        self.teams_config_path = "teams.conf"
        self.pluggins_config_path = "pluggins.conf"

        self.general = self.general_conf()
        self.teams = self.teams_conf()
        self.pluggins = self.pluggins_conf()

    def general_conf(self):
        general = self.file_map(self.general_config_path)
        return general

    def pluggins_conf(self):
        tmp_pluggins = self.file_map(self.pluggins_config_path)
        pluggins = {}
        for i in tmp_pluggins:
            if tmp_pluggins[i]["enabled"] == "True":
                pluggins[i] = tmp_pluggins[i]
        return pluggins

    def teams_conf(self):
        teams = self.file_map(self.teams_config_path)
        return teams

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

class Comp:
    def __init__(self, comp_conf):
        self.id = comp_conf["comp_id"]

def log(db, comp, team, service, points):
    comp_id = comp.id
    team_id = team.id
    serv_id = service.id # Really, this should have a service id and service version
    db.new_score(comp_id, team_id, serv_id, points)
    print comp_id, team_id, serv_id, points

def pluggin_module(pluggin_obj):
    module_string = pluggin_obj["module"]
    module = __import__('pluggins.' + module_string, fromlist=[module_string])
    return getattr(module, module_string)(pluggin_obj)

def comp_factory(conf):
    return Comp(conf.general["competition"])

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

def run_loop(conf, db, comp, teams, services):
    condition = True
    while(condition):
        rand_sleep(conf)
        for i in services:
            for t in teams:
                points = i.score(t) # i.score() should return an integer, even if boolean result
                log(db, comp, t, i, points)

        # This is here just for testing!!
        break

def rand_sleep(conf):
    min_seconds = int(conf.general["scoring"]["min_seconds"])
    max_seconds = int(conf.general["scoring"]["max_seconds"])
    sleep_time = randrange(min_seconds, max_seconds)
    sleep(sleep_time)

def main():
    conf = Configuration()
    db = Database(conf.general["database"])
    comp = comp_factory(conf)
    teams = team_factory(conf)
    services = service_factory(conf)

    run_loop(conf, db, comp, teams, services)

main()