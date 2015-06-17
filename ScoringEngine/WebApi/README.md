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
	"maxCompetitions": 10,
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
		"last_login": "2015-06-17 00:13:14"
		"teamname": "Example Team 1",
		"loginname": "exampleteam1",
		"password": "password-ex1",
		"networkCidr": "192.168.1.0\24",
		"scoreConfigurations": "{}"
	},
	{
		"teamId": 2,
		"competitionId": 2,
		"last_login": "2015-06-17 00:13:14"
		"teamname": "Example Team 2",
		"loginname": "exampleteam2",
		"password": "password-ex2",
		"networkCidr": "192.168.2.0\24",
		"scoreConfigurations": "{}"
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
	"last_login": "2015-06-17 00:13:14"
	"teamname": "Example Team 2",
	"loginname": "exampleteam2",
	"password": "password-ex2",
	"networkCidr": "192.168.2.0\24",
	"scoreConfigurations": "{}"
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
		"requireResponse": True,
		"manualDelivery": False,
		"datetimeDelivery": "2015-06-17 00:13:14",
		"datetimeResponseDue": "2015-06-17 00:13:15",
		"datetimeResponseClose": "2015-06-17 00:13:15",
		"title": "Suspicious Network Traffic",
		"content": "Attached is a pcap file of some suspicious activity. Find out what happened!",
		"responses": [
			{
				"injectResponseId": 1,
				"competitionId": 2,
				"teamId": 1,
				"injectId": 1,
				"datetime": "2015-06-17 00:13:14",
				"content": "There was a bruteforce attack on the root user account via telnet.",
				"documents": [
				]
			},
			{
				"injectResponseId": 2,
				"competitionId": 2,
				"teamId": 1,
				"injectId": 1,
				"datetime": "2015-06-17 00:13:14",
				"content": "The attacker got in and ran 'dd if=/dev/urandom of=/dev/sda bs=1'",
				"documents": [
				]
			}
		],
		"documents": [
			{
				"documentId": 6,
				"contentType": "text/plain",
				"fileHash": "md5hashofthefile",
				"filePath": "/opt/cssef/file_storage/dmz_network.pcap",
				"filename": "dmz_network.pcap"
				"urlEncodedFilename": "dmz_network.pcap"
			}
		]
	},
	{
		"injectId": 2,
		"competitionId": 2,
		"requireResponse": True,
		"manualDelivery": True,
		"datetimeDelivery": "",
		"datetimeResponseDue": "2015-06-17 00:13:14",
		"datetimeResponseClose": "2015-06-17 00:14:14",
		"title": "Change all passwords",
		"content": "Please change all of the passwords!",
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
	"requireResponse": True,
	"manualDelivery": False,
	"datetimeDelivery": "2015-06-17 00:13:14",
	"datetimeResponseDue": "2015-06-17 00:13:15",
	"datetimeResponseClose": "2015-06-17 00:13:15",
	"title": "Suspicious Network Traffic",
	"content": "Attached is a pcap file of some suspicious activity. Find out what happened!",
	"responses": [
		{
			"injectResponseId": 1,
			"competitionId": 2,
			"teamId": 1,
			"injectId": 1,
			"datetime": "2015-06-17 00:13:14",
			"content": "There was a bruteforce attack on the root user account via telnet.",
			"documents": [
			]
		},
		{
			"injectResponseId": 2,
			"competitionId": 2,
			"teamId": 1,
			"injectId": 1,
			"datetime": "2015-06-17 00:13:14",
			"content": "The attacker got in and ran 'dd if=/dev/urandom of=/dev/sda bs=1'",
			"documents": [
			]
		}
	],
	"documents": [
		{
			"documentId": 6,
			"contentType": "text/plain",
			"fileHash": "md5hashofthefile",
			"filePath": "/opt/cssef/file_storage/dmz_network.pcap",
			"filename": "dmz_network.pcap"
			"urlEncodedFilename": "dmz_network.pcap"
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
		"competitionId": 2,
		"teamId": 1,
		"injectId": 1,
		"datetime": "2015-06-17 00:13:14",
		"content": "inject response text",
		"documents": [
		]
	},
	{
		"injectResponseId": 2,
		"competitionId": 2,
		"teamId": 1,
		"injectId": 1,
		"datetime": "2015-06-17 00:13:14",
		"content": "another inject response text",
		"documents": [
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
	"competitionId": 2,
	"teamId": 1,
	"injectId": 2,
	"datetime": "2015-06-17 00:13:14",
	"content": "inject response text",
	"documents": [
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
		"body": "This is an example incident response.",
		"responses": [
			{
				"incidentResponseId": 1,
				"competitionId": 2,
				"teamId": 1,
				"incidentId": 1,
				"datetime": "2015-06-17 00:13:14",
				"content": "some follow up text to incident 1",
				"documents": [
				]
			},
			{
				"incidentResponseId": 2,
				"competitionId": 2,
				"teamId": 1,
				"incidentId": 1,
				"datetime": "2015-06-17 00:13:14",
				"content": "some more follow up text to incident 1",
				"documents": [
				]
			}
		],
		"documents": [
		]
	},
	{
		"incidentId": 2,
		"competitionId": 2,
		"name": "Incident Response 2",
		"body": "This is another example incident response.",
		"responses": [
		],
		"documents": [
			{
				"documentId": 5,
				"contentType": "text/pdf",
				"fileHash": "md5hashofthefile",
				"filePath": "/opt/cssef/file_storage/who_done_it.pdf",
				"filename": "who_done_it.pdf"
				"urlEncodedFilename": "who_done_it.pdf"
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
	"body": "This is an example incident response.",
	"responses": [
		{
			"incidentResponseId": 1,
			"competitionId": 2,
			"teamId": 1,
			"incidentId": 1,
			"datetime": "2015-06-17 00:13:14",
			"content": "some follow up text to incident 1",
			"documents": [
			]
		},
		{
			"incidentResponseId": 2,
			"competitionId": 2,
			"teamId": 1,
			"incidentId": 1,
			"datetime": "2015-06-17 00:13:14",
			"content": "some more follow up text to incident 1",
			"documents": [
			]
		}
	],
	"documents": [
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
		"competitionId": 2,
		"teamId": 1,
		"incidentId": 1,
		"datetime": "2015-06-17 00:13:14",
		"content": "some follow up text to incident 1",
		"documents": [
		]
	},
	{
		"incidentResponseId": 2,
		"competitionId": 2,
		"teamId": 1,
		"incidentId": 1,
		"datetime": "2015-06-17 00:13:14",
		"content": "some more follow up text to incident 1",
		"documents": [
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
	"competitionId": 2,
	"teamId": 1,
	"incidentId": 1,
	"datetime": "2015-06-17 00:13:14",
	"content": "some follow up text to incident 1",
	"documents": [
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
		"datetime": "2015-06-17 00:13:14",
		"value": 10,
		"messagesInfo": "Service is up!",
		"messagesWarning": "",
		"messagesError": ""
	},
	{
		"scoreId": 2,
		"competitionId": 2,
		"serviceId": 1,
		"teamId": 2,
		"datetime": "2015-06-17 00:13:14",
		"value": 0,
		"messagesInfo": "",
		"messagesWarning": "",
		"messagesError": "Service appears down!"
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
	"datetime", "2015-06-17 00:13:14",
	"value": 0,
	"messagesInfo": "",
	"messagesWarning": "",
	"messagesError": "Service appears down!"
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
		"description": "Plugin to scores SSH services",
		"document": {
			"documentId": 3,
			"contentType": "text/plain",
			"fileHash": "md5hashofthescript",
			"filePath": "/opt/cssef/file_storage/cssef_ssh_plugin.py",
			"filename": "cssef_ssh_plugin.py"
			"urlEncodedFilename": "cssef_ssh_plugin.py"
		}
	},
	{
		"name": "FTP Plugin",
		"description": "Plugin to score FTP services",
		"document": {
			"documentId": 4,
			"contentType": "text/plain",
			"fileHash": "md5hashofthescript",
			"filePath": "/opt/cssef/file_storage/cssef_ftp_plugin.py",
			"filename": "cssef_ftp_plugin.py"
			"urlEncodedFilename": "cssef_ftp_plugin.py"
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
	"description": "Plugin to scores SSH services",
	"document": {
		"documentId": 3,
		"contentType": "text/plain",
		"fileHash": "md5hashofthescript",
		"filePath": "/opt/cssef/file_storage/cssef_ssh_plugin.py",
		"filename": "cssef_ssh_plugin.py"
		"urlEncodedFilename": "cssef_ssh_plugin.py"
	}
}</pre>
## Documents
Endpoints:
* [/documents.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-list-11)
* [/documents/\<id\>.json](https://github.com/bplower/cssef/blob/refactor/ScoringEngine/WebApi/README.md#resource-details-11)

### Documents
#### Resource List
URL: /documents.json
<br> Description: Lists all files
<br> Methods: GET, POST
<br> Example Output:
<pre>[
	{
		"documentId": 1,
		"contentType": "text/plain",
		"fileHash": "md5hashofthefile",
		"filePath": "/opt/cssef/file_storage/example_file.txt",
		"filename": "example_file.txt"
		"urlEncodedFilename": "example_file.txt"
	},
	{
		"documentId": 2,
		"contentType": "text/pdf",
		"fileHash": "md5hashofthepdf",
		"filePath": "/opt/cssef/file_storage/intrusion_report.pdf",
		"filename": "intrusion_report.pdf"
		"urlEncodedFilename": "intrusion_report.pdf"
	}
]</pre>
#### Resource Details
URL: /documents/6.json
<br> Description: Provides details for file with id 6
<br> Methods: GET, PUT, PATCH, DELETE
<br> Example Output:
<pre>{
	"documentId": 1,
	"contentType": "text/plain",
	"fileHash": "md5hashofthefile",
	"filePath": "/opt/cssef/file_storage/example_file.txt",
	"filename": "example_file.txt"
	"urlEncodedFilename": "example_file.txt"
}</pre>
