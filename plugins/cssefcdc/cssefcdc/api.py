from datetime import datetime
import ipaddr
from cssefserver.utils import ModelWrapper
from cssefserver.account.api import Organization
from cssefcdc.models import Competition as CompetitionModel
from cssefcdc.models import Team as TeamModel
from cssefcdc.models import Score as ScoreModel
from cssefcdc.models import Inject as InjectModel
from cssefcdc.models import InjectResponse as InjectResponseModel
from cssefcdc.models import Incident as IncidentModel
from cssefcdc.models import IncidentResponse as IncidentResponseModel
from cssefcdc.models import ScoringEngine as ScoringEngineModel
from cssefcdc.models import Plugin as PluginModel
from cssefcdc.models import Service as ServiceModel

class ServicePlugin(ModelWrapper):
    model_object = PluginModel
    fields = [
        'name',
        'description'
    ]

    @property
    def name(self):
        return self.model.name

    @name.setter
    def name(self, value):
        self.model.name = value
        self.db_conn.commit()

    @property
    def description(self):
        return self.model.description

    @description.setter
    def description(self, value):
        self.model.description = value
        self.db_conn.commit()

    def get_module_name(self):
        #return Document.objects.get(servicemodule = self.servicemodule).filename.split(".")[0]
        pass

    def get_import_path(self, module_name=None):
        if module_name:
            #return settings.CONTENT_PLUGGINS_PATH.replace('/','.')[1:] + module_name
            return ""
        else:
            return self.get_import_path(self.get_module_name())

class Service(ModelWrapper):
    model_objectmodel_object = ServiceModel
    fields = [
        'name',
        'description',
        'manualStart',
        'datetimeStart',
        'datetimeFinish',
        'points',
        'machineIp',
        'machineFqdn',
        'defaultPort'
    ]

    @property
    def name(self):
        return self.model.name

    @name.setter
    def name(self, value):
        self.model.name = value
        self.db_conn.commit()

    @property
    def description(self):
        return self.model.description

    @description.setter
    def description(self, value):
        self.model.description = value
        self.db_conn.commit()

    @property
    def manual_start(self):
        return self.model.manualStart

    @manual_start.setter
    def manual_start(self, value):
        self.model.manualStart = value
        self.db_conn.commit()

    @property
    def datetime_start(self):
        return self.model.datetimeStart

    @datetime_start.setter
    def datetime_start(self, value):
        self.model.datetimeStart = value
        self.db_conn.commit()

    @property
    def datetime_finish(self):
        return self.model.datetimeFinish

    @datetime_finish.setter
    def datetime_finish(self, value):
        self.model.datetimeFinish = value
        self.db_conn.commit()

    @property
    def points(self):
        return self.model.points

    @points.setter
    def points(self, value):
        self.model.points = value
        self.db_conn.commit()

    @property
    def machine_ip(self):
        return self.model.machineIp

    @machine_ip.setter
    def machine_ip(self, value):
        self.model.machineIp = value
        self.db_conn.commit()

    @property
    def machine_fqdn(self):
        return self.model.machineFqdn

    @machine_fqdn.setter
    def machine_fqdn(self, value):
        self.model.machineFqdn = value
        self.db_conn.commit()

    @property
    def default_port(self):
        return self.model.defaultPort

    @default_port.setter
    def default_port(self, value):
        self.model.defaultPort = value
        self.db_conn.commit()

    # I commented this out because it relied on the loadPlugin being there.
    # Haven't bothered to migrated that quite yet :)
    # def score(self, team):
    #     instance = self.loadPlugin()
    #     score_inst = instance.score(team)
    #     score_inst.datetime = datetime.now()
    #     score_inst.teamId = team.teamId
    #     score_inst.serviceId = self.serviceId
    #     score_inst.competitionId = self.competitionId
    #     return score_inst

    # def loadPlugin(self):
    #     #moduleName = Document.objects.get(servicemodule = self.servicemodule).filename.split(".")[0]
    #     #module = __import__(settings.CONTENT_PLUGGINS_PATH.replace('/','.')[1:] + moduleName, fromlist=[moduleName])
    #     moduleName = self.plugin.getModuleName()
    #     module = __import__(self.plugin.getImportPath(moduleName), fromlist=[moduleName])
    #     return getattr(module, moduleName)(self)

class ScoringEngine(ModelWrapper):
    'Scoring Engine object to represent a scoring engine module available for use by competitions.'
    model_object = ScoringEngineModel
    fields = [
        'name',
        'packageName',
        'enabled'
    ]

    @property
    def name(self):
        return self.model.name

    @name.setter
    def name(self, value):
        self.model.name = value
        self.db_conn.commit()

    @property
    def enabled(self):
        return self.model.enabled

    @enabled.setter
    def enabled(self, value):
        self.model.enabled = value
        self.db_conn.commit()

    @property
    def package_name(self):
        # This is a read-only attribute, so there is no corresponding setter method
        return self.model.name

