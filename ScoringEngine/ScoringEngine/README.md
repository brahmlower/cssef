# API Documentation

#### getObjects()
endpoints.**getObjects**(classPointer, \*\*kwargs)
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### getObject()
endpoints.**getObject**(classPointer, \*\*kwargs)
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *
#### wrappedSearch()
endpoints.**wrappedSearch**(objType, objTypeModel, \*\*kwargs)
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### getCompetition()
endpoints.**getCompetition**(\*\*kwargs)
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### getCompetitions()
endpoints.**getCompetitions**(\*\*kwargs)
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### getOrganization()
endpoints.**getOrganization**(\*\*kwargs)
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### getOrganizations()
endpoints.**getOrganizations**(\*\*kwargs)
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### createOrganization()
endpoints.**createOrganization**(postData, serialized = False)
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### editOrganization()
endpoints.**editOrganization**(\*\*kwargs)
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### getUsers()
endpoints.**getUsers**(\*\*kwargs)
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### getUser()
endpoints.**getUser**(\*\*kwargs)
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### editUser()
endpoints.**editUser**(\*\*kwargs)
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

## Competition
#### count()
endpoints.Competition.**count**(\*\*kwarg)
<br>This returns the number of Competition objects that match the provided filter.
<br>**Input**
<br>**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;Returns value of type integer
<br>**Example**
```
>>> from ScoringEngine.endpoints import *
>>> orgData = {'name': 'New Org', 'url':'new_org'}
>>> org = createOrganization(orgData)
>>> org.createCompetition({'name':'First Comp})
>>> org.createCompetition({'name': 'Second Comp})
>>> organizationId = org.getId()
>>> numCompetitions = Competition.count(organization = organizationId)
>>> print numCompetitions
2
>>>
```
* * *

#### getName()
endpoints.Competition.**getName**(self)
<br>This will return the name of the competition as a string.
<br>**Input**
<br>&nbsp;&nbsp;&nbsp;&nbsp;None
<br>**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;Returns value of type str
<br>**Example**
```
>>> from ScoringEngine.endpoints import *
>>> orgData = {'name': 'New Org', 'url':'new_org'}
>>> org = createOrganization(orgData)
>>> competition = org.createCompetition({'name':'First Comp})
>>> name = competition.getName()
>>> print name
New Org
>>>
```
* * *


#### check()
endpoints.Competition.**check**(self)<br>
This should one day perform a consistency check to make sure the competition doesn't have any conflicting values set. This may or may not be necessary depending on how much I implement error checking.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### createTeam()
endpoints.Competition.**createTeam**(self, objType, serialized = False)
<br>This will create and return a new team in within the competition.
<br>**Input**
* postData (required)
<br>&nbsp;&nbsp;&nbsp;&nbsp;Dictionary containing required keywords for a new Team.
* serialized (optional)
<br>&nbsp;&nbsp;&nbsp;&nbsp;Return as object (False) or as a dictionary (True). If not provided, this value will default to False.

**Output**
<br>**Example**
```
>>> from ScoringEngine.endpoints import *
>>> orgData = {'name': 'New Org', 'url':'new_org'}
>>> org = createOrganization(orgData)
>>> competition = org.createCompetition({'name':'First Comp})
>>> teamData = {'name':'New Team', 'username':'new_team', 'password':'$3(Ur#!'}
>>> team = competition.createTeam(teamData)
>>>
```
* * *

#### editTeam()
endpoints.Competition.**editTeam**(\*\*kwargs)
<br>Take a dictionary of values for the Team object and applies their values to the team object. This effectively calls getTeam() with the provided teamId, then calls edit() on that team. This would be used in cases where you only wish to apply changes to team, but you don't have the team object.
<br>**Input**
* \*\*kwargs
  * teamId - *Integer* (required)
<br>&nbsp;&nbsp;&nbsp;&nbsp;Specifies the team to edit. Cannot be changed.
  * serialized - *Boolean* (optional)
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * name - *String* (optional)
<br>&nbsp;&nbsp;&nbsp;&nbsp;The team name
  * username - *String* (optional)
