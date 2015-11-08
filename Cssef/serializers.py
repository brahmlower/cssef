from django.forms import widgets
from rest_framework import serializers
from models import Competition
from models import Team
from models import Score
from models import User
from models import Inject
from models import InjectResponse
from models import Incident
from models import IncidentResponse
from models import Document
from models import Organization
from models import ScoringEngine

class CompetitionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Competition
		fields = (
			'pkid',
			'name',
			'url',
			'organization',
			'description',
			'datetimeDisplay',
			'datetimeStart',
			'datetimeFinish',
			'scoringEngine',
			# 'scoringEnabled',
			# 'scoringInterval',
			# 'scoringIntervalUncertainty',
			# 'scoringMethod',
			# 'scoringSlaEnabled',
			# 'scoringSlaThreashold',
			# 'scoringSlaPenalty',
			#'servicesEnabled',
			# 'teamsViewRankingEnabled',
			# 'teamsViewScoreboardEnabled',
			# 'teamsViewServiceStatisticsEnabled',
			# 'teamsViewServiceStatusEnabled',
			# 'teamsViewInjectsEnabled',
			# 'teamsViewIncidentResponseEnabled'
			)

class TeamSerializer(serializers.ModelSerializer):
	class Meta:
		model = Team
		fields = (
			'pkid',
			'competition',
			'last_login',
			'name',
			'username',
			'password',
			'networkCidr',
			'scoreConfigurations')

class ScoreSerializer(serializers.ModelSerializer):
	class Meta:
		model = Score
		fields = (
			'pkid',
			'competition',
			'teamId',
			'datetime',
			'value',
			'message')

# class UserSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = User
# 		fields = (
# 			'last_login',
# 			'userId',
# 			'name',
# 			'username',
# 			'password',
# 			'description',
# 			'organizationId')

# 	def get_organization(self, obj):
# 		organization = Organization.objects.get(organizationId = obj.organizationId)
# 		serializer = OrganizationSerializer(organization)
# 		return serializer.data

class InjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Inject
		fields = (
			'pkid',
			'competition',
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
			'pkid',
			'competition',
			'teamId',
			'injectId',
			'datetime',
			'content')

class IncidentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Incident
		fields = (
			'pkid',
			'competition',
			'teamId',
			'datetime',
			'subject',
			'content')

class IncidentResponseSerializer(serializers.ModelSerializer):
	class Meta:
		model = IncidentResponse
		fields = (
			'pkid',
			'competition',
			'incidentId',
			'teamId',
			'replyTo',
			'datetime',
			'subject',
			'content')

class DocumentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Document
		fields = (
			'pkid',
			'inject',
			'injectResponse',
			'incidentResponse',
			'plugin',
			'contentType',
			'fileHash',
			'filePath',
			'filename',
			'urlEncodedFilename')

class ScoringEngineSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScoringEngine
		fields = (
			'pkid',
			'name',
			'packageName',
			'disabled',
			'ownership')

class OrganizationSerializer(serializers.ModelSerializer):
	members = serializers.SerializerMethodField()
	competitions = serializers.SerializerMethodField()
	class Meta:
		model = Organization
		fields = (
			'pkid',
			'name',
			'url',
			'description',
			'maxMembers',
			'maxCompetitions',
			'numMembers',
			'numCompetitions',
			'members',
			'competitions')

	def get_members(self, obj):
		users = User.objects.filter(organizationId = obj.pkid)
		usersList = []
		for i in users:
			usersList.append(UserSerializer(i).data)
		return usersList

	def get_competitions(self, obj):
		competitions = Competition.objects.filter(organization = obj.pkid)
		competitionsList = []
		for i in competitions:
			competitionsList.append(CompetitionSerializer(i).data)
		return competitionsList

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'pkid',
			'name',
			'password',
			'organization')