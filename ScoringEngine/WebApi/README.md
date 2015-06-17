# API Documentation
## Organization
Endpoints:
* [/organizations.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list)
* [/organizations/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details)
* [/organizations/\<id\>/members.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-1)
* [/organizations/\<id\>/members/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-1)
* [/organizations/\<id\>/competitions.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-2)
* [/organizations/\<id\>/competitions/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-2)

### Organizations
#### Resource List
URL: /organizations.json
<br> Description: Lists all organizations
<br> Methods: GET, POST
<br> Example Output:
<pre>[
	{
		"organizationId": 1,
		"name": "Example Organization Name 1",
		"url": "example_organization_name_1",
		"maxMembers": 10,
		"maxCompetitions": 10
	},
	{
		"organizationId": 2,
		"name": "Example Organization Name 2",
		"url": "example_organization_name_2",
		"maxMembers": 10,
		"maxCompetitions": 10
	}
]</pre>
#### Resource Details
URL: /organizations/1.json
<br> Description: Lists extended details about the organization with the id of 1
<br> Methods: GET, PUT, PATCH, DELETE
<br> Example Output:
<pre>{
	"organizationId": 1,
	"name": "Example Organization Name 1",
	"url": "example_organization_name_1",
	"maxMembers": 10,
	"maxCompetitions": 10
	"members": [
		{
			"userId": 1,
			"name": "John Doe",
			"username": "johnd",
			"password": "somehashhere"
		},
		{
			"userId": 2,
			"name": "Jane Doe",
			"username": "janed",
			"password": "somehashhere"
		}
	],
	"competitions": [
		{
			"competitionId": 1,
			"name": "Example Competition 1",
			"url": "example_competition_1",
			"description": "This is an example description."
		},
		{
			"competitionId": 2,
			"name": "Example Competition 2",
			"url": "example_competition_2",
			"description": "This is another example description."
		}
	]
}</pre>
### Organizations - Members
#### Resource List
URL: /organizations/1/members.json
<br> Description: Lists the members of the organization with the id of 1
<br> Methods: GET, POST
<br> Example Output:
<pre>[
	{
		"userId": 1,
		"name": "John Doe",
		"username": "johnd",
		"password": "somehashhere"
	},
	{
		"userId": 2,
		"name": "Jane Doe",
		"username": "janed",
		"password": "somehashhere"
	}
]</pre>
#### Resource Details
URL: /organizations/1/members/1.json
<br>Description: This provides details for the member with id 1 within organization with id 1
<br>Methods: GET, PUT, PATCH, DELETE
<br>Example Output:
<pre>{
	"userId": 2,
	"name": "Jane Doe",
	"username": "janed",
	"password": "somehashhere"
}</pre>
### Organizations - Competitions
#### Resource List
URL: /organizations/1/competitions.json
<br> Description: Lists the competitions of the organization with the id of 1
<br> Methods: GET, POST
<br> Example Output:
<pre>[
	{
		"competitionId": 1,
		"name": "Example Competition 1",
		"url": "example_competition_1",
		"description": "This is an example description."
	},
	{
		"competitionId": 2,
		"name": "Example Competition 2",
		"url": "example_competition_2",
		"description": "This is another example description."
	}
]</pre>
#### Resource Details
URL: /organizations/1/competitions/2.json
<br> Description: Lists the competitions of the organization with the id of 1
<br> Methods: GET, PUT, PATCH, DELETE
<br> Example Output:
<pre>{
	"competitionId": 2,
	"name": "Example Competition 2",
	"url": "example_competition_2",
	"description": "This is another example description."
}</pre>
## Competitions
Endpoints:
* [/competitions.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-3)
* [/competitions/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-3)
* [/competitions/\<id\>/services.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-4)
* [/competitions/\<id\>/services/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-4)
* [/competitions/\<id\>/teams.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-5)
* [/competitions/\<id\>/teams/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-5)
* [/competitions/\<id\>/injects.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-6)
* [/competitions/\<id\>/injects/\<id>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-6)
* [/competitions/\<id\>/injects/\<id\>/responses.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-8)
* [/competitions/\<id\>/injects/\<id\>/responses/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-8)
* [/competitions/\<id\>/incidents.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-7)
* [/competitions/\<id\>/incidents/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-7)
* [/competitions/\<id\>/incidents/\<id\>/responses.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#competitions---incidents---responses)
* [/competitions/\<id\>/incidents/\<id\>/responses/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-11)
* [/competitions/\<id\>/scores.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-8)
* [/competitions/\<id\>/scores/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-8)

### Competitions
#### Resource List
URL: /compeititons.json
<br>Description: Lists all competitions
<br>Methods: GET, POST
<br>Example Output:
<pre>[
	{
		"competitionId": 1,
		"name": "Example Competition 1",
		"url": "example_competition_1",
		"description": "This is an example description."
	},
	{
		"competitionId": 2,
		"name": "Example Competition 2",
		"url": "example_competition_2",
		"description": "This is another example description."
	}
]</pre>
#### Resource Details
URL: /compeititons/2.json
<br> Description: Lists the competition with the id of 2
<br> Methods: GET, PUT, PATCH, DELETE
<br> Example Output:
<pre>{
	"competitionId": 2,
	"name": "Example Competition 2",
	"url": "example_competition_2",
	"description": "This is another example description."
}</pre>
### Competitions - Services
#### Resource List
URL: /compeititons/2/services.json
<br> Description: Lists the services within the competition with the id of 2
<br> Methods: GET, POST
<br> Example Output:
<pre>[
	{
		"serviceId": 1,
		"competitionId": 2,
		"name": "SSH Service",
		"description": "This is an example service description."
	},
	{
		"serviceId": 2,
		"competitionId": 2,
		"name": "HTTP Service",
		"description": "This is another example service description."
	}
]</pre>
#### Resource Details
URL: /compeititons/2/services/1.json
<br> Description: Lists the services within the competition with the id of 2
<br> Methods: GET, PUT, PATCH, DELETE
<br> Example Output:
<pre>{
	"serviceId": 2,
	"competitionId": 2,
	"name": "HTTP Service",
	"description": "This is another example service description."
}</pre>
### Competitions - Teams
#### Resource List
URL: /compeititons/2/teams.json
<br> Description: Lists the teams within the competition with the id of 2
<br> Methods: GET, POST
<br> Example Output:
<pre>[
	{
		"teamId": 1,
		"competitionId": 2,
		"name": "Example Team 1",
		"username": "exampleteam1",
		"password": "password-ex1",
		"description": "This is an example service description."
	},
	{
		"teamId": 2,
		"competitionId": 2,
		"name": "Example Team 2",
		"username": "exampleteam2"
		"password": "password-ex2"
		"description": "This is another example service description."
	}
]</pre>
#### Resource Details
URL: /compeititons/2/teams/2.json
<br> Description: Lists the services within the competition with the id of 2
<br> Methods: GET, PUT, PATCH, DELETE
<br> Example Output:
<pre>{
	"teamId": 2,
	"competitionId": 2,
	"name": "Example Team 2",
	"username": "exampleteam2"
	"password": "password-ex2"
	"description": "This is another example service description."
}</pre>
### Competitions - Injects
#### Resource List
URL: /compeititons/2/injects.json
<br> Description: Lists the injects within the competition with the id of 2
<br> Methods: GET, POST
<br> Example Output:
<pre>[
	{
		"injectId": 1,
		"competitionId": 2,
		"name": "Inject Number 1",
		"description": "This is an example inject description."
		"responses": [
			{
				"injectResponseId": 1,
				"indexId": 1,
				"body": "inject response text",
				"files": [
				]
			},
			{
				"injectResponseId": 2,
				"indexId": 2,
				"body": "inject second response text",
				"files": [
				]
			}
		],
		"files": [
			{
				"name": "file_one.txt",
				"size": "1024"
			}
		]
	},
	{
		"injectId": 2,
		"competitionId": 2,
		"name": "Inject Number 2",
		"description": "This is another example inject description.",
		"responses": [
		],
		"files": [
		]
	}
]</pre>
#### Resource Details
URL: /compeititons/2/injects/1.json
<br> Description: Lists the injects within the competition with the id of 2
<br> Methods: GET, PUT, PATCH, DELETE
<br> Example Output:
<pre>{
	"injectId": 1,
	"competitionId": 2,
	"name": "Inject Number 1",
	"description": "This is an example inject description."
	"responses": [
		{
			"injectResponseId": 1,
			"indexId": 1,
			"body": "inject response text",
			"files": [
			]
		},
		{
			"injectResponseId": 2,
			"indexId": 2,
			"body": "inject second response text",
			"files": [
			]
		}
	],
	"files": [
		{
			"name": "file_one.txt",
			"size": "1024"
		}
	]
}</pre>
### Competitions - Injects - Responses
#### Resource List
URL: /compeititons/2/injects/1/responses.json
<br> Description: Lists the responses to an inject within the competition with the id of 2
<br> Methods: GET, POST
<br> Example Output:
<pre>[
	{
		"injectResponseId": 1,
		"indexId": 1,
		"body": "inject response text",
		"files": [
		]
	},
	{
		"injectResponseId": 2,
		"indexId": 1,
		"body": "inject response text",
		"files": [
		]
	}
]</pre>
#### Resource Details
URL: /compeititons/2/injects/1/responses/1.json
<br> Description: Lists the injects within the competition with the id of 2
<br> Methods: GET, PUT, PATCH, DELETE
<br> Example Output:
<pre>{
	"injectResponseId": 1,
	"indexId": 1,
	"body": "inject response text",
	"files": [
	]
}</pre>
### Competitions - Incidents
#### Resource List
URL: /compeititons/2/incidents.json
<br> Description: Lists the incidents within the competition with the id of 2
<br> Methods: GET, POST
<br> Example Output:
<pre>[
	{
		"incidentId": 1,
		"competitionId": 2,
		"name": "Incident Response 1",
		"body": "This is an example incident response."
		"responses": [
			{
				"incidentResponseId": 1,
				"incidentId": 1,
				"competitionId": 2,
				"body": "some follow up text to incident 1",
				"files": [
				]
			},
			{
				"incidentResponseId": 2,
				"incidentId": 1,
				"competitionId": 2,
				"body": "another follow up text to incident 1",
				"files": [
				]
			}
		],
		"files": [
		]
	},
	{
		"incidentId": 2,
		"competitionId": 2,
		"name": "Incident Response 2",
		"body": "This is another example incident response."
		"responses": [
		],
		"files": [
			{
				"name": "who_done_it.pdf",
				"size": "1024"
			}	
		]
	}
]</pre>
#### Resource Details
URL: /compeititons/2/incidents/1.json
<br> Description: Lists the incidents within the competition with the id of 2
<br> Methods: GET, PUT, PATCH, DELETE
<br> Example Output:
<pre>{
	"incidentId": 1,
	"competitionId": 2,
	"name": "Incident Response 1",
	"body": "This is an example incident response."
	"responses": [
		{
			"incidentResponseId": 1,
			"incidentId": 1,
			"competitionId": 2,
			"body": "some follow up text to incident 1",
			"files": [
			]
		},
		{
			"incidentResponseId": 2,
			"incidentId": 1,
			"competitionId": 2,
			"body": "another follow up text to incident 1",
			"files": [
			]
		}
	],
	"files": [
	]
}</pre>
### Competitions - Incidents - Responses
URL: /compeititons/2/incidents/1/responses.json
<br> Description: Lists the responses to an incident within the competition with the id of 2
<br> Methods: GET, POST
<br> Example Output:
#### Resource List
<pre>[
	{
		"incidentResponseId": 1,
		"incidentId": 1,
		"competitionId": 2,
		"body": "some follow up text to incident 1",
		"files": [
		]
	},
	{
		"incidentResponseId": 2,
		"incidentId": 1,
		"competitionId": 2,
		"body": "another follow up text to incident 1",
		"files": [
		]
	}
]</pre>
#### Resource Details
URL: /compeititons/2/incidents/1/responses/1.json
<br> Description: Lists a specific responses to an incident within the competition with the id of 2
<br> Methods: GET, PUT, PATCH, DELETE
<br> Example Output:
<pre>{
	"incidentResponseId": 1,
	"incidentId": 1,
	"competitionId": 2,
	"body": "some follow up text to incident 1",
	"files": [
	]
}</pre>
### Competitions - Scores
#### Resource List
URL: /compeititons/2/scores.json
<br> Description: Lists the scores within the competition with the id of 2
<br> Methods: GET, POST
<br> Example Output:
<pre>[
	{
		"scoreId": 1,
		"competitionId": 2,
		"serviceId": 1,
		"teamId": 1,
		"value": 100,
		"messages": {
			"info": "Service was accessible.",
			"warning": "",
			"error": ""
		}
	},
	{
		"scoreId": 2,
		"competitionId": 2,
		"serviceId": 1,
		"teamId": 2,
		"value": 0,
		"messages": {
			"info": "",
			"warning": "",
			"error": "Service unavailable."
		}
	}
]</pre>
#### Resource Details
URL: /compeititons/2/scores/2.json
<br> Description: Provides details for the score with id 2
<br> Methods: GET, PUT, PATCH, DELETE
<br> Example Output:
<pre>{
	"scoreId": 2,
	"competitionId": 2,
	"serviceId": 1,
	"teamId": 2,
	"value": 0,
	"messages": {
		"info": "",
		"warning": "",
		"error": "Service unavailable."
	}
}</pre>
## Plugins
Endpoints:
* [/plugins.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-9)
* [/plugins/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-9)

### Plugins
#### Resource List
URL: /plugins.json
<br> Description: Lists all plugins
<br> Methods: GET, POST
<br> Example Output:
<pre>[
	{
		"name": "SSH Plugin",
		"description": "Scores SSH services",
		"file": {
			"fileId": 5,
			"name": "cssef_ssh_plugin.py",
			"size": 1024
		}
	},
	{
		"name": "FTP Plugin",
		"description": "Scores FTP services",
		"file": {
			"fileId": 6,
			"name": "cssef_ftp_plugin.py",
			"size": 1024
		}
	}
]</pre>
#### Resource Details
URL: /plugins/1.json
<br> Description: Provides details for plugin with id of 2
<br> Methods: GET, PUT, PATCH, DELETE
<br> Example Output:
<pre>{
	"name": "SSH Plugin",
	"description": "Scores SSH services",
	"file": {
		"fileId": 5,
		"name": "cssef_ssh_plugin.py",
		"size": 1024
	}
}</pre>
## Files
Endpoints:
* [/files.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-11)
* [/files/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-11)

### Files
#### Resource List
URL: /files.json
<br> Description: Lists all files
<br> Methods: GET, POST
<br> Example Output:
<pre>[
	{
		"fileId": 5,
		"name": "cssef_ssh_plugin.py",
		"size": 1024,
		"md5": "some md5 hash"
	},
	{
		"fileId": 6,
		"name": "cssef_ftp_plugin.py",
		"size": 1024,
		"md5": "some md5 hash"
	}
]</pre>
#### Resource Details
URL: /files/6.json
<br> Description: Provides details for file with id 6
<br> Methods: GET, PUT, PATCH, DELETE
<br> Example Output:
<pre>{
	"fileId": 6,
	"name": "cssef_ftp_plugin.py",
	"size": 1024,
	"md5": "some md5 hash"
}</pre>