<br>&nbsp;&nbsp;&nbsp;&nbsp;The username used to sign in
  * password - *String* (optional)
<br>&nbsp;&nbsp;&nbsp;&nbsp;The password used to sign in
  * networkCidr - *String* (optional)
<br>&nbsp;&nbsp;&nbsp;&nbsp;The CIDR representation of the network associated with the team
  * scoreConfiguration - *String* (optional)
<br>&nbsp;&nbsp;&nbsp;&nbsp;The dictionary for storing scoring configurations

**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;None
<br>**Example**
```
>>> from ScoringEngine.endpoints import *
>>> org = createOrganization({'name': 'New Org', 'url':'new_org'})
>>> competition = org.createCompetition({'name':'First Comp})
>>> teamData = {'name':'New Team', 'username':'new_team', 'password':'$3(Ur#!'}
>>> team = competition.createTeam(teamData)
>>> print team.getName()
New Team
>>> competition.editTeam(teamId = team.getId(), name = 'Super Team')
>>> print team.getName()
Super Team
>>>
```
* * *

#### getTeam()
endpoints.Competition.**getTeam**(self, \*\*kwargs)
<br> Retrieves an existing team object.
<br>**Input**

**Output**
<br>**Example**
```
>>> from SoringEngine.endpoints import *
>>> org = createOrganization({'name': 'New Org', 'url':'new_org'})
>>> competition = org.createCompetition({'name':'First Comp})
>>> team = competition.createTeam({'name':'New Team', 'username':'new_team', 'password':'$3(Ur#!'})
>>> competition.getTeam(teamId = team.getId())
>>>
```
* * *

#### getTeams()
endpoints.Competition.**getTeams**(self, \*\*kwargs)
<br> Retrieves an existing team object.
<br>**Input**
* objType (required):
<br>&nbsp;&nbsp;&nbsp;&nbsp;This is the class type of the object to search for
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.

**Output**
<br>**Example**
This is a bad example, using a function that doesn't exist. I'll get back to this eventually.
```
>>> from SoringEngine.endpoints import *
>>> org = createOrganization({'name': 'New Org', 'url':'new_org'})
>>> competition = org.createCompetition({'name':'First Comp})
>>> team = competition.createTeam({'name':'New Team', 'username':'new_team', 'password':'$3(Ur#!'})
>>> team.setScore(100)
>>> teamList = competition.getTeams(score = 100)
>>> len(teamList)
1
>>> 
```
* * *
#### deleteTeam()
endpoints.Competition.**deleteTeam**(self, \*\*kwargs)
<br> Deletes the specified team object.
<br>**Input**
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the Team object you'd like to delete.

**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;None
<br>**Example**
```
competition = getCompetition(competitionId = 1)
competition.deleteTeam(teamId = 5)
```
* * *

#### createIncident()
endpoints.Competition.**createIncident**(self, postData, serialized = False)
<br> Creates a new incident object.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### editIncident()
endpoints.Competition.**editIncident**(self, \*\*kwargs)
<br> Edits an existing incident object.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### getIncident()
endpoints.Competition.**getIncident**(self, \*\*kwargs)
<br> Retrieves an existing incident object.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### getIncidents()
endpoints.Competition.**getIncidents**(self, \*\*kwargs)
<br> Retrieves multiple existing incident objects.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### deleteIncident()
endpoints.Competition.**deleteIncident**(self, \*\*kwargs)
<br> Deletes a single incident object.
<br>**Input**
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the Incident object you'd like to delete.

**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;None
<br>**Example**
```
competition = getCompetition(competitionId = 1)
competition.deleteIncident(incidentId = 5)
```
* * *

#### createIncidentResponse()
endpoints.Competition.**createIncidentResponse**()
<br> Creates a new incident response object.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### editIncidentResponse()
endpoints.Competition.**editIncidentResponse**(self, \*\*kwargs)
<br> Edits an existing incident response object.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### getIncidentResponse()
endpoints.Competition.**getIncidentResponse**(self, \*\*kwargs)
<br> Retrieves an existing incident response object.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *
#### getIncidentResponses
endpoints.Competition.**getIncidentResponses**(self, \*\*kwargs)
<br> Retrieves multiple existing incident response objects.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### deleteIncidentResponse()
endpoints.Competition.**deleteIncidentResponse**(self, \*\*kwargs)
<br> Deletes a single specified incident response object.
<br>**Input**
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the IncidentResponse object you'd like to delete.

