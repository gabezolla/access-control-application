# Photo Register :camera_flash:
The proccess of registering photos in the access control application database will be done by requests on an simple API. One side of the system will be responsible for doing the face recognition, whilst the other will be in charge of registering new allowed people.

<details>
<summary><b>Create</b> an entry on control access database by sending person's name and photo.</summary>

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

</details>

<details>
<summary><b>Consult</b> someone's photo searching by its id</summary>

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

</details>

<details>
<summary> <b>Delete</b> photo </summary>

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
</details>

<hr style="border:1px solid gray; border-style: dashed;"> </hr>

# Notification Register :vibration_mode::warning:
The application might send notifications for the user depending on which configurations he has setted up. For example, an emergency alert may be configured when fear microexpression has been detected for a period of time. In this case, a Telegram message could be sent for the user.

<details>
<summary><b>Create</b> a notification based on its type</summary>

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

</details>

<details>
<summary><b>Delete</b> notification</summary>

### Request
```http
DELETE api/notifications/{{id}}
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

</details>







