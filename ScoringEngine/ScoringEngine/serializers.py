from django.forms import widgets
from rest_framework import serializers
from models import Competition
from models import Team
from models import Plugin
from models import Service
from models import Score
from models import User
from models import Inject
from models import InjectResponse
from models import Incident
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
			'description',
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
			'name',
			'username',
			'password',
			'networkCidr',
			'scoreConfigurations')

class PluginSerializer(serializers.ModelSerializer):
	document = serializers.SerializerMethodField()
	class Meta:
		model = Plugin
		fields = (
			'pluginId',
			'name',
			'description',
			'document')

	def get_document(self, obj):
		document = Document.objects.get(plugin = obj)
		serializer = DocumentSerializer(document)
		return serializer.data

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

class UserSerializer(serializers.ModelSerializer):
	#organization = serializers.SerializerMethodField()
	class Meta:
		model = User
		fields = (
			'last_login',
			'userId',
			'name',
			'username',
			'password',
			'organizationId')

	def get_organization(self, obj):
		organization = Organization.objects.get(organizationId = obj.organizationId)
		serializer = OrganizationSerializer(organization)
		return serializer.data

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

class IncidentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Incident
		fields = (
			'incidentId',
			'competitionId',
			'teamId',
			'datetime',
			'subject',
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
			'fileHash',
			'filePath',
			'filename',
			'urlEncodedFilename')

class OrganizationSerializer(serializers.ModelSerializer):
	members = serializers.SerializerMethodField()
	competitions = serializers.SerializerMethodField()
	class Meta:
		model = Organization
		fields = (
			'organizationId',
			'name',
			'url',
			'description',
			'maxMembers',
			'maxCompetitions',
			'members',
			'competitions')

	def get_members(self, obj):
		users = User.objects.filter(organizationId = obj.organizationId)
		usersList = []
		for i in users:
			usersList.append(UserSerializer(i).data)
		return usersList

	def get_competitions(self, obj):
		competitions = Competition.objects.filter(organization = obj.organizationId)
		competitionsList = []
		for i in competitions:
			competitionsList.append(CompetitionSerializer(i).data)
		return competitionsList

	# def create(self, validatedData):
	# 	return Organization.objects.create(**validatedData)

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'userId',
			'name',
			'password',
			'organizationId')
