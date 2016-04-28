from cssefserver.api import Plugin
from cssefcdc import tasks

class CyberDefenseCompetition(Plugin):
    endpoint_list = [
        (tasks.CompetitionAdd, 'competitionadd'),
        (tasks.CompetitionDel, 'competitiondel'),
        (tasks.CompetitionSet, 'competitionset'),
        (tasks.CompetitionGet, 'competitionget'),
        (tasks.TeamAdd, 'teamadd'),
        (tasks.TeamDel, 'teamdel'),
        (tasks.TeamSet, 'teamset'),
        (tasks.TeamGet, 'teamget'),
        (tasks.ScoreAdd, 'scoreadd'),
        (tasks.ScoreDel, 'scoredel'),
        (tasks.ScoreSet, 'scoreset'),
        (tasks.ScoreGet, 'scoreget'),
        (tasks.InjectAdd, 'injectadd'),
        (tasks.InjectDel, 'injectdel'),
        (tasks.InjectSet, 'injectset'),
        (tasks.InjectGet, 'injectget'),
        (tasks.InjectResponseAdd, 'injectresponseadd'),
        (tasks.InjectResponseDel, 'injectresponsedel'),
        (tasks.InjectResponseSet, 'injectresponseset'),
        (tasks.InjectResponseGet, 'injectresponseget'),
        (tasks.IncidentAdd, 'incidentadd'),
        (tasks.IncidentDel, 'incidentdel'),
        (tasks.IncidentSet, 'incidentset'),
        (tasks.IncidentGet, 'incidentget'),
        (tasks.IncidentResponseAdd, 'incdientresponseadd'),
        (tasks.IncidentResponseDel, 'incdientresponsedel'),
        (tasks.IncidentResponseSet, 'incdientresponseset'),
        (tasks.IncidentResponseGet, 'incdientresponseget'),
        (tasks.ScoringEngineAdd, 'scoringengineadd'),
        (tasks.ScoringEngineDel, 'scoringenginedel'),
        (tasks.ScoringEngineSet, 'scoringengineset'),
        (tasks.ScoringEngineGet, 'scoringengineget')
    ]
    def __init__(self, config):
        self.config = config
