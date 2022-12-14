# Boats and Loads API Documentation

# Table of Contents
1. [Table of Contents](#table-of-contents)
2. [Getting Started](#getting-started)
3. [Data Model](#data-model)
   1. [Boats](#Boats)
   2. [Users](#Users)
   3. [Loads](#Loads)
4. [Create a Boat](#create-a-boat)
5. [Get a Boat](#get-a-boat)
6. [List all Boats](#list-all-boats)
7. [Patch a Boat](#patch-a-boat)
8. [Edit a Boat](#edit-a-boat)
9. [Delete a Boat](#delete-a-boat)
10. [Create a Load](#create-a-load)
11. [Get a Load](#get-a-load)
12. [List all Loads](#list-all-loads)
13. [Patch a Load](#patch-a-load)
14. [Edit a Load](#edit-a-load) 
15. [Delete a Load](#delete-a-load) 
16. [Assign a Load to a Boat](#assign-a-load-to-a-boat)
17. [Remove a Load from a Boat](#remove-a-load-from-a-boat)

________________

## Getting Started

URL: https://cs493-final-towlerj.uk.r.appspot.com/ 

Login URL: https://cs493-final-towlerj.uk.r.appspot.com/ 

## Data Model 
The app stores two kinds of entities in Datastore, Boats and Slips. 
### Boats 
**Relationship to Loads:** A boat can have many loads that it carries and there is no limit, but a load can only be on one ship at a time.

| Property   | Data Type | Notes                                                                                                                                                                                                     | Required? |
|------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| id         | Integer   | The id of the boat. Datastore automatically generates it. This will be the path parameter to identify a boat.                                                                                             | n/a       |
| name       | String    | Name of the boat as a string.                                                                                                                                                                             | yes       |
| type       | String    | Type of the boat. E.g., Sailboat, Catamaran, etc.                                                                                                                                                         | yes       |
| length     | Integer   | The length of the boat in feet. Can be given as a string, but must be able to be cast to an integer.                                                                                                      | yes       |
| captain_id | String    | The owner id of the user that owns the boat. Cannot be null. Corresponds with the ???sub??? property from Users. Used to validate ownership of the boat from a request. Not directly used as a path parameter | n/a       |
| loads      | Array     | A list of Loads being carried by the boat.                                                                                                                                                                | no        |

### Users
**Relationship to Boats:** One user may have many boats, but a boat may only have one user/captain.

| Property    | Data Type | Notes                                                                                                               | Required |
|-------------|-----------|---------------------------------------------------------------------------------------------------------------------|----------|
| id          | Integer   | The id of the user. Datastore automatically generates this. Not used to identify any resources.                     | n/a      |
| sub         | String    | The unique id for this user that is used to identify the captain of a boat resource. Obtained from id_token in JWT. | n/a      |
| given_name  | String    | The user???s first/given name. Obtained from People API.                                                              | yes      |
| family name | String    | The user???s last/family name Obtained from People API                                                                | yes      |

### Loads
**Relationship to Boats:** A load can be carried by only one boat, but a boat may carry many loads.

| Property      | Data Type | Notes                                                                                                         | Required? |
|---------------|-----------|---------------------------------------------------------------------------------------------------------------|-----------|
| id            | Integer   | The id of the load. Datastore automatically generates it. This will be the path parameter to identify a load. | n/a       |
| volume        | Integer   | The volume of the load. Can be given as a string, but must be able to be cast to an integer.                  | yes       |
| carrier       | Boat      | The boat entity currently carrying this load. Can be null if the load is not being carried by any boats.      | no        |
| item          | String    | The item in the load. Any valid string is acceptable.                                                         | yes       |
| creation_date | String    | The date the load was created. Any valid date format is acceptable.                                           | yes       |


# Create a Boat 
Allows the user to create a new boat. 

```POST /boats```

## Request 
### Request Headers

| Name         | Value            | Required? |
|--------------|------------------|-----------|
| Accept       | application/json | yes       |
| Content-type | application/json | yes       |

### Path Parameters 
None

### Query Parameters
None

### Authorization
JWT, Required

### Request Body 
Required 

### Request Body Format 
JSON 

### Request JSON Attributes 

| Name   | Description                                       | Required? |
|--------|---------------------------------------------------|-----------|
| name   | The name of the boat.                             | yes       |
| type   | The type of boat. E.g., Sailboat, Catamaran, etc. | yes       |
| length | Length of the boat in feet.                       | yes       |

### Request Body Example 
```json
{ 
 "name": "Sea Witch", 
 "type": "Catamaran", 
 "length": 28 
}
```

## Response 
### Response Body Format 
JSON, None

### Response Statuses 

| Outcome | Status Code                | Notes                                                                                                                                                                                                                         |
|---------|----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Success | 201 Created                |                                                                                                                                                                                                                               |
| Failure | 400 Bad Request            | If the request is missing any of the 3 required attributes,  the boat will not be created, and 400 status code will be returned. Similarly, if the length is not a valid integer or can???t be converted, 400 will be returned. |
| Failure | 401 Unauthorize            | JWT authorization is missing or invalid in request header.                                                                                                                                                                    |
| Failure | 406 Not Acceptable         | Accept header does not include JSON.                                                                                                                                                                                          |
| Failure | 415 Unsupported Media Type | Content-type header is not JSON.                                                                                                                                                                                              |
	
### Response Examples
#### Success 
```javascript
Status: 201 Created 
{
    "captain_id": "102032202542673265884",
    "id": 5132758833692672,
    "length": 25,
    "loads": [],
    "name": "Jolly Roger",
    "self": "http://localhost:5000/boats/5132758833692672",
    "type": "Schooner"
}
```

#### Failure
```javascript
Status: 400 Bad Request 
{
    "Error": "The request object is missing at least one of the required attributes"
}

Status: 400 Bad Request
{
    "error": "Length must be an integer."
}

Status: 401 Unauthorized
{
    "error": "JWT missing, expired, or invalid"
}

Status: 406 Not Acceptable
No response body

Status: 415 Unsupported Media Type
No response body
```

# Get a Boat 
Allows the user to retrieve details of an existing boat that they own.

```GET /boats/:boat_id```

## Request 
### Request Headers

| Name         | Value            | Required? |
|--------------|------------------|-----------|
| Accept       | application/json | yes       |
| Content-type | application/json | yes       |

### Path Parameters 

| Name    | Description    |
|---------|----------------|
| boat_id | ID of the boat |

### Query Parameters
None

### Authorization
JWT, Required

### Request Body 
None

## Response 
### Response Body Format 
JSON, None

### Response Statuses 

| Outcome | Status Code        | Notes                                                            |
|---------|--------------------|------------------------------------------------------------------|
| Success | 200 OK             |                                                                  |
| Failure | 401 Unauthorized   | JWT in the Authorization header is missing, invalid, or expired. |
| Failure | 403 Forbidden      | Requested boat belongs to another user.                          |
| Failure | 404 Not Found      | No boat with this boat_id exists.                                |
| Failure | 406 Not Acceptable | Accept header does not include JSON                                 |

### Response Examples 
#### Success 
```json
Status: 200 OK 
{
    "captain_id": "102032202542673265884",
    "id": 5132758833692672,
    "length": 25,
    "loads": [],
    "name": "Jolly Roger",
    "self": "http://localhost:5000/boats/5132758833692672",
    "type": "Schooner"
}
```
	
#### Failure
```json
Status: 401 Unauthorized
{
    "error": "JWT missing, expired, or invalid"
}


Status: 403 Forbidden
{
    "error": "The boat with this boat id is owned by another captain."
}


Status: 404 Not Found 
{  
    "Error": "No boat with this boat_id exists" 
}


Status: 406 Not Acceptable
No response body
```

# List all Boats 
List all the boats associated with the requesting user.

```GET /boats```

## Request 
### Request Headers
| Name         | Value            | Required? |
|--------------|------------------|-----------|
| Accept       | application/json | yes       |
| Content-type | application/json | yes       |

### Path Parameters 
None 

### Query Parameters
| Name   | Description                                                   |
|--------|---------------------------------------------------------------|
| offset | The offset from the start of the total boats in the database. |
| limit  | The number of boats to return.                                |

### Request Body 
None 

## Response 
### Response Body Format 
JSON, None

### Response Statuses 

| Outcome | Status Code         | Notes                                |
|--------|---------------------|--------------------------------------|
| Success | 200 OK              |                                      |
| Failure | 401 Unauthorized.   | JWT is missing, invalid, or expired. |
| Failure | 406 Not Acceptable. | Accept Header does not include JSON. |

### Response Examples 
#### Success
```json
Status: 200 OK 
{
    "boats": [
        {
            "captain_id": "102032202542673265884",
            "id": 4790176471580672,
            "length": 25,
            "loads": [],
            "name": "Jolly Roger",
            "self": "http://localhost:5000/boats/4790176471580672",
            "type": "Schooner"
        },
        {
            "captain_id": "102032202542673265884",
            "id": 4857241781927936,
            "length": 25,
            "loads": [],
            "name": "Jolly Roger",
            "self": "http://localhost:5000/boats/4857241781927936",
            "type": "Schooner"
        },
        {
            "captain_id": "102032202542673265884",
            "id": 5071651448291328,
            "length": 25,
            "loads": [],
            "name": "Jolly Roger",
            "self": "http://localhost:5000/boats/5071651448291328",
            "type": "Schooner"
        },
        {
            "captain_id": "102032202542673265884",
            "id": 5107442887163904,
            "length": 25,
            "loads": [],
            "name": "Jolly Roger",
            "self": "http://localhost:5000/boats/5107442887163904",
            "type": "Schooner"
        },
        {
            "captain_id": "102032202542673265884",
            "id": 5114509786087424,
            "length": 25,
            "loads": [],
            "name": "Jolly Roger",
            "self": "http://localhost:5000/boats/5114509786087424",
            "type": "Schooner"
        }
    ],
    "next": "http://localhost:5000/boats/?limit=5&offset=5",
    "total": 29
}
```

#### Failure
```json
Status: 401 Unauthorized
{
    "error": "JWT missing, expired, or invalid"
}

Status: 406 Not Acceptable
No response body
```

# Patch a Boat
Allows the user to edit some properties of a boat.

```PATCH /boats/:boat_id```

## Request
### Request Headers
| Name         | Value            | Required? |
|--------------|------------------|-----------|
| Accept       | application/json | yes       |
| Content-Type | application/json | yes       |

### Path Parameters
| Name    | Description     |
|---------|-----------------|
| boat_id | ID of the boat. |

### Query Parameters
None

### Authorization
JWT, Required

### Request Body
Required

### Request Body Format
JSON

### Request JSON Attributes 

| Name   | Description                                           | Required? |
|--------|-------------------------------------------------------|-----------|
| name   | The name of the boat.                                 | no        |
| type   | The type of the baot. E.g., Sailboat, Catamaran, etc. | no        |
| length | The length of the boat in feet.                       | no        |

### Request Body Example 
```json
{ 
 "name": "Sea Witch", 
 "type": "Catamaran" 
}
```

## Response
### Response Body Format
JSON, None

### Response Statuses

| Outcome | Status Code                | Notes                                                       |
|---------|----------------------------|-------------------------------------------------------------|
| Success | 200 OK                     |                                                             |
| Failure | 400 Bad Request            | Length is not a valid integer or can???t be converted to one. |
| Failure | 401 Unauthorized           | JWT is missing, invalid, or expired.                        |
| Failure | 403 Forbidden              | Boat belongs to another user.                               |
| Failure | 404 Not Found              | No boat with this boat_id exists.                           |
| Failure | 406 Not Acceptable         | Accept header does not include JSON.                        |
| Failure | 415 Unsupported Media Type | Content-Type header does not include JSON.                  |

### Response Examples
#### Success
```json
Status: 200 OK
{
    "captain_id": "102032202542673265884",
    "id": 5132758833692672,
    "length": 25,
    "loads": [],
    "name": "Black Pearl",
    "self": "http://localhost:5000/boats/51327588336926725132758833692672",
    "type": "Schooner"
}
```

#### Failure
```json
Status: 400 Bad Request
{
    "error": "Length must be an integer."
}

Status: 401 Unauthorized
{
    "error": "JWT missing, expired, or invalid"
}

Status: 403 Forbidden
{
    "error": "The boat with this boat id is owned by another captain."
}

Status: 404 Not Found
{
    "Error": "No boat with this boat_id exists."
}

Status: 406 Not Acceptable
No response body

Status: 415 Unsupported Media Type
No response body
```

# Edit a Boat 
Allows you to edit a boat. 

```PUT /boats/:boat_id```

## Request 
### Request Headers
| Name         | Value            | Required? |
|--------------|------------------|-----------|
| Accept       | application/json | yes       |
| Content-type | application/json | yes       |

### Path Parameters
| Name    | Description    |
|---------|----------------|
| boat_id | ID of the boat |

### Query Parameters
None

### Authorization
JWT, Required

### Request Body 
Required 

### Request Body Format 
JSON 

### Request JSON Attributes 
| Name   | Description                                           | Required? |
|--------|-------------------------------------------------------|-----------|
| name   | The name of the boat.                                 | yes       |
| type   | The type of the baot. E.g., Sailboat, Catamaran, etc. | yes       |
| length | The length of the boat in feet.                       | yes       |
	
### Request Body Example 
```json
{ 
 "name": "Sea Witch", 
 "type": "Catamaran", 
 "length": 99 
}
```
	
## Response
### Response Body Format
JSON, None

### Response Statuses
| Outcome | Status Code                | Notes                                                                                                               |
|---------|----------------------------|---------------------------------------------------------------------------------------------------------------------|
| Success | 200 OK                     |                                                                                                                     |
| Failure | 400 Bad Request            | Request body is missing one of the required attributes. Length is not a valid integer or can???t be converted to one. |
| Failure | 401 Unauthorized           | JWT is missing, invalid, or expired.                                                                                |
| Failure | 403 Forbidden              | Boat belongs to another user.                                                                                       |
| Failure | 404 Not Found              | No boat with this boat_id exists.                                                                                   |
| Failure | 406 Not Acceptable         | Accept header does not include JSON.                                                                                |
| Failure | 415 Unsupported Media Type | Content-Type header does not include JSON                                                                           |

###	Response Examples
#### Success
```json
Status: 200 OK
{
    "captain_id": "102032202542673265884",
    "id": 5132758833692672,
    "length": 26,
    "loads": [],
    "name": "Black Pearl",
    "self": "http://localhost:5000/boats/51327588336926725132758833692672",
    "type": "Cutlass"
}
```

#### Failure
```json
Status: 400 Bad Request
{
    "Error": "The request object is missing at least one of the required attributes"
}
{
    "error": "Length must be an integer."
}

Status: 401 Unauthorized
{
    "error": "JWT missing, expired, or invalid"
}

Status: 403 Forbidden
{
    "error": "The boat with this boat id is owned by another captain."
}

Status: 404 Not Found
{
    "Error": "No boat with this boat_id exists."
}

Status: 406 Not Acceptable
No response body

Status: 415 Unsupported Media Type
No response body
```

# Delete a Boat 
Allows you to delete a boat. If the boat is carrying any loads, those loads will not be deleted and will no longer be listed as carried

```DELETE /boats/:boat_id```

## Request 
### Request Headers
| Name         | Value            | Required? |
|--------------|------------------|-----------|
| Accept       | application/json | yes       |
| Content-type | application/json | yes       |

### Path Parameters 

| Name    | Description    |
|---------|----------------|
| boat_id | ID of the boat |

### Query Parameters
None

### Authorization
JWT, Required

### Request Body 
None 

## Response 
### Response Body Format 
JSON, None 

### Response Statuses
| Outcome | Status Code      | Notes                                            |
|---------|------------------|--------------------------------------------------|
| Success | 204 No Content   |                                                  |
| Failure | 401 Unauthorized | JWT missing, invalid, or expired.                |
| Failure | 403 Forbidden    | Boat with this boat_id is owned by another user. |
| Failure | 404 Not Found    | No boat with this boat_id exists.                |
	
### Response Examples 
#### Success 
```json
Status: 204 No Content
No response body
```
	
#### Failure
```json
Status: 401 Unauthorized
{
    "error": "JWT missing, expired, or invalid"
}

Status: 403 Forbidden
{
    "error": "The boat with this boat id is owned by another captain."
}

Status: 404 Not Found
{
    "Error": "No boat with this boat_id exists."
}
```

# Create a Load
Allows you to create a new load.

```POST /loads```

## Request
### Request Headers
| Name         | Value            | Required? |
|--------------|------------------|-----------|
| Accept       | application/json | yes       |
| Content-type | application/json | yes       |

### Path Parameters
None

### Query Parameters
None

### Authorization
None

### Request Body 
Required 

### Request Body Format 
JSON 

### Request JSON Attributes 

| Name          | Description                   | Required? |
|---------------|-------------------------------|-----------|
| volume        | The volume of the load        | yes       |
| item          | The item held in the load     | yes       |
| creation_date | The date the load was created | yes       |
	
### Request Body Example 
```json
{
  "volume": 5,
  "item": "LEGO Blocks",
  "creation_date": "10/18/2021"
}
```

## Response 
### Response Body Format 
JSON, None

### Response Statuses 
| Outcome | Status Code                | Notes                                                                                                                          |
|---------|----------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Success | 201 Created                |                                                                                                                                |
| Failure | 400 Bad Request            | If the request is missing any of the required attributes, the load must not be created, and 400 status code must be  returned. |
| Failure | 406 Not Acceptable         | Accept header does not include JSON.                                                                                           |
| Failure | 415 Unsupported Media Type | Content-type header is not JSON.                                                                                               |
	
### Response Examples  
#### Success 
```json
Status: 201 Created 
{
    "carrier": null,
    "creation_date": "12/01/22",
    "id": 6206500422811648,
    "item": "paper",
    "self": "http://localhost:5000/loads/6206500422811648",
    "volume": 25
}
```
	
#### Failure
```json
Status: 400 Bad Request 
{
    "Error": "The request object is missing at least one of the required attributes"
}
{
    "error": "Volume must be an integer."
}
        
Status: 406 Not Acceptable
No response body
        
Status: 415 Unsupported Media Type
No response body
```

# Get a Load
Allows you to get an existing load

```GET /loads/:load_id```

## Request 
### Request Headers
| Name         | Value            | Required? |
|--------------|------------------|-----------|
| Accept       | application/json | yes       |
| Content-type | application/json | yes       |

### Path Parameters
| Name    | Description     |
|---------|-----------------|
| load_id | ID of the load. |

### Query Parameters
None

### Authorization
None

### Request Body 
None 

## Response 
### Response Body Format 
JSON, None

### Response Statuses 

| Outcome | Status Code        | Notes                               |
|---------|--------------------|-------------------------------------|
| Success | 200 OK             |                                     |
| Failure | 404 Not Found      | No load with this load_id exists.   |
| Failure | 406 Not Acceptable | Accept Header does not include JSON |

### Response Examples
#### Success 
```json
Status: 200 OK 
{
    "carrier": null,
    "creation_date": "12/01/22",
    "id": 6206500422811648,
    "item": "paper",
    "self": "http://localhost:5000/loads/6206500422811648",
    "volume": 25
}
```
	
#### Failure
```json
Status: 404 Not Found 
{
    "Error": "No load with this load_id exists"
}
        
Status: 406 Not Acceptable
No response Body
```

# List all Loads

List all the loads. 

```GET /loads```

## Request 
### Request Headers
| Name         | Value            | Required? |
|--------------|------------------|-----------|
| Accept       | application/json | yes       |
| Content-type | application/json | no        |

### Query Parameters
| Name   | Description                                                   |
|--------|---------------------------------------------------------------|
| offset | The offset from the start of the total loads in the database. |
| limit  | The number of loads to return.                                |
	
### Path Parameters 
None

### Authorization
None

### Request Body 
None

## Response 
### Response Body Format 
JSON 

### Response Statuses
| Outcome | Status Code        | Notes                                |
|---------|--------------------|--------------------------------------|
| Success | 200 OK             |                                      |
| Failure | 406 Not Acceptable | Accept header does not include JSON. |

### Response Examples 
#### Success
```json
Status: 200 OK 
{
    "loads": [
        {
            "carrier": null,
            "creation_date": "12/01/22",
            "id": 4822282560077824,
            "item": "paper",
            "self": "http://localhost:5000/loads/4822282560077824",
            "volume": 25
        },
        {
            "carrier": null,
            "creation_date": "12/01/22",
            "id": 5067028654194688,
            "item": "paper",
            "self": "http://localhost:5000/loads/5067028654194688",
            "volume": 25
        },
        {
            "carrier": null,
            "creation_date": "12/01/22",
            "id": 5080600515969024,
            "item": "paper",
            "self": "http://localhost:5000/loads/5080600515969024",
            "volume": 25
        },
        {
            "carrier": null,
            "creation_date": "12/01/22",
            "id": 5087093063680000,
            "item": "paper",
            "self": "http://localhost:5000/loads/5087093063680000",
            "volume": 25
        },
        {
            "carrier": null,
            "creation_date": "12/01/22",
            "id": 5090685099180032,
            "item": "paper",
            "self": "http://localhost:5000/loads/5090685099180032",
            "volume": 25
        }
    ],
    "next": "http://localhost:5000/loads/?limit=5&offset=5",
    "total": 31
}
```

#### Failure
```json
Status: 406 Not Acceptable
No response Body
```

# Patch a Load
Allows the user to edit some attributes of the given load.

```PATCH /loads/:load_id```

## Request
### Request Headers
| Name         | Value            | Required? |
|--------------|------------------|-----------|
| Accept       | application/json | yes       |
| Content-type | application/json | yes       |

### Path Parameters
None

### Query Parameters
None

### Authorization
None

### Request Body
Required

### Request Body Format
JSON

### Request JSON Attributes 
| Name          | Description                    | Required? |
|---------------|--------------------------------|-----------|
| volume        | The volume of the load.        | no        |
| item          | The item held in the load.     | no        |
| creation_date | The date the load was created. | no        |

## Response
### Response Body Format
JSON, None

### Response Statuses
| Outcome | Status Code                | Notes                                  |
|---------|----------------------------|----------------------------------------|
| Success | 200 OK                     |                                        |
| Failure | 400 Bad Request            | Volume is not an integer.              |
| Failure | 404 Not Found              | Load with this load_id does not exist. |
| Failure | 406 Not Acceptable         | Accept header does not include JSON    |
| Failure | 415 Unsupported Media Type | Content-Type header is not JSON        |

### Response Examples
#### Success
```json
Status: 200 OK
{
    "carrier": null,
    "creation_date": "12/01/22",
    "id": 6206500422811648,
    "item": "paper",
    "self": "http://localhost:5000/loads/6206500422811648",
    "volume": 26
}
```

#### Failure
```json
Status: 400 Bad Request
{
    "error": "Volume must be an integer."
}
        
Status: 404 Not Found
{
    "Error": "No load with this load_id exists"
}
        
Status: 406 Not Acceptable
No response body

Status: 415 Unsupported Media Type
No response body
```
	

# Edit a Load
Allows the user to edit the given load.

```PUT /loads/:load_id```

## Request
### Request Headers
| Name         | Value            | Required? |
|--------------|------------------|-----------|
| Accept       | application/json | yes       |
| Content-type | application/json | yes       |

### Path Parameters
None

### Query Parameters
None

### Authorization
None

### Request Body
Required

### Request Body Format
JSON

### Request JSON Attributes 
| Name          | Description                    | Required? |
|---------------|--------------------------------|-----------|
| volume        | The volume of the load.        | yes       |
| item          | The item held in the load.     | yes       |
| creation_date | The date the load was created. | yes       |

## Response
### Response Body Format
JSON, None

### Response Statuses
| Outcome | Status Code                | Notes                                                               |
|---------|----------------------------|---------------------------------------------------------------------|
| Success | 200 OK                     |                                                                     |
| Failure | 400 Bad Request            | Volume is not an integer or missing one of the required attributes. |
| Failure | 404 Not Found              | Load with this load_id does not exist.                              |
| Failure | 406 Not Acceptable         | Accept header does not include JSON                                 |
| Failure | 415 Unsupported Media Type | Content-Type header is not JSON.                                    |

### Response Examples
#### Success
```json
Status: 200 OK
{
    "carrier": null,
    "creation_date": "12/01/22",
    "id": 6206500422811648,
    "item": "paper",
    "self": "http://localhost:5000/loads/6206500422811648",
    "volume": 26
}
```
	
#### Failure
```json
Status: 400 Bad Request
{
    "Error": "The request object is missing at least one of the required attributes"
}
{
    "error": "Volume must be an integer."
}

Status: 404 Not Found
{
    "Error": "No load with this load_id exists"
}
        
Status: 406 Not Acceptable
No response body
        
Status: 415 Unsupported Media Type
No response body
```

# Delete a Load
Allows you to delete a load. Note that if the boat is currently carrying a load, the boat is not deleted.

```DELETE /loads/:load_id```

## Request 
### Request Headers
| Name         | Value            | Required? |
|--------------|------------------|-----------|
| Accept       | application/json | no        |
| Content-type | application/json | no        |

### Path Parameters
| Name    | Description    |
|---------|----------------|
| load_id | ID of the load |
	
### Query Parameters
None

### Authorization
None

### Request Body 
None

## Response 
### Response Body Format 
JSON, None 

### Response Statuses
| Outcome | Status Code    | Notes                             |
|---------|----------------|-----------------------------------|
| Success | 204 No Content |                                   |
| Failure | 404 Not Found  | No load with this load_id exists. |

### Response Examples 
#### Success 
```json
Status: 204 No Content
No response body
```

#### Failure
```json
Status: 404 Not Found 
{
    "Error": "No load with this load_id exists"
}
```

# Assign a Load to a Boat
A load is now assigned to a boat. The boat now includes the load in its list of loads and the load lists the boat as its carrier

```PUT /boats/:boat_id/loads/:load_id```

## Request
### Request Headers
| Name         | Value            | Required? |
|--------------|------------------|-----------|
| Accept       | application/json | yes       |
| Content-type | application/json | yes       |

### Path Parameters
| Name    | Description    |
|---------|----------------|
| boat_id | ID of the boat |
| load_id | ID of the load |

### Query Parameters
None

### Request Body
None

## Response
No body 

### Response Body Format 
JSON, None 

### Response Statuses 

| Outcome | Status Code      | Notes                                                                                                                                                                                                                                               |
|---------|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Success | 204 No Content   | Succeeds only if a boat exists with this boat_id, a load exists with this load_id and this load is not already on a boat.                                                                                                                           |
| Failure | 401 Unauthorized | JWT is missing, invalid, or expired.                                                                                                                                                                                                                |
| Failure | 403 Forbidden    | The load with this load_id is already being carried by a boat with some boat_id. Can fail if the load is being carried by a boat with the given boat_id. Can also fail if the boat with the given boat_id is being loaded is owned by another user. |
| Failure | 404 Not Found    | No boat with this boat_id is carrying a load with this load_id.  This could be because no boat with this boat_id exists, or  because no load with load_id exists.                                                                                   |

### Response Examples 
#### Success 
```json
Status: 204 No Content
No response body
````

#### Failure
```json
Status: 401 Unauthorized
{
    "error": "JWT missing, expired, or invalid"
}

Status: 403 Forbidden 
{  
    "Error": "The load is already loaded on another boat" 
}
{
    ???Error???: "The boat with this boat id is owned by another captain."
}

Status: 404 Not Found 
{  
    "Error": "The specified boat and/or load does not exist"
}
```

# Remove a Load from a Boat
A load is removed from a boat. The boat no longer lists the load in its list of loads and the load has a null carrier. The load is not deleted.

```DELETE /boats/:boat_id/loads/:load_id```
	
## Request
### Request Headers
| Name         | Value            | Required? |
|--------------|------------------|-----------|
| Accept       | application/json | no        |
| Content-type | application/json | no        |

### Path Parameters
| Name    | Description    |
|---------|----------------|
| boat_id | ID of the boat |
| load_id | ID of the load |

### Query Parameters
None

### Request Body
None

## Response

### Response Body Format 
JSON, None 

### Response Statuses
| Outcome | Status Code      | Notes                                                                                                                                                                                                                                                                             |
|---------|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Success | 204 No Content   | Succeeds only if a boat exists with this boat_id, a load exists with this load_id and this load is on this boat.                                                                                                                                                                  |
| Failure | 401 Unauthorized | JWT is invalid, missing, or expired.                                                                                                                                                                                                                                              |
| Failure | 403 Forbidden    | The boat with the given boat_id is owned by another user.                                                                                                                                                                                                                         |
| Failure | 404 Not Found    | No boat with this boat_id has a load with this load_id.  This could be because no boat with this boat_id exists, or because no load with this load_id exists, or even if both boat_id and load_id are valid, the boat with this boat_id is not carrying a load with this load_id. |

### Response Examples
#### Success 
```json
Status: 204 No Content
No response body
```
	

#### Failure
```json
Status: 401 Unauthorized
{
    "error": "JWT missing, expired, or invalid"
}

Status: 403 Forbidden
{
    ???Error???: "The boat with this boat id is owned by another captain."
}

Status: 404 Not Found 
{  
    "Error": "No boat with this boat_id is loaded with the load with this load_id"
}
```