# Access Control Application
Access control and microexpression evaluator application for UFABC Graduation Project

# Photo Register :camera_flash:
The proccess of registering photos in the access control application database will be done by requests on an simple API. One side of the system will be responsible for doing the face recognition, whilst the other will be in charge of registering new allowed people.

## Create
Create an entry on control access database by sending person's name and photo.

### Request
```http
POST api/users/{{name}}/photos
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `api_key` | `string` | **Required**. API key |
| `image` | `.jpg, .png` | **Required**. Face image |

### Response
```javascript
{
  "message" : string,
}
```

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 400 | `Bad Request` |
| 404 | `Not Found` |
| 500 | `Internal Server Error` |

<hr style="border:0.2px solid gray"> </hr>

## Read
Consult someone's photo searching by its id

### Request
```http
GET api/users/{{name}}/photos/{{id}}
```

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 400 | `Bad Request` |
| 404 | `Not Found` |
| 500 | `Internal Server Error` |

<hr style="border:0.2px solid gray"> </hr>

## Delete
Delete photo

### Request
```http
DELETE api/users/{{name}}/photos/{{id}}
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `api_key` | `string` | **Required**. API key |

### Response
```javascript
{
  "message" : string,
}
```

| Status Code | Description |
| :--- | :--- |
| 200 | `OK` |
| 400 | `Bad Request` |
| 404 | `Not Found` |
| 500 | `Internal Server Error` |

<hr style="border:1px solid gray"> </hr>

# Notification Register :vibration_mode::warning:
The application might send notifications for the user depending on which configurations he has setted up. For example, an emergency alert may be configured when fear microexpression has been detected for a period of time. In this case, a Telegram message could be sent for the user.

## Create
Create a notification based on its type

### Request
```http
POST api/notifications
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `api_key` | `string` | **Required**. API key |
| `type` | `string` | **Required**. Notification type (e.g. "telegram", "email", etc.) |

### Response
```javascript
{
  "message" : string,
}
```

| Status Code | Description |
| :--- | :--- |
| 201 | `Created` |
| 400 | `Bad Request` |
| 404 | `Not Found` |
| 500 | `Internal Server Error` |

## Delete
Delete notification

### Request
```http
DELETE api/notifications/{{id}}
```
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `api_key` | `string` | **Required**. API key |
| `type` | `string` | **Required**. Notification type (e.g. "telegram", "email", etc.) |

### Response
```javascript
{
  "message" : string,
}
```

| Status Code | Description |
| :--- | :--- |
| 201 | `Created` |
| 400 | `Bad Request` |
| 404 | `Not Found` |
| 500 | `Internal Server Error` |







