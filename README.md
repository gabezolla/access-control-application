# Access Control Application
Access control and microexpression evaluator application for UFABC Graduation Project

# Photo Register
The proccess of registering photos in the access control application database will be done by requests on an simple API. One side of the system will be responsible for doing the face recognition, whilst the other will be in charge of registering new allowed people.

## Create
```http
POST api/photos
```

### Request
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `api_key` | `string` | **Required**. API key |
| `name` | `string` | **Required**. Person's name |
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

## Delete
```http
DELETE api/photos/{{id}}
```

### Request
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `api_key` | `string` | **Required**. API key |
| `name` | `string` | **Required**. Person's name |

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

# Notification Register
The application might send notifications for the user depending on which configurations he has setted up. For example, an emergency alert may be configured when fear microexpression has been detected for a period of time. In this case, a Telegram message could be sent for the user.

```http
POST api/notifications
```

### Request
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







