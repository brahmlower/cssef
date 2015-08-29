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

from ScoringEngine.endpoints import CssefObjectDoesNotExist
from ScoringEngine.endpoints import MaxMembersReached
from ScoringEngine.endpoints import MaxCompetitionsReached

class JSONResponse(HttpResponse):
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

def callObject(classPointer, methodName, content, **kwargs):
	kwargs['serialized'] = True
	try:
		method = getattr(classPointer, methodName) 
		serializedData = method(**kwargs)
	except CssefObjectDoesNotExist:
		return Response(status = status.HTTP_404_NOT_FOUND)
	if content:
		return JSONResponse(serializedData)
	else:
		return Response(status = status.HTTP_204_NO_CONTENT)

def listObject(classPointer, methodName, **kwargs):
	try:
		obj = classPointer(**kwargs)
		serializedData = classPointer.serialize(obj)
	except CssefObjectDoesNotExist:
		return Response(status = status.HTTP_404_NOT_FOUND)
	return JSONResponse(serializedData)

def listObjects(classPointer, methodName):
	method = getattr(classPointer, methodName) 
	serializedData = method(serialized = True)
	return JSONResponse(serializedData)

def postObject(classPointer, methodName, request):
	method = getattr(classPointer, methodName)
	try:
		returnObject = method(request.POST, serialized = True)
	except MaxMembersReached as error:
		return JSONResponse({error.message}, status = status.HTTP_403_FORBIDDEN)
	except MaxCompetitionsReached as error:
		return JSONResponse({error.message}, status = status.HTTP_403_FORBIDDEN)
	if returnObject:
		if request.FILES:
			for i in request.FILES:
				# TODO: create/save the file here
				pass
		return JSONResponse(returnObject, status = status.HTTP_201_CREATED)
	print "Failed to create object..."
	print returnObject
	print request.POST
	return JSONResponse(returnObject, status = status.HTTP_400_BAD_REQUEST)

def patchObject(competition, subclass, request, **kwargs):
	return Response(status = status.HTTP_501_NOT_IMPLEMENTED)

# def patchObject(request, objectType, objectTypeSerializer, **kwargs):
# 	objectInstance = objectType.objects.get(**kwargs)
# 	serializer = objectTypeSerializer(objectInstance)
# 	data = serializer.data
# 	data.update(json.loads(request.body))
# 	serializer = objectTypeSerializer(objectInstance, data = data)
# 	if serializer.is_valid():
# 		serializer.save()
# 		return JSONResponse(serializer.data, status = status.HTTP_202_ACCEPTED)
# 	return JSONResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

def deleteObject(classPointer, methodName, **kwargs):
	obj = classPointer(**kwargs)
	getattr(obj, methodName)()
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
	#print document.filePath
	wfile = open(document.filePath, "w")
	wfile.write(fileContent)
	wfile.close()
	document.save()