class Competition(ModelWrapper):
    'Competition object for controling competition settings and operation'
    model_object = CompetitionModel
    fields = [
        'organization',
        'name',
        'url',
        'description',
        'datetimeDisplay',
        'datetimeStart',
        'datetimeFinish',
        'autoStart']

    @property
    def organization(self):
        return self.model.organization

    @organization.setter
    def organization(self, value):
        # Todo:
        # Only site admins should be able to change this
        self.model.organization = value
        self.db_conn.commit()

    @property
    def name(self):
        return self.model.name

    @name.setter
    def name(self, value):
        # Todo:
        # Only site admins & organization admins should be able to change this
        self.model.name = value
        self.db_conn.commit()

    @property
    def url(self):
        return self.model.url

    @url.setter
    def url(self, value):
        # Todo:
        # Only site admins should be able to change this
        self.model.url = value
        self.db_conn.commit()

    @property
    def description(self):
        return self.model.description

    @description.setter
    def description(self, value):
        # Todo:
        # Only site admins & organization admins should be able to change this
        self.model.description = value
        self.db_conn.commit()

    @property
    def datetime_display(self):
        return self.model.datetimeDisplay

    @datetime_display.setter
    def datetime_display(self, value):
        # Todo:
        # Only site admins & organization admins should be able to change this
        self.model.datetimeDisplay = value
        self.db_conn.commit()

    @property
    def datetime_start(self):
        return self.model.datetimeStart

    @datetime_start.setter
    def datetime_start(self, value):
        # Todo:
        # Only site admins & organization admins should be able to change this
        self.model.datetimeStart = value
        self.db_conn.commit()

    @property
    def datetime_finish(self):
        return self.model.datetimeFinish

    @datetime_finish.setter
    def datetime_finish(self, value):
        # Todo:
        # Only site admins & organization admins should be able to change this
        self.model.datetimeFinish = value
        self.db_conn.commit()

    @property
    def auto_start(self):
        return self.model.autoStart

    @auto_start.setter
    def auto_start(self, value):
        # Todo:
        # Only site admins & organization admins should be able to change this
        self.model.autoStart = value
        self.db_conn.commit()

    @property
    def scoring_engine(self):
        return self.model.scoringEngine

    @scoring_engine.setter
    def scoring_engine(self, value):
        # Todo:
        # Only site admins & organization admins should be able to change this
        self.model.scoringEngine = value
        self.db_conn.commit()

    @classmethod
    def from_dict(cls, db_conn, kw_dict):
        org = Organization.from_database(db_conn, pkid=kw_dict['organization'])
        if not org:
            print "Failed to get organization with pkid '%s'" % kw_dict['organization']
            raise ValueError
        # Competition limiting is disabled for now since I'm not entirely sure
        # how it will be implemented with the new plugin arrangement
        #if org.model.numCompetitions >= org.maxCompetitions:
        #    raise MaxCompetitionsReached(org.maxCompetitions)
        # Copied right from ModelWrapper.fromDict
        model_object_inst = cls.model_object()
        cls_inst = cls(db_conn, model_object_inst)
        for i in kw_dict:
            if i in cls_inst.fields:
                setattr(cls_inst, i, kw_dict[i])
        db_conn.add(cls_inst.model)
        db_conn.commit()
        #org.setNumCompetitions()
        return cls_inst

    def check(self):
        # Todo:
        # I don't think this is necessary. Lets just remove this
        # This conducts a consistency check on the competiton settings.
        print "A consistency check was conducted here..."

    def start(self):
        # Somehow start scoring the competition :O
        pass

class Team(ModelWrapper):
    'Team object for controling team settings'
    model_object = TeamModel
    fields = [
        'username',
        'name',
        'password',
        'networkCidr',
        'scoreConfigurations']

    @property
    def username(self):
        return self.model.username

    @username.setter
    def username(self, value):
        self.model.username = value
        self.db_conn.commit()

    @property
    def name(self):
        return self.model.name

    @name.setter
    def name(self, value):
        self.model.name = value
        self.db_conn.commit()

    @property
    def password(self):
        return self.model.password

    @password.setter
    def password(self, value):
        self.model.password = value
        self.db_conn.commit()

    @property
    def network_cidr(self):
        return self.model.networkCidr

    @network_cidr.setter
    def network_cidr(self, value):
        parsed_value = ipaddr.IPNetwork(value)
        self.model.networkCidr = parsed_value
        self.db_conn.commit()

    @property
    def score_configurations(self):
        return self.model.scoreConfigurations

    @score_configurations.setter
    def score_configurations(self, value):
        # This function will also need to change as I improve the way
        # score configurations are interacted with....
        self.model.scoreConfigurations = value
        self.db_conn.commit()

    def get_scores(self, **kwargs):
        return Score.search(team=self.model, **kwargs)

    def get_incidents(self, **kwargs):
        return Incident.search(team=self.model, **kwargs)

    def get_incident_responses(self, **kwargs):
        return IncidentResponse.search(self.model, **kwargs)

    def get_inject_responses(self, **kwargs):
        return InjectResponse.search(self.model, **kwargs)

