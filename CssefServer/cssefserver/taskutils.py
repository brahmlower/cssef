from cssefserver import DatabaseConnection

def modelDel(cls, pkid):
	if pkid == "*":
		# todo: implement a wildcard
		returnDict = getEmptyReturnDict()
		returnDict['value'] = 1
		returnDict['message'] = ["Wildcards are not implemented yet."]
		return returnDict
	elif type(pkid) == str and "-" in pkid:
		x = pkid.split("-")
		if len(x) == 2:
			try:
				for pkid in range(int(x[0]), int(x[1])+1):
					modelObj = cls.fromDatabase(DatabaseConnection, pkid)
					if modelObj:
						modelObj.delete()
			except ValueError:
				# One of the ranges provided could not be cast as an integer. Return error.
				returnDict = getEmptyReturnDict()
				returnDict['value'] = 1
				returnDict['message'] = ["Range value could not be cast to integer. Expected integer range like 1-4. Got '%s' instead." % pkid]
				return returnDict
		else:
			print x
			returnDict = getEmptyReturnDict()
			returnDict['value'] = 1
			returnDict['message'] = ["Expected integer range like 1-4. Got '%s' instead." % pkid]
			return returnDict
	elif type(pkid) == int:
		modelObj = cls.fromDatabase(DatabaseConnection, pkid)
		modelObj.delete()
	else:
		# We don't know what the hell we were given. Disregard it and thow an error :(
		returnDict = getEmptyReturnDict()
		returnDict['value'] = 1
		returnDict['message'] = ["Expected integer value (5) or range (2-7). Got '%s' of type %s instead." % (str(pkid), str(type(pkid)))]
	return getEmptyReturnDict()

def modelSet(cls, pkid, **kwargs):
	modelObj = cls.fromDatabase(DatabaseConnection, pkid)
	modelObj.edit(**kwargs)
	returnDict = getEmptyReturnDict()
	returnDict['content'].append(modelObj.asDict())
	return returnDict

def modelGet(cls, **kwargs):
	modelObjs = cls.search(DatabaseConnection, **kwargs)
	returnDict = getEmptyReturnDict()
	for i in modelObjs:
		returnDict['content'].append(i.asDict())
	return returnDict