#from django.core.exceptions import ObjectDoesNotExist
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

	modelObject = None

	def __init__(self, **kwargs):
		self.model = kwargs.pop('modelInst', None)
		if not self.model:
			try:
				self.model = self.modelObject.objects.get(**kwargs)
			#except ObjectDoesNotExist:
			#	raise self.ObjectDoesNotExist("custom 1 - Database object matching query does not exist.")
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
	def create(db, kwDict):
		newObject = modelObject(kwDict)
		db.add(newObject)
		db.commit()
		# serializedModel = objectType.serializerObject(data = postData)
		# if serializedModel.is_valid():
		# 	obj = serializedModel.save()
		# 	return objectType(modelInst = obj)
		# else:
		# 	print "\n====================================="
		# 	print "Failed to create %s object!" % objectType.__name__
		# 	print "-------------------------------------"
		# 	print "Serializer errors:"
		# 	print serializedModel.errors
		# 	print "Provided values:"
		# 	print postData
		# 	print "=====================================\n"
		# 	# failed to create object
		# 	return serializedModel.errors

def wrappedSearch(objType, objTypeModel, **kwargs):
	return objTypeModel.objects.filter(**kwargs)