from cssefserver.errors import CssefException
from cssefserver.utils import CssefRPCEndpoint
from cssefserver.utils import get_empty_return_dict
from cssefserver.taskutils import model_del
from cssefserver.taskutils import model_set
from cssefserver.taskutils import model_get
from cssefserver.account.utils import authorize_access
from cssefcdc.api import Competition
from cssefcdc.api import Team
from cssefcdc.api import Score
from cssefcdc.api import Inject
from cssefcdc.api import InjectResponse
from cssefcdc.api import Incident
from cssefcdc.api import IncidentResponse
from cssefcdc.api import ScoringEngine

# ==================================================
# Competition Endpoints
# ==================================================
class CompetitionAdd(CssefRPCEndpoint):
    onRequestArgs = ['auth']
    def on_request(self, auth, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        competition = Competition.from_dict(self.database_connection, kwargs)
        return_dict = get_empty_return_dict()
        return_dict['content'].append(competition.as_dict())
        return return_dict

class CompetitionDel(CssefRPCEndpoint):
    takesKwargs = False
    onRequestArgs = ['auth', 'pkid']
    def on_request(self, auth, pkid):
        authorize_access(self.database_connection, auth, self.config)
        return model_del(Competition, self.database_connection, pkid)

class CompetitionSet(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'pkid']
    def on_request(self, auth, pkid, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_set(Competition, self.database_connection, pkid, **kwargs)

class CompetitionGet(CssefRPCEndpoint):
    onRequestArgs = ['auth']
    def on_request(self, auth, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_get(Competition, self.database_connection, **kwargs)

class CompetitionStart(CssefRPCEndpoint):
    takesKwargs = False
    onRequestArgs = ['auth', 'pkid']
    def on_request(self, auth, pkid):
        authorize_access(self.database_connection, auth, self.config)
        competition = Competition.from_database(self.database_connection, pkid)
        competition.start()

# ==================================================
# Team Endpoints
# ==================================================
class TeamAdd(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        competition_obj = Competition.from_database(self.database_connection, competition)
        kwargs['competition'] = competition_obj.get_id()
        team = Team.from_dict(self.database_connection, kwargs)
        return_dict = get_empty_return_dict()
        return_dict['content'].append(team.as_dict())
        return return_dict

class TeamDel(CssefRPCEndpoint):
    takesKwargs = False
    onRequestArgs = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid):
        authorize_access(self.database_connection, auth, self.config)
        return model_del(Team, self.database_connection, pkid)

class TeamSet(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_set(Team, self.database_connection, pkid, **kwargs)

class TeamGet(CssefRPCEndpoint):
    onRequestArgs = ['auth' 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_get(Team, self.database_connection, **kwargs)

# ==================================================
# Score Endpoints
# ==================================================
class ScoreAdd(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        competition_obj = Competition.from_database(self.database_connection, competition)
        kwargs['competition'] = competition_obj.get_id()
        score = Score.from_dict(self.database_connection, kwargs)
        return_dict = get_empty_return_dict()
        return_dict['content'].append(score.as_dict())
        return return_dict

class ScoreDel(CssefRPCEndpoint):
    takesKwargs = False
    onRequestArgs = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid):
        authorize_access(self.database_connection, auth, self.config)
        return model_del(Score, self.database_connection, pkid)

class ScoreSet(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_set(Score, self.database_connection, pkid, **kwargs)

class ScoreGet(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_get(Score, self.database_connection, **kwargs)

# ==================================================
# Inject Endpoints
# ==================================================
class InjectAdd(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        competition_obj = Competition.from_database(self.database_connection, competition)
        kwargs['competition'] = competition_obj.get_id()
        inject = Inject.from_dict(self.database_connection, kwargs)
        return_dict = get_empty_return_dict()
        return_dict['content'].append(inject.as_dict())
        return return_dict

class InjectDel(CssefRPCEndpoint):
    takesKwargs = False
    onRequestArgs = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid):
        authorize_access(self.database_connection, auth, self.config)
        return model_del(Inject, self.database_connection, pkid)

class InjectSet(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_set(Inject, self.database_connection, pkid, **kwargs)

class InjectGet(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_get(Inject, self.database_connection, **kwargs)

# ==================================================
# Inject Response Endpoints
# ==================================================
class InjectResponseAdd(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        competition_obj = Competition.from_database(self.database_connection, competition)
        kwargs['competition'] = competition_obj.get_id()
        injectResponse = InjectResponse.from_dict(self.database_connection, kwargs)
        return_dict = get_empty_return_dict()
        return_dict['content'].append(injectResponse.as_dict())
        return return_dict

class InjectResponseDel(CssefRPCEndpoint):
    takesKwargs = False
    onRequestArgs = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid):
        authorize_access(self.database_connection, auth, self.config)
        return model_del(InjectResponse, self.database_connection, pkid)

class InjectResponseSet(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_set(InjectResponse, self.database_connection, pkid, **kwargs)

class InjectResponseGet(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_get(InjectResponse, self.database_connection, **kwargs)

# ==================================================
# Incident Endpoints
# ==================================================
class IncidentAdd(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        competition_obj = Competition.from_database(self.database_connection, competition)
        kwargs['competition'] = competition_obj.get_id()
        incident = Incident.from_dict(self.database_connection, kwargs)
        return_dict = get_empty_return_dict()
        return_dict['content'].append(incident.as_dict())
        return return_dict

class IncidentDel(CssefRPCEndpoint):
    takesKwargs = False
    onRequestArgs = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid):
        authorize_access(self.database_connection, auth, self.config)
        return model_del(Incident, self.database_connection, pkid)

class IncidentSet(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_set(Incident, self.database_connection, pkid, **kwargs)

class IncidentGet(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_get(Incident, self.database_connection, **kwargs)

# ==================================================
# Incident Response Endpoints
# ==================================================
class IncidentResponseAdd(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        competition_obj = Competition.from_database(self.database_connection, competition)
        kwargs['competition'] = competition_obj.get_id()
        incident_response = IncidentResponse.from_dict(self.database_connection, kwargs)
        return_dict = get_empty_return_dict()
        return_dict['content'].append(incident_response.from_dict())
        return return_dict

class IncidentResponseDel(CssefRPCEndpoint):
    takesKwargs = False
    onRequestArgs = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid):
        authorize_access(self.database_connection, auth, self.config)
        return model_del(IncidentResponse, self.database_connection, pkid)

class IncidentResponseSet(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'competition', 'pkid']
    def on_request(self, auth, competition, pkid, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_del(IncidentResponse, self.database_connection, pkid)

class IncidentResponseGet(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'competition']
    def on_request(self, auth, competition, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        return model_get(IncidentResponse, self.database_connection, **kwargs)

# ==================================================
# Scoring Engine Endpoints
# ==================================================
class ScoringEngineAdd(CssefRPCEndpoint):
    onRequestArgs = ['auth']
    def on_request(self, auth, **kwargs):
        authorize_access(self.database_connection, auth, self.config)
        scoringEngine = ScoringEngine.from_dict(self.database_connection, kwargs)
        return_dict = get_empty_return_dict()
        return_dict['content'].append(scoringEngine.as_dict())
        return return_dict

class ScoringEngineDel(CssefRPCEndpoint):
    takesKwargs = False
    onRequestArgs = ['auth', 'pkid']
    def on_request(self, auth, pkid):
        return model_del(ScoringEngine, self.database_connection, pkid)

class ScoringEngineSet(CssefRPCEndpoint):
    onRequestArgs = ['auth', 'pkid']
    def on_request(self, auth, pkid, **kwargs):
        return model_set(ScoringEngine, self.database_connection, pkid, **kwargs)

class ScoringEngineGet(CssefRPCEndpoint):
    onRequestArgs = ['auth']
    def on_request(self, auth, **kwargs):
        return model_get(ScoringEngine, self.database_connection, **kwargs)

endpointsDict = {
    "name": "Competition",
    "author": "",
    "menuName": "competition",
    "endpoints": [
        # Scoring Engine Endpoints
        {    "name": "Add Scoring Engine",
            "celeryName": "competitionScoringEngineAdd",
            "menu": ["engine", "add"],
            "arguments": []
        },
        {    "name": "Del Scoring Engine",
            "celeryName": "competitionScoringEngineDel",
            "menu": ["engine", "del"],
            "arguments": []
        },
        {    "name": "Set Scoring Engine",
            "celeryName": "competitionScoringEngineSet",
            "menu": ["engine", "set"],
            "arguments": []
        },
        {    "name": "Get Scoring Engine",
            "celeryName": "competitionScoringEngineGet",
            "menu": ["engine", "get"],
            "arguments": []
        },
        # Competition Endpoints
        {    "name": "Add Competition",
            "celeryName": "competitionAdd",
            "menu": ["add"],
            "arguments": [
                {    "name": "Organization",
                    "argument": "organization",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Name",
                    "argument": "name",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "URL",
                    "argument": "url",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Description",
                    "argument": "description",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Datetime Display",
                    "argument": "datetimeDisplay",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Datetime Start",
                    "argument": "datetimeStart",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Datetime Finish",
                    "argument": "datetimeFinish",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Auto-Start",
                    "argument": "autoStart",
                    "keyword": True,
                    "optional": True
                }
            ]
        },
        {    "name": "Delete Competition",
            "celeryName": "competitionDel",
            "menu": ["del"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": False
                }
            ]
        },
        {    "name": "Set Competition",
            "celeryName": "competitionSet",
            "menu": ["set"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Name",
                    "argument": "name",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "URL",
                    "argument": "url",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Description",
                    "argument": "description",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Datetime Display",
                    "argument": "datetimeDisplay",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Datetime Start",
                    "argument": "datetimeStart",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Datetime Finish",
                    "argument": "datetimeFinish",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Auto-Start",
                    "argument": "autoStart",
                    "keyword": True,
                    "optional": True
                }
            ]
        },
        {    "name": "Get Competition",
            "celeryName": "competitionGet",
            "menu": ["get"],
            "arguments": [
                {    "name": "Organization",
                    "argument": "organization",
                    "keyword": True,
                    "optional": False,
                },
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": False,
                },
                {    "name": "Name",
                    "argument": "name",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "URL",
                    "argument": "url",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Description",
                    "argument": "description",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Datetime Display",
                    "argument": "datetimeDisplay",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Datetime Start",
                    "argument": "datetimeStart",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Datetime Finish",
                    "argument": "datetimeFinish",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Auto-Start",
                    "argument": "autoStart",
                    "keyword": True,
                    "optional": True
                }
            ]
        },
        # Team Endpoints
        {    "name": "Add Team",
            "celeryName": "competitionTeamAdd",
            "menu": ["team", "add"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Name",
                    "argument": "name",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Username",
                    "argument": "username",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Password",
                    "argument": "password",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Network CIDR",
                    "argument": "networkCidr",
                    "keyword": True,
                    "optional": False
                }
            ]
        },
        {    "name": "Delete Team",
            "celeryName": "competitionTeamDel",
            "menu": ["team", "del"],
            "arguments": [
                {    "name": "Team",
                    "argument": "team",
                    "keyword": True,
                    "optional": False
                }
            ]
        },
        {    "name": "Set Team",
            "celeryName": "competitionTeamSet",
            "menu": ["team", "set"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Name",
                    "argument": "name",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Username",
                    "argument": "username",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Password",
                    "argument": "password",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Network CIDR",
                    "argument": "networkCidr",
                    "keyword": True,
                    "optional": True
                }
            ]
        },
        {    "name": "Get Team",
            "celeryName": "competitionTeamGet",
            "menu": ["team", "get"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Name",
                    "argument": "name",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Username",
                    "argument": "username",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Network CIDR",
                    "argument": "networkCidr",
                    "keyword": True,
                    "optional": True
                }
            ]
        },
        # Score Endpoints
        {    "name": "Add Score",
            "celeryName": "competitionScoreAdd",
            "menu": ["score", "add"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Team",
                    "argument": "team",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Datetime",
                    "argument": "datetime",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Value",
                    "argument": "value",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Message",
                    "argument": "message",
                    "keyword": True,
                    "optional": True
                }
            ]
        },
        {    "name": "Delete Score",
            "celeryName": "competitionScoreDel",
            "menu": ["score", "del"],
            "arguments": [
                {    "name": "Score",
                    "argument": "score",
                    "keyword": True,
                    "optional": False
                }
            ]
        },
        {    "name": "Set Score",
            "celeryName": "competitionScoreSet",
            "menu": ["score", "set"],
            "arguments": [
                {    "name": "Score",
                    "argument": "Score",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Team",
                    "argument": "team",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Datetime",
                    "argument": "datetime",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Value",
                    "argument": "value",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Message",
                    "argument": "message",
                    "keyword": True,
                    "optional": True
                }
            ]
        },
        {    "name": "Get Score",
            "celeryName": "competitionScoreGet",
            "menu": ["score", "get"],
            "arguments": [
                {    "name": "Score",
                    "argument": "Score",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Team",
                    "argument": "team",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Datetime",
                    "argument": "datetime",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Value",
                    "argument": "value",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Message",
                    "argument": "message",
                    "keyword": True,
                    "optional": True
                }
            ]
        },
        # Inject Endpoints
        {    "name": "Add Inject",
            "celeryName": "competitionInjectAdd",
            "menu": ["inject", "add"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Require Response",
                    "argument": "requireResponse",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Manual Delivery",
                    "argument": "manualDelivery",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Datetime Delivery",
                    "argument": "datetimeDelivery",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Datetime Response Due",
                    "argument": "datetimeResponseDue",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Datetime Response Close",
                    "argument": "datetimeResponseClose",
                    "keyword": True,
                    "optional": True
                },
                {    "name": "Title",
                    "argument": "title",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Body",
                    "argument": "body",
                    "keyword": True,
                    "optional": False
                }
            ]
        },
        {    "name": "Delete Inject",
            "celeryName": "competitionInjectDel",
            "menu": ["inject", "del"],
            "arguments": [
                {    "name": "Inject",
                    "argument": "Inject",
                    "keyword": True,
                    "optional": False
                }
            ]
        },
        {    "name": "Set Inject",
            "celeryName": "competitionInjectSet",
            "menu": ["inject", "set"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Require Response",
                    "argument": "requireResponse",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Manual Delivery",
                    "argument": "manualDelivery",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Datetime Delivery",
                    "argument": "datetimeDelivery",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Datetime Response Due",
                    "argument": "datetimeResponseDue",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Datetime Response Close",
                    "argument": "datetimeResponseClose",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Title",
                    "argument": "title",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Body",
                    "argument": "body",
                    "keyword": True,
                    "optional": False
                }
            ]
        },
        {    "name": "Get Inject",
            "celeryName": "competitionInjectGet",
            "menu": ["inject", "get"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Require Response",
                    "argument": "requireResponse",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Manual Delivery",
                    "argument": "manualDelivery",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Datetime Delivery",
                    "argument": "datetimeDelivery",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Datetime Response Due",
                    "argument": "datetimeResponseDue",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Datetime Response Close",
                    "argument": "datetimeResponseClose",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Title",
                    "argument": "title",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Body",
                    "argument": "body",
                    "keyword": True,
                    "optional": False
                }
            ]
        },
        # Inject Response Endpoints
        {    "name": "Add Inject Response",
            "celeryName": "competitionTInjectResponsedd",
            "menu": ["injectresponse", "add"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Team",
                    "argument": "team",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Inject",
                    "argument": "Inject",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Datetime",
                    "argument": "datetime",
                    "keyword": True,
                    "optional": False
                },
                {    "name": "Content",
                    "argument": "content",
                    "keyword": True,
                    "optional": False
                }
            ]
        },
        {    "name": "Delete Inject Response",
            "celeryName": "competitionInjectResponseDel",
            "menu": ["injectresponse", "del"],
            "arguments": [
                {    "name": "Inject Response",
                    "argument": "injectResponse",
                    "keyword": True,
                    "optional": False
                }
            ]
        },
        {    "name": "Set Inject Response",
            "celeryName": "competitionInjectResponseSet",
            "menu": ["injectresponse", "set"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Team",
                    "argument": "team",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Inject",
                    "argument": "Inject",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Datetime",
                    "argument": "datetime",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Content",
                    "argument": "content",
                    "keyword": True,
                    "optional": True,
                }
            ]
        },
        {    "name": "Get Inject Response",
            "celeryName": "competitionInjectResponseGet",
            "menu": ["injectresponse", "get"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Team",
                    "argument": "team",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Inject",
                    "argument": "Inject",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Datetime",
                    "argument": "datetime",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Content",
                    "argument": "content",
                    "keyword": True,
                    "optional": True,
                }
            ]
        },
        # Incident Endpoints
        {    "name": "Add Incident",
            "celeryName": "competitionIncidentAdd",
            "menu": ["incident", "add"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": False,
                },
                {    "name": "Team",
                    "argument": "team",
                    "keyword": True,
                    "optional": False,
                },
                {    "name": "Datetime",
                    "argument": "datetime",
                    "keyword": True,
                    "optional": False,
                },
                {    "name": "Subject",
                    "argument": "subject",
                    "keyword": True,
                    "optional": False,
                },
                {    "name": "Content",
                    "argument": "content",
                    "keyword": True,
                    "optional": False,
                }
            ]
        },
        {    "name": "Delete Incident",
            "celeryName": "competitionIncidentDel",
            "menu": ["incident", "del"],
            "arguments": [
                {    "name": "Incident",
                    "argument": "incident",
                    "keyword": True,
                    "optional": False,
                }
            ]
        },
        {    "name": "Set Incident",
            "celeryName": "competitionIncidentSet",
            "menu": ["incident", "set"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": False,
                },
                {    "name": "Team",
                    "argument": "team",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Datetime",
                    "argument": "datetime",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Subject",
                    "argument": "subject",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Content",
                    "argument": "content",
                    "keyword": True,
                    "optional": True,
                }
            ]
        },
        {    "name": "Get Incident",
            "celeryName": "competitionIncidentGet",
            "menu": ["incident", "get"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": False,
                },
                {    "name": "Team",
                    "argument": "team",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Datetime",
                    "argument": "datetime",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Subject",
                    "argument": "subject",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Content",
                    "argument": "content",
                    "keyword": True,
                    "optional": True,
                }
            ]
        },
        # Incident Response Endpoints
        {    "name": "Add Incident Response",
            "celeryName": "competitionIncidentResponseAdd",
            "menu": ["incidentresponse", "add"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": False,
                },
                {    "name": "Team",
                    "argument": "team",
                    "keyword": True,
                    "optional": False,
                },
                {    "name": "Incident",
                    "argument": "incident",
                    "keyword": True,
                    "optional": False,
                },
                {    "name": "Reply To",
                    "argument": "replyTo",
                    "keyword": True,
                    "optional": False,
                },
                {    "name": "Datetime",
                    "argument": "datetime",
                    "keyword": True,
                    "optional": False,
                },
                {    "name": "Subject",
                    "argument": "subject",
                    "keyword": True,
                    "optional": False,
                },
                {    "name": "Content",
                    "argument": "content",
                    "keyword": True,
                    "optional": False,
                }
            ]
        },
        {    "name": "Delete Incident Response",
            "celeryName": "competitionIncidentResponseDel",
            "menu": ["incidentresponse", "del"],
            "arguments": [
                {    "name": "Incident Response",
                    "argument": "incidentResponse",
                    "keyword": True,
                    "optional": False,
                }
            ]
        },
        {    "name": "Set Incident Response",
            "celeryName": "competitionIncidentResponseSet",
            "menu": ["incidentresponse", "set"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": False,
                },
                {    "name": "Team",
                    "argument": "team",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Incident",
                    "argument": "incident",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Reply To",
                    "argument": "replyTo",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Datetime",
                    "argument": "datetime",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Subject",
                    "argument": "subject",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Content",
                    "argument": "content",
                    "keyword": True,
                    "optional": True,
                }
            ]
        },
        {    "name": "Get Incident Response",
            "celeryName": "competitionIncidentResponseGet",
            "menu": ["incidentresponse", "get"],
            "arguments": [
                {    "name": "Competition",
                    "argument": "competition",
                    "keyword": True,
                    "optional": False,
                },
                {    "name": "Team",
                    "argument": "team",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Incident",
                    "argument": "incident",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Reply To",
                    "argument": "replyTo",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Datetime",
                    "argument": "datetime",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Subject",
                    "argument": "subject",
                    "keyword": True,
                    "optional": True,
                },
                {    "name": "Content",
                    "argument": "content",
                    "keyword": True,
                    "optional": True,
                }
            ]
        }
    ]
}