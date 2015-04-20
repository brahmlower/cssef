from django.forms import widgets
from rest_framework import serializers
from models import Competition
from models import Team
from models import Plugin
from models import Service
from models import Score
from models import Inject
from models import User
from models import InjectResponse
from models import IncidentResponse
from models import Document
from models import Organization

class CompetitionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Competition
		fields = (
			'competitionId',
			'name',
			'url',
			'organization',
			'descriptionShort',
			'descriptionFull',
			'datetimeDisplay',
			'datetimeStart',
			'datetimeFinish',
			'scoringEnabled',
			'scoringInterval',
			'scoringIntervalUncertainty',
			'scoringMethod',
			'scoringSlaEnabled',
			'scoringSlaThreashold',
			'scoringSlaPenalty',
			'servicesEnabled',
			'teamsViewRankingEnabled',
			'teamsViewScoreboardEnabled',
			'teamsViewServiceStatisticsEnabled',
			'teamsViewServiceStatusEnabled',
			'teamsViewInjectsEnabled',
			'teamsViewIncidentResponseEnabled')

class TeamSerializer(serializers.ModelSerializer):
	class Meta:
		model = Team
		fields = (
			'teamId',
			'competitionId',
			'last_login',
			'teamname',
			'loginname',
			'password',
			'networkCidr',
			'scoreConfigurations')

class PluginSerializer(serializers.ModelSerializer):
	class Meta:
		model = Plugin
		fields = (
			'pluginId',
			'name',
			'description')

class ServiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Service
		fields = (
			'serviceId',
			'competitionId',
			'plugin',
			'name',
			'description',
			'manualStart',
			'datetimeStart',
			'datetimeFinish',
			'points',
			'machineIp',
			'machineFqdn',
			'defaultPort')

class ScoreSerializer(serializers.ModelSerializer):
	class Meta:
		model = Score
		fields = (
			'scoreId',
			'competitionId',
			'teamId',
			'serviceId',
			'datetime',
			'value',
			'message')

class InjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Inject
		fields = (
			'injectId',
			'competitionId',
			'requireResponse',
			'manualDelivery',
			'datetimeDelivery',
			'datetimeResponseDue',
			'datetimeResponseClose',
			'title',
			'body')


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'last_login',
			'userId',
			'name',
			'username',
			'password',
			'organization')

class InjectResponseSerializer(serializers.ModelSerializer):
	class Meta:
		model = InjectResponse
		fields = (
			'injectResponseId',
			'competitionId',
			'teamId',
			'injectId',
			'datetime',
			'content')

class IncidentResponseSerializer(serializers.ModelSerializer):
	class Meta:
		model = IncidentResponse
		fields = (
			'incidentResponseId',
			'competitionId',
			'teamId',
			'replyTo',
			'datetime',
			'subject',
			'content')

class DocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Document
		fields = (
			'documentId',
			'inject',
			'injectResponse',
			'incidentResponse',
			'plugin',
			'contentType',
			'filehash',
			'filepath',
			'filename',
			'urlEncodedFilename')

class OrganizationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Organization
		fields = (
			'organizationId',
			'name',
			'url')

	def create(self, validatedData):
		return Organization.objects.create(**validatedData)
