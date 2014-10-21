from ScoredService import ScoredService
import socket

class OpenPort(ScoredService):
    def __init__(self, conf_dict):
        self.name = conf_dict["name"]
        self.port = int(conf_dict["port"])
        self.socket_timeout = int(conf_dict["socket_timeout"])

    def score(self, team):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Sets low timeout otherwise scoring will take FOREVER
        sock.settimeout(self.socket_timeout)
        result = sock.connect_ex((team.net_addr, self.port))
        if result == 0:
            return True
        else:
            return False