# Access Control Application
Access control and microexpression evaluator application for UFABC Graduation Project

# Photo Register
The proccess of registering photos in the access control application database will be done by requests on an simple API. One side of the system will be responsible for doing the face recognition, whilst the other will be in charge of registering new allowed people.

```http
POST api/photos
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `api_key` | `string` | **Required**. API key |
| `api_key` | `string` | **Required**. Person's name |
| `api_key` | `.jpg, .png` | **Required**. Face image |










