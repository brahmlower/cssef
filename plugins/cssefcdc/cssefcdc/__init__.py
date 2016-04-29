from cssefserver import Plugin
from cssefcdc import tasks

class CyberDefenseCompetition(Plugin):
    endpoints = [
        tasks.CompetitionAdd.info_dict(),
        tasks.CompetitionDel.info_dict(),
        tasks.CompetitionSet.info_dict(),
        tasks.CompetitionGet.info_dict(),
        tasks.TeamAdd.info_dict(),
        tasks.TeamDel.info_dict(),
        tasks.TeamSet.info_dict(),
        tasks.TeamGet.info_dict(),
        tasks.ScoreAdd.info_dict(),
        tasks.ScoreDel.info_dict(),
        tasks.ScoreSet.info_dict(),
        tasks.ScoreGet.info_dict(),
        tasks.InjectAdd.info_dict(),
        tasks.InjectDel.info_dict(),
        tasks.InjectSet.info_dict(),
        tasks.InjectGet.info_dict(),
        tasks.InjectResponseAdd.info_dict(),
        tasks.InjectResponseDel.info_dict(),
        tasks.InjectResponseSet.info_dict(),
        tasks.InjectResponseGet.info_dict(),
        tasks.IncidentAdd.info_dict(),
        tasks.IncidentDel.info_dict(),
        tasks.IncidentSet.info_dict(),
        tasks.IncidentGet.info_dict(),
        tasks.IncidentResponseAdd.info_dict(),
        tasks.IncidentResponseDel.info_dict(),
        tasks.IncidentResponseSet.info_dict(),
        tasks.IncidentResponseGet.info_dict(),
        tasks.ScoringEngineAdd.info_dict(),
        tasks.ScoringEngineDel.info_dict(),
        tasks.ScoringEngineSet.info_dict(),
        tasks.ScoringEngineGet.info_dict()
    ]
    def __init__(self, config):
        self.config = config
