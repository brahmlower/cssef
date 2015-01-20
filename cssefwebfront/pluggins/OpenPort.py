# Imports required for django modules
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cssefwebfront.settings'
from django.conf import settings

# Imports required for base pluggin
from cssefwebfront.models import Score
from cssefwebfront.ScoringUtils import Pluggin
from cssefwebfront.ScoringUtils import PlugginTest
import json

# Imports required for specific pluggin
import socket

class OpenPort(Pluggin):
    team_config_type_dict = {
        "port": int,
        "timeout": int
    }
    def __init__(self, service_obj):
        Pluggin.__init__(self, service_obj)

    def score(self, team_obj):
        self.update_configuration(team_obj)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        result = sock.connect_ex((self.build_address(), self.port))
        new_score = Score()
        if result == 0:
            new_score.value = self.points
            new_score.message = ""
        else:
            new_score.value = 0
            new_score.message = "" # TODO: Could eventually use an error message here
        return new_score