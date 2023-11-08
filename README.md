# FastAPI Firebase Authentication with FireStore
  You Can find and test APIs on [Hosted FASTAPI Server Backend](http://ec2-54-144-109-217.compute-1.amazonaws.com:8010/docs)

### Installation

- Clone the Repo.
- Open terminal from repo folder
- Create a virtual environment.

  ```bash
  python -m venv .venv
  ```

- Activate Environment

  ```powershell
  # For Windows User
  .venv/Scripts/activate
  ```

  ```bash
  # For Linux User
  source .venv/bin/activate
  ```

- Install Dependencies

  ```bash
  pip install -r requirements.txt
  ```

### Starting the Server

- Start uvicorn Server

  ```bash
  python main.py
  ```

### APIs Docs

If you're running it on localhost.

HOST URL : http://localhost:8000

##### Authentication

- Signup : `/auth/signin`
  Request:

  Method: POST
  Body: Mode(Raw)
  Header: Content-Type :application/json
  Body Content:

  ```json
  {
    "username": "uername",
    "email": "email",
    "password": "valid passsword",
    "Full Name": "Full Name"
  }
  ```

  Response:

  - 201 : User Created
    e.g.:

    ```json
    {
      "created_at": 1699383886038,
      "full_name": "ABC 123 XYZ",
      "email": "abc123@xyz.com",
      "username": "abc123xyz"
    }
    ```

  - 400 :

    - UserNameExists

      ```json
      {
        "detail": {
          "error": {
            "exception": "UserNameExists",
            "message": "User with abc123xyz already exists"
          }
        }
      }
      ```

    - EmailAlreadyExistsError

      ```json
      {
        "detail": {
          "error": {
            "exception": "EmailAlreadyExistsError",
            "message": "The user with the provided email already exists (EMAIL_EXISTS)."
          }
        }
      }
      ```

    - Assetion Errors (422):

      - ## Password Validations

        - Must have 8 Chars or More
        - Must have 20 chars or less
        - Must have at least one uppercase, lowercase, digit, special character each.

      - Username Validations

        - Must be AlphaNumeric
        - Must have >3 and <20 character length

      - Valid Email

- SignIn : `/auth/signin`

  Request:

  Method: POST
  Body: Mode(Raw)
  Header: Content-Type :application/json
  Body Content:

  ```json
  {
    "email": "email",
    "password": "valid password"
  }
  ```

  Response:

  - 200: User Found, Return Access Tokens. e.g. :

    ```json
    {
      "user_id": "rphoTumr1pg7FCOwGg1iziaRWKD3",
      "email": "abc123@xyz.com",
      "full_name": "ABC 123 XYZ",
      "access_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ0OWU0N2ZiZGQ0ZWUyNDE0Nzk2ZDhlMDhjZWY2YjU1ZDA3MDRlNGQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiQUJDIDEyMyBYWVoiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vaGVsbG9maXJlYmFzZS03MTA3YSIsImF1ZCI6ImhlbGxvZmlyZWJhc2UtNzEwN2EiLCJhdXRoX3RpbWUiOjE2OTkzODQ3NDMsInVzZXJfaWQiOiJycGhvVHVtcjFwZzdGQ093R2cxaXppYVJXS0QzIiwic3ViIjoicnBob1R1bXIxcGc3RkNPd0dnMWl6aWFSV0tEMyIsImlhdCI6MTY5OTM4NDc0MywiZXhwIjoxNjk5Mzg4MzQzLCJlbWFpbCI6ImFiYzEyM0B4eXouY29tIiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7ImVtYWlsIjpbImFiYzEyM0B4eXouY29tIl19LCJzaWduX2luX3Byb3ZpZGVyIjoicGFzc3dvcmQifX0.G-xAjrCO2upzF6cC99g2lebUgRlj4utEnMAtdC0KgOYGZWGLqMWlPomTh3hwO4XHSFXHP3WUd7okQr0cJrpcXKefT-8UlWqgTnjiiDvui8Hpwao6u0XDlWTh8j7S5mcQ4K1Jc-TkSslcxAPAD5hpSlpcY2aFQcTmgFjB9f3Kqdik0KHA2VzOS3S_iQIAfBpytGayFZm6l27aYXQnGohW2DhEgbmfMq4yJGXXSywntxFTMzqv_ES7w-G8f0-l1wGuTyDx9xElFu3dCmIFddkdWt8pNHjLz5ZXNsUsvHxh0PdvVZJSZtgmwUYG7uJeiZJJvCVEzcDbFQqpYAcu7PXUww",
      "token_type": "bearer",
      "expires_in": 3600,
      "refresh_token": "AMf-vBxUuQAIOfNKwd6kQYrOgPPPCl4Mc80EW4aI-Pg5KTikyaJjBg1BLTPkmHYqG7aSSGCgbj3395Ig8wpU1Mm6zAZ2wZU4rTFIjhGgNmy9AmGdVNPKFJHylbAg9fs6BySHa5Xv2Tt7Q2BhZr0kP0_HnzD222mKjEt9u-uuBLSKkOqfQvLULW6gh_BrUDOU_4jz33hH1KmZkqh8QoPrWZUzq-9b4oUA6fhN5sveilgC2Y62NmQyLN8"
    }
    ```

  - 400:

    - Invalid Password

      ```json
      {
        "detail": {
          "error": {
            "exception": "INVALID_PASSWORD",
            "message": "Password Entered is InValid"
          }
        }
      }
      ```

    - Email Not Found

      ```json
      {
        "detail": {
          "error": {
            "exception": "EMAIL_NOT_FOUND",
            "message": "Password Entered is InValid"
          }
        }
      }
      ```

    - 422 : Improper Json Body Passed

      ```json
      {
        "detail": [
          {
            "type": "json_invalid",
            "loc": ["body", 71],
            "msg": "JSON decode error",
            "input": {},
            "ctx": {
              "error": "Expecting property name enclosed in double quotes"
            }
          }
        ]
      }
      ```

##### Users

- Get User Details : `/users/me/`
  Request:
  Method : Get
  Header: Authorization : Bearer {access_token}

  Response:

  - 200 : User Details e.g.:

    ```json
    {
      "created_at": 1699383886038,
      "full_name": "ABC 123 XYZ",
      "email": "abc123@xyz.com",
      "username": "abc123xyz"
    }
    ```

  - 401 : Unauthorised

    ```json
    {
      "detail": {
          "error": {
              "exception": "InvalidIdTokenError",
              "message": "Wrong number of segments in token: b'undefined'"
          }
      }
    }
    ```

- Update User Details : `/users/me/`
  Request:
  Method : Put
  Header: Authorization : Bearer {access_token}
  Body: Mode(Raw)
  Header: Content-Type :application/json
  Body Content:

  ```json
  {
    "full_name": "New Name",
    "username": "newusername",
    "email": "new email"
  }
  ```

  Response:

  - 200 : User Details e.g.:

    ```json
    {
      "created_at": 1699383886038,
      "full_name": "New Name",
      "email": "new email",
      "username": "newusername"
    }
    ```
  - 401 : Unauthorised

    ```json
    {
      "detail": {
          "error": {
              "exception": "InvalidIdTokenError",
              "message": "Wrong number of segments in token: b'undefined'"
          }
      }
    }
    ```
  - 400 : Bad Request

    ```json
    {
      "detail": {
          "error": {
              "exception": "UserNameExists",
              "message": "User with newusername already exists"
          }
      }
    }
    ```
  - 422 : Improper Json Body Passed

    ```json
    {
      "detail": [
        {
          "type": "json_invalid",
          "loc": ["body", 71],
          "msg": "JSON decode error",
          "input": {},
          "ctx": {
            "error": "Expecting property name enclosed in double quotes"
          }
        }
      ]
    }
    ```
  - Delete User : `/users/me/`
    Request:
    Method : Delete
    Header: Authorization : Bearer {access_token}

    Response:

    - 200 : User Details e.g.:

      ```json
      {
        "created_at": 1699383886038,
        "full_name": "New Name",
        "email": "new email",
        "username": "newusername"
      }
      ```
    - 401 : Unauthorised

      ```json
      {
        "detail": {
            "error": {
                "exception": "InvalidIdTokenError",
                "message": "Wrong number of segments in token: b'undefined'"
            }
        }
      }
      ```
  - Reset Password : `/users/reset-password/`
    Request:
    Method : Post
    Body: Mode(Raw)
    Header: 
    - Content-Type :application/json
    - Authorization : Bearer {access_token}

    Body Content:

    ```json
    {
      "new_password": "new_password"
    }
    ```

    Response:

    - 200 : Password Reset

      ```json
      {
          "created_at": 1699383886038,
          "full_name": "ABC 123 XYZ",
          "email": "abc123@xyz.com",
          "username": "abc123xyz"
      }
      ```

    - 401 :  Unauthorised

      ```json
      {
        "detail": {
            "error": {
                "exception": "InvalidIdTokenError",
                "message": "Wrong number of segments in token: b'undefined'"
            }
        }
      }
      ```
    - 422 : Improper Json Body Passed
      
        ```json
        {
          "detail": [
            {
              "type": "json_invalid",
              "loc": ["body", 71],
              "msg": "JSON decode error",
              "input": {},
              "ctx": {
                "error": "Expecting property name enclosed in double quotes"
              }
            }
          ]
        }
        ```

### POSTMAN Collection

- Postman APIs with Pre-Configured Environments and Tests

 - Follow the link to join the team and get the collection
  [![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/join-team?invite_code=5f5099534d0417bfb1b2706c468b3f5b&target_code=8646f36f7c70aa8ada1ef3ab4b948708)
  

  Useful authorization Scripts in Users Collection

  ```javascript
  const email = pm.globals.get("email")
  const password = pm.globals.get("password")
  const access_token = pm.collectionVariables.get("access_token")
  const expires_at = pm.collectionVariables.get("expires_at")


  if (!access_token || !expires_at ||  expires_at < Math.floor(Date.now()/1000)){
    pm.sendRequest({
        url: 'http://localhost:8000/auth/signin',
        method: 'POST',
        header: {
            'Content-Type': 'application/json'
        },
        body: {
            mode: 'raw',
            raw: JSON.stringify({
                email: email,
                password: password
            })
        }
    }, function (err, res) {
        if (err) {
            console.log(err);
        } else {
            let response = res.json()
            console.log(response)
            pm.collectionVariables.set('access_token', response.access_token);
            pm.collectionVariables.set('expires_at', Math.floor(Date.now()/1000)+response.expires_in-600)
            
        }
    })
  }
  pm.request.headers.add({
    key: 'Authorization',
    value: `Bearer ${pm.collectionVariables.get('access_token')}`
  });
  ```

    

# TODOs

- [x] User APIs : Get, Update, Delete
- [ ] Rate Limiting
- [ ] Unit Test
- [x] Password Reset
