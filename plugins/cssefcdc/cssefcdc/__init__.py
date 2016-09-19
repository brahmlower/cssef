from cssefserver import Plugin
from cssefcdc import tasks

class CyberDefenseCompetition(Plugin):
    name = "Cyber Defense Competition"
    short_name = "CDC"
    __version__ = "0.0.1"
    endpoints = [
        tasks.CompetitionAdd,
        tasks.CompetitionDel,
        tasks.CompetitionSet,
        tasks.CompetitionGet,
        tasks.TeamAdd,
        tasks.TeamDel,
        tasks.TeamSet,
        tasks.TeamGet,
        tasks.ScoreAdd,
        tasks.ScoreDel,
        tasks.ScoreSet,
        tasks.ScoreGet,
        tasks.InjectAdd,
        tasks.InjectDel,
        tasks.InjectSet,
        tasks.InjectGet,
        tasks.InjectResponseAdd,
        tasks.InjectResponseDel,
        tasks.InjectResponseSet,
        tasks.InjectResponseGet,
        tasks.IncidentAdd,
        tasks.IncidentDel,
        tasks.IncidentSet,
        tasks.IncidentGet,
        tasks.IncidentResponseAdd,
        tasks.IncidentResponseDel,
        tasks.IncidentResponseSet,
        tasks.IncidentResponseGet,
        tasks.ScoringEngineAdd,
        tasks.ScoringEngineDel,
        tasks.ScoringEngineSet,
        tasks.ScoringEngineGet
    ]
