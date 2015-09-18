from django.forms import widgets
from rest_framework import serializers
from models import Plugin
from models import Service

class PluginSerializer(serializers.ModelSerializer):
	#document = serializers.SerializerMethodField()
	class Meta:
		model = Plugin
		fields = (
			'pluginId',
			'name',
			'description')
		#	'document')

	# def get_document(self, obj):
	# 	document = Document.objects.get(plugin = obj)
	# 	serializer = DocumentSerializer(document)
	# 	return serializer.data

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