class Score(ModelWrapper):
    'Score object for controlling score settings'
    model_object = ScoreModel
    fields = [
        'datetime',
        'value',
        'message']

    @property
    def datetime(self):
        return self.model.datetime

    @datetime.setter
    def datetime(self, value):
        self.model.datetime = value
        self.db_conn.commit()

    @property
    def value(self):
        return self.model.value

    @value.setter
    def value(self, value):
        self.model.value = value
        self.db_conn.commit()

    @property
    def message(self):
        return self.model.message

    @message.setter
    def message(self, value):
        self.model.message = value
        self.db_conn.commit()

class Inject(ModelWrapper):
    'Inject object for controling inject settings'
    model_object = InjectModel
    fields = [
        'requireResponse',
        'manualDelivery',
        'datetimeDelivery',
        'datetimeResponseDue',
        'datetimeResponseClose',
        'title',
        'body']

    @property
    def require_response(self):
        return self.model.requireResponse

    @require_response.setter
    def require_response(self, value):
        self.model.requireResponse = value
        self.db_conn.commit()

    # Manual Delivery modules
    @property
    def manual_delivery(self):
        return self.model.manualDelivery

    @manual_delivery.setter
    def manual_delivery(self, value):
        self.model.manualDelivery = value
        self.db_conn.commit()

    # Datetime Delivery modules
    @property
    def datetime_delivery(self):
        return self.model.datetimeDelivery

    @datetime_delivery.setter
    def datetime_delivery(self, value):
        self.model.datetimeDelivery = value
        self.db_conn.commit()

    # Datetime Response Due modules
    @property
    def datetime_response_due(self):
        return self.model.datetimeResponseDue

    @datetime_response_due.setter
    def datetime_response_due(self, value):
        self.model.datetimeResponseDue = value
        self.db_conn.commit()

    # Datetime Response Close modules
    @property
    def datetime_response_close(self):
        return self.model.datetimeResponseClose

    @datetime_response_close.setter
    def datetime_response_close(self, value):
        self.model.datetimeResponseClose = value
        self.db_conn.commit()

    # Title modules
    @property
    def title(self):
        return self.model.title

    @title.setter
    def title(self, value):
        self.model.title = value
        self.db_conn.commit()

    # Body modules
    @property
    def body(self):
        return self.model.body

    @body.setter
    def body(self, value):
        self.model.body = value
        self.db_conn.commit()

    # # Document modules
    # def addDocument(self, fileObj, contentType, filePath, filename, **kwargs):
    #     # What do I do with the file object....?
    #     Document(
    #         kwargs,
    #         inject = self.model,
    #         contentType = contentType,
    #         filePath = filePath,
    #         filename = filename)

    # def getDocuments(self):
    #     return Document.search(inject = self.model)

    # def delDocument(self, documentObj):
    #     documentObj.delete()
    #     del documentObj

    # Inject Response module
    def get_responses(self):
        return InjectResponse.search(self.db_conn, inject=self.model)

class InjectResponse(ModelWrapper):
    'Inject Response object for controling inject response settings'
    model_object = InjectResponseModel
    fields = [
        'datetime',
        'content']

    @property
    def datetime(self):
        return self.model.datetime

    @datetime.setter
    def datetime(self, value):
        self.model.datetime = value
        self.db_conn.commit()

    @property
    def content(self):
        return self.model.content

    @content.setter
    def content(self, value):
        self.model.content = value
        self.db_conn.commit()

class Incident(ModelWrapper):
    'Incident object for controlling incident settings'
    model_object = IncidentModel
    fields = [
        'datetime',
        'subject',
        'content']

    @property
    def datetime(self):
        return self.model.datetime

    @datetime.setter
    def datetime(self, value):
        self.model.datetime = value
        self.db_conn.commit()

    @property
    def subject(self):
        return self.model.subject

    @subject.setter
    def subject(self, value):
        self.model.subject = value
        self.db_conn.commit()

    @property
    def content(self):
        return self.model.content

    @content.setter
    def content(self, value):
        self.model.content = value
        self.db_conn.commit()

class IncidentResponse(ModelWrapper):
    'Incident Response object for controlling incident response settings'
    model_object = IncidentResponseModel
    fields = [
        'replyTo',
        'datetime',
        'subject',
        'content']

    @property
    def reply_to(self):
        return self.model.replyTo

    @reply_to.setter
    def reply_to(self, value):
        self.model.replyTo
        self.db_conn.commit()

    @property
    def datetime(self):
        return self.model.datetime

    @datetime.setter
    def datetime(self, value):
        self.model.replyTo
        self.db_conn.commit()

    @property
    def subject(self):
        return self.model.subject

    @subject.setter
    def subject(self, value):
        self.model.subject = value
        self.db_conn.commit()

    @property
    def content(self):
        return self.model.content

    @content.setter
    def content(self, value):
        self.model.content = value
        self.db_conn.commit()