**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;None
<br>**Example**
```
competition = getCompetition(competitionId = 1)
competition.deleteIncidentResponse(incidentResponseId = 5)
```

#### createInject()
endpoints.Competition.**createInject**()
<br> Creates a new inject object.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### editInject()
endpoints.Competition.**editInject**(self, \*\*kwargs)
<br> Edits an existing inject object.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### getInject()
endpoints.Competition.**getInject**(self, \*\*kwargs)
<br> Retrieves an existing inject object.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### getInjects()
endpoints.Competition.**getInjects**(self, \*\*kwargs)
<br> Retrieves existing inject objects.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### deleteInject()
endpoints.Competition.**deleteInject**(self, \*\*kwargs)
<br> Deletes a single specified inject response.
<br>**Input**
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the Inject object you'd like to delete.

**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;None
<br>**Example**
```
competition = getCompetition(competitionId = 1)
competition.deleteInject(injectId = 5)
```

#### createInjectResponse
endpoints.Competition.**createInjectResponse**()
<br> Creates a new inject response object.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### editInjectResponse()
endpoints.Competition.**editInjectResponse**(self, \*\*kwargs)
<br> Edits an existing inject response object.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### getInjectResponse()
endpoints.Competition.**getInjectResponse**(self, \*\*kwargs)
<br> Retrieves an existing inject response object.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### getInjectResponses()
endpoints.Competition.**getInjectResponses**(self, \*\*kwargs)
<br> Retrieves specified existing inject response objects.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### deleteInjectResponse()
endpoints.Competition.**deleteInjectResponses**(self, \*\*kwargs)
<br> Delete the specified inject response object.
<br>**Input**
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the InjectResponse object you'd like to delete.

**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;None
<br>**Example**
```
competition = getCompetition(competitionId = 1)
competition.deleteInjectResponse(injectResponseId = 5)
```

#### createScore()
endpoints.Competition.**createScore**()
<br> Create a new score object.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### editScore()
endpoints.Competition.**editScore**(self, \*\*kwargs)
<br> Edit an existing score object.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### getScore()
endpoints.Competition.**getScore**(self, \*\*kwargs)
<br> Retrieves an existing score.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### getScores()
endpoints.Competition.**getScores**(self, \*\*kwargs)
<br> Retrieves the specified existing score objects.
<br>**Input**
<br>**Output**
<br>**Example**
```
```
* * *

#### deleteScore()
endpoints.Competition.**deleteScore**(self, \*\*kwargs)
<br> Deletes the specified score object.
<br>**Input**
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the Score object you'd like to delete.

**Output**
<br>&nbsp;&nbsp;&nbsp;&nbsp;None
<br>**Example**
```
competition = getCompetition(competitionId = 1)
competition.deleteScore(scoreId = 5)
```

### Team
### Inject
### InjectResponse
### Incident
### IncidentResponse
### Score


## Organization
### edit
### getDeleteable
### getName
### setName
### getUrl
### setUrl
### getDescription
### setDescription
### getMaxMembers
### setMaxMembers
### getMaxCompetitions
### setMaxCompetitions
### getNumMembers
### setNumMembers
### getNumCompetitions
### setNumCompetitions
### getCompetitions
### getCompetition
### createCompetition
### deleteCompetition
### editCompetition
### getMembers
### getMember
### createMember
### deleteMember
### editMember


## User
### count
### edit
### getName
### setName
### getUsername
### setUsername
### getPassword
### setPassword
### getDescription
### setDescription
### getOrganizationId
### setOrganizationId

## Document
### edit
### setContentType
### getContentType
### setFileHash
### getFileHash
### setFilePath
### getfilePath
### setFilename
### getFilename
### setUrlEncodedFilename
### getUrlEncodedFilename
