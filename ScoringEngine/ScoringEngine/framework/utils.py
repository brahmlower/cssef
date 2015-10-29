from django.core.exceptions import ObjectDoesNotExist
#from django.db.models.signals import post_save

class CssefObjectDoesNotExist(Exception):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return repr(self.message)

class ModelWrapper:
	class ObjectDoesNotExist(CssefObjectDoesNotExist):
		def __init__(self, message):
			self.message = message

		def __str__(self):
			return repr(self.message)

	serializerObject = None
	modelObject = None

	def __init__(self, **kwargs):
		self.model = kwargs.pop('modelInst', None)
		if not self.model:
			try:
				self.model = self.modelObject.objects.get(**kwargs)
			except ObjectDoesNotExist:
				raise self.ObjectDoesNotExist("custom 1 - Database object matching query does not exist.")
			except self.modelObject.DoesNotExist:
				raise self.ObjectDoesNotExist("custom 2 - Database object matching query does not exist.")
		#post_save.connect(self.reload, sender=self.modelObject)

	def getId(self):
		return self.model.pkid

	def delete(self):
		self.model.delete()

	def reload(self,):
		self.model.refresh_from_db()

	@staticmethod
	def search(objectType, **kwargs):
		return wrappedSearch(objectType, objectType.modelObject, **kwargs)

	@staticmethod
	def create(objectType, postData, serialized = False):
		serializedModel = objectType.serializerObject(data = postData)
		if serializedModel.is_valid():
			obj = serializedModel.save()
			if serialized:
				return serializedModel.data
			else:
				return objectType(modelInst = obj)
		else:
			print "\n====================================="
			print "Failed to create %s object!" % objectType.__name__
			print "-------------------------------------"
			print "Serializer errors:"
			print serializedModel.errors
			print "Provided values:"
			print postData
			print "=====================================\n"
			# failed to create object
			return serializedModel.errors

	@staticmethod
	def serialize(objectType, items):
		if items.__class__.__name__ == "QuerySet":
			return objectType.serializerObject(items, many = True).data
		else:
			return objectType.serializerObject(items.model).data

def wrappedSearch(objType, objTypeModel, **kwargs):
	serialized = kwargs.pop('serialized', False)
	modelResults = objTypeModel.objects.filter(**kwargs)
	if serialized:
		return objType.serialize(modelResults)
	else:
		return modelResults