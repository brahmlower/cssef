# Imports required for django modules
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cssefwebfront.settings'
from django.conf import settings

# Imports required for base pluggin
from cssefwebfront.models import Score
from ScoringUtils import Pluggin
from ScoringUtils import PlugginTest
import json

# Imports required for specific pluggin
import socket

class OpenPort(Pluggin):
    team_config_type_dict = {
        "port": int,
        "network": str,
        "timeout": int
    }
    def __init__(self, conf_dict):
        Pluggin.__init__(self, conf_dict)

    def score(self, service_name):
        team_config = json.loads(team.score_configs)[service_name]
        address = self.build_address(team_config)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(team_config["timeout"])
        result = sock.connect_ex((address, team_config["port"]))
        new_score = Score()
        if result == 0:
            new_score.value = self.points
            new_score.message = ""
        else:
            new_score.value = 0
            new_score.message = "" # TODO: Could eventually use an error message here
        return new_score

class Test(PlugginTest):
    def __init__(self):
        PlugginTest.__init__(self, OpenPort)
