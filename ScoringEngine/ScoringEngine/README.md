# API Documentation

### getObjects
### getObject
### wrappedSearch

### getCompetition
### getCompetitions
### getOrganization
### getOrganizations
### createOrganization
### editOrganization
### getUsers
### getUser
### editUser

## Competition
ScoringEngine.endpoints.Competition.**count**()<br>
ScoringEngine.endpoints.Competition.**getName**()<br>
This will return the name of the competition as a string.

ScoringEngine.endpoints.Competition.**check**()<br>
This should one day perform a consistency check to make sure the competition doesn't have any conflicting values set. THis may or may not be necessary depending on how much I implement error checking.

#### searchOne()
Competition.searchOne(self, objType, [\*\*kwargs])<br>
I'm not sure if this is still in use. It was used to search for and return a single database object.
##### Input
* objType (required):
<br>&nbsp;&nbsp;&nbsp;&nbsp;This is the class type of the object to search for
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.

##### Output

##### Example

ScoringEngine.endpoints.Competition.**searchMany**()<br>
I'm not sure if this is still in use. It was used to search for and return many database objects.

ScoringEngine.endpoints.Competition.**createTeam**()<br>
ScoringEngine.endpoints.Competition.**editTeam**()<br>
ScoringEngine.endpoints.Competition.**getTeam**()<br>

#### getTeams()
Competition.**getTeams**([**kwargs])
##### Input
* objType (required):
<br>&nbsp;&nbsp;&nbsp;&nbsp;This is the class type of the object to search for
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.

##### Output

##### Example
```
```
* * *
#### deleteTeam()
Competition.**deleteTeam**()
##### Input
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the Team object you'd like to delete.

##### Output
Returns None

##### Example
```
competition = getCompetition(competitionId = 1)
competition.deleteTeam(teamId = 5)
```
* * *

#### createIncident()
Competition.**createIncident**()
##### Input
##### Output
##### Example
```
```
* * *

#### editIncident
Competition.**editIncident**()
##### Input
##### Output
##### Example
```
```
* * *

#### getIncident()
Competition.**getIncident**()
##### Input
##### Output
##### Example
```
```
* * *

#### getIncidents()
Competition.**getIncidents**()
##### Input
##### Output
##### Example
```
```
* * *

#### deleteIncident()
Competition.**deleteIncident**()
##### Input
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the Incident object you'd like to delete.

##### Output
Returns None

##### Example
```
competition = getCompetition(competitionId = 1)
competition.deleteIncident(incidentId = 5)
```
* * *
ScoringEngine.endpoints.Competition.**createIncidentResponse**()
ScoringEngine.endpoints.Competition.**editIncidentResponse**()
ScoringEngine.endpoints.Competition.**getIncidentResponse**()
ScoringEngine.endpoints.Competition.**getIncidentResponses**()

#### deleteIncidentResponse()
Competition.**deleteIncidentResponse**()
##### Input
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the IncidentResponse object you'd like to delete.

##### Output
Returns None

##### Example
```
competition = getCompetition(competitionId = 1)
competition.deleteIncidentResponse(incidentResponseId = 5)
```
ScoringEngine.endpoints.Competition.**createInject**()
ScoringEngine.endpoints.Competition.**editInject**()
ScoringEngine.endpoints.Competition.**getInject**()
ScoringEngine.endpoints.Competition.**getInjects**()

#### deleteInject()
Competition.**deleteInject**()
##### Input
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the Inject object you'd like to delete.

##### Output
Returns None

##### Example
```
competition = getCompetition(competitionId = 1)
competition.deleteInject(injectId = 5)
```
ScoringEngine.endpoints.Competition.**createInjectResponse**()
ScoringEngine.endpoints.Competition.**editInjectResponse**()
ScoringEngine.endpoints.Competition.**getInjectResponse**()
ScoringEngine.endpoints.Competition.**getInjectResponses**()

#### deleteResponse()
Competition.**deleteInjectResponses**()
##### Input
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the InjectResponse object you'd like to delete.

##### Output
Returns None

##### Example
```
competition = getCompetition(competitionId = 1)
competition.deleteInjectResponse(injectResponseId = 5)
```
ScoringEngine.endpoints.Competition.**createScore**()
ScoringEngine.endpoints.Competition.**editScore**()
ScoringEngine.endpoints.Competition.**getScore**()
ScoringEngine.endpoints.Competition.**getScores**()

#### deleteScore()
Competition.**deleteScore**()
##### Input
* \*\*kwargs (optional):
  * serialized:
<br>&nbsp;&nbsp;&nbsp;&nbsp;This defines the type to return. If not provided, this defaults to False.
  * teamId:
<br>&nbsp;&nbsp;&nbsp;&nbsp;The ID for the Score object you'd like to delete.

##### Output
Returns None

##### Example
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
