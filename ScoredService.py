import ConfigParser

class ScoredService:
    def __init__(self, serv_name, serv_id):
        self.serv_name = serv_name
        self.serv_id = serv_id

    def load_config(self, config_path):
        conf = ConfigParser.ConfigParser()
        conf.readfp(open(self.config_path))
        return conf
