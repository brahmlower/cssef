from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from ScoringEngine.models import Document
from ScoringEngine import settings
from django.core.files.uploadedfile import UploadedFile
from hashlib import md5
from urllib import quote
import json

class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

def objectExists(objectType, **kwargs):
	try:
		objectType.objects.get(**kwargs)
		return True
	except objectType.DoesNotExist:
		return False

def listObject(objectType, objectTypeSerializer, **kwargs):
	objectInstance = objectType.objects.get(**kwargs)
	serializer = objectTypeSerializer(objectInstance)
	return JSONResponse(serializer.data)

def listObjects(objectType, objectTypeSerializer):
	objects = objectType.objects.all()
	serializer = objectTypeSerializer(objects, many = True)
	return JSONResponse(serializer.data)

def postObject(request, objectTypeSerializer):
	serializer = objectTypeSerializer(data = request.POST)
	if serializer.is_valid():
		serializerResult = serializer.save()
		if request.FILES:
			print request.FILES
			for i in request.FILES:
				saveDocument(request.FILES[i], serializerResult)
		return JSONResponse(serializer.data, status = status.HTTP_201_CREATED)
	print "Serializer object is not valid:"
	print serializer.errors
	return JSONResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

def patchObject(request, objectType, objectTypeSerializer, **kwargs):
	objectInstance = objectType.objects.get(**kwargs)
	serializer = objectTypeSerializer(objectInstance)
	data = serializer.data
	data.update(json.loads(request.body))
	serializer = objectTypeSerializer(objectInstance, data = data)
	if serializer.is_valid():
		serializer.save()
		return JSONResponse(serializer.data, status = status.HTTP_202_ACCEPTED)
	return JSONResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

def deleteObject(objectType, **kwargs):
	objectType.objects.get(**kwargs).delete()
	return Response(status = status.HTTP_204_NO_CONTENT)

def saveDocument(postedFile, relatedObject):
	uploadedFile = UploadedFile(postedFile)
	fileContent = uploadedFile.read()
	document = Document()
	document.fileHash = md5(fileContent).hexdigest()
	document.urlEncodedFilename = quote(uploadedFile.name)
	document.filename = uploadedFile.name
	document.contentType = uploadedFile.file.content_type
	document.filePath = settings.BASE_DIR + '/' + document.filename
	if relatedObject.__class__.__name__.lower() == "queryset":
		if len(relatedObject) == 1:
			setattr(document, relatedObject[0].__class__.__name__.lower(), relatedObject[0])
		else:
			print "ERROR: The queryset object had %d elements to it. Expected only one." % len(relatedObject)
			return None
	else:
		setattr(document, relatedObject.__class__.__name__.lower(), relatedObject)
	print document.filePath
	wfile = open(document.filePath, "w")
	wfile.write(fileContent)
	wfile.close()
	document.save()