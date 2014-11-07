#!/usr/bin/python

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import delete
from sqlalchemy.exc import NoSuchTableError
from datetime import datetime
from json import loads as json_loads
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
        services = Table('services', md,
            Column('id', Integer),
            Column('compid', Integer),
            Column('name', String(20)),
            Column('module', String(20)),
            Column('version', Integer),
            Column('release', Integer),
            Column('config', String(1000)),
        )
        competitions = Table('competitions', md,
            Column('compid', Integer),
            Column('compname', String(50)),
            Column('compurlid', String(25)),
            Column('snippet', String(300)),
            Column('description', String(1000)),
            Column('viewable', Boolean),
            Column('autodisplay', Boolean),
            Column('displaytime', Integer),
        )
        teams = Table('teams', md,
            Column('teamid', Integer),
            Column('compid', Integer),
            Column('cidr', String(18)),
            Column('teamname', String(20)),
        )

        tables = {}
        tables["scores"] = scores
        tables["services"] = services
        tables["competitions"] = competitions
        tables["teams"] = teams
        return tables

    def tables_load(self, md):
        tables = {}
        tables["scores"] = Table('scores', md, autoload=True)
        tables["services"] = Table('services', md, autoload=True)
        tables["competitions"] = Table('competitions', md, autoload=True)
        tables["teams"] = Table('teams', md, autoload=True)
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

    # def new_serv(self):
    #     insert = self.tb["services"].insert()
    #     fields = {
    #         ''
    #     }
    #     insert.execute(fields)

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
    def __init__(self, db_row_result):
        self.id = db_row_result.teamid
        self.name = db_row_result.teamname
        self.cidr = db_row_result.cidr

class Comp:
    def __init__(self, db_row_result):
        self.id = db_row_result.compid

def log(db, comp, team, service, points):
    comp_id = comp.id
    team_id = team.id
    serv_id = service.id # Really, this should have a service id and service version
    db.new_score(comp_id, team_id, serv_id, points)
    print comp_id, team_id, serv_id, points

def pluggin_module(db_row_result):
    # pluggins are named like "plugginname_versionnum_releasenum.py"
    module_string = db_row_result.module#"%s_%s_%s" % (db_row_result.module, db_row_result.version, db_row_result.release)
    class_string = db_row_result.module
    print db_row_result.config
    config_json = json_loads(db_row_result.config)
    #module_string = pluggin_obj["module"]
    module = __import__('pluggins.' + module_string, fromlist=[class_string])
    return getattr(module, class_string)(config_json)

def comp_factory(db, compid):
    selection = db.tb["competitions"].select(db.tb["competitions"].c.compid == compid)
    result = selection.execute()
    rows = result.fetchall()
    if len(rows) == 0:
        sys.exit("No competitions matching '%s' in table 'competitions'" % str(compid))
    if len(rows) > 1:
        sys.exit("More than one competition entry with id '%s' in table 'competitions'" % str(compid))
    return Comp(rows[0])

def team_factory(db, compid):
    selection = db.tb["teams"].select(db.tb["teams"].c.compid == compid)
    result = selection.execute()
    rows = result.fetchall()
    if len(rows) == 0:
        sys.exit("No teams were associated with competition with id '%s' in table 'teams'" % str(compid))
    teamlist = []
    for i in rows:
        teamlist.append(Team(i))
    return teamlist

def service_factory(db, compid):
    selection = db.tb["services"].select(db.tb["services"].c.compid == compid)
    result = selection.execute()
    rows = result.fetchall()
    if len(rows) == 0:
        sys.exit("No services were associated with competition with id '%s' in table 'services'" % str(compid))
    service_list = []
    for i in rows:
        service_list.append(pluggin_module(i))
        #service_list.append(pluggin_module(conf.pluggins[i]))
    return service_list

def run_loop(conf, db, comp, teams, services):
    condition = True
    while(condition):
        rand_sleep(conf)
        for i in services:
            for t in teams:
                points = i.score(t)
                log(db, comp, t, i, points)

        # This is here just for testing!!
        break

def rand_sleep(conf):
    min_seconds = int(conf.general["scoring"]["min_seconds"])
    max_seconds = int(conf.general["scoring"]["max_seconds"])
    sleep_time = randrange(min_seconds, max_seconds)
    sleep(sleep_time)

class SetConfigurations():
    @staticmethod
    def dump_teams(db):
        selection = db.tb["teams"].select()
        result = selection.execute()
        rows = result.fetchall()

        for i in rows:
            print i

    @staticmethod
    def delete_team(db, teamid):
        d = delete(db.tb["teams"], db.tb["teams"].c.teamid == teamid)
        db.db.execute(d)

    @staticmethod
    def create_team(db, args_list):
        vals = {}
        for i in args_list:
            x = i.split("=")
            vals[x[0]] = x[1]
        insert = db.tb["teams"].insert()
        insert.execute(vals)

    @staticmethod
    def dump_competitions(db):
        selection = db.tb["competitions"].select()
        result = selection.execute()
        rows = result.fetchall()

        for i in rows:
            print i

    @staticmethod
    def delete_competitions(db, compid):
        d = delete(db.tb["competitions"], db.tb["competitions"].c.compid == compid)
        db.db.execute(d)

    @staticmethod
    def create_competition(db, args_list):
        vals = {}
        for i in args_list:
            x = i.split("=")
            vals[x[0]] = x[1]
        insert = db.tb["competitions"].insert()
        insert.execute(vals)

    @staticmethod
    def dump_services(db):
        selection = db.tb["services"].select()
        result = selection.execute()
        rows = result.fetchall()

        for i in rows:
            print i

    @staticmethod
    def delete_service(db, serviceid):
        d = delete(db.tb["services"], db.tb["services"].c.id == serviceid)
        db.db.execute(d)

    @staticmethod
    def create_service(db, args_list):
        vals = {}
        for i in args_list:
            x = i.split("=")
            vals[x[0]] = x[1]
        insert = db.tb["services"].insert()
        insert.execute(vals)

def db_configuration(db):
    if sys.argv[2] == "team":
        if sys.argv[3] == "dump":
            SetConfigurations.dump_teams(db)
        elif sys.argv[3] == "delete":
            SetConfigurations.delete_team(db, sys.argv[4])
        elif sys.argv[3] == "create":
            SetConfigurations.create_team(db, sys.argv[4:])
        else:
            print "Did not match {dump|delete|create}"
    elif sys.argv[2] == "competition":
        if sys.argv[3] == "dump":
            SetConfigurations.dump_competitions(db)
        elif sys.argv[3] == "delete":
            SetConfigurations.delete_competitions(db, sys.argv[4])
        elif sys.argv[3] == "create":
            SetConfigurations.create_competition(db, sys.argv[4:])
        else:
            print "Did not match {dump|delete|create}"
    elif sys.argv[2] == "service":
        if sys.argv[3] == "dump":
            SetConfigurations.dump_services(db)
        elif sys.argv[3] == "delete":
            SetConfigurations.delete_service(db, sys.argv[4])
        elif sys.argv[3] == "create":
            SetConfigurations.create_service(db, sys.argv[4:])
        else:
            print "Did not match {dump|delete|create}"
    else:
        print "Did not match {team|competition|service}"

def main():
    conf = Configuration()
    db = Database(conf.general["database"])
    try:
        if sys.argv[1] == "config":
            db_configuration(db)
    except IndexError:
        comp = comp_factory(db, 1001) # Temporarily hardcoded competition id
        teamlist = team_factory(db, comp.id)
        services = service_factory(db, comp.id)

        run_loop(conf, db, comp, teamlist, services)

main()