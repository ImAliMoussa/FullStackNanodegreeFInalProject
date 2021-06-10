# FullStackNanodegreeFInalProject

This is the Full Stack Nanodegree final project. The project combines alot of the things I learned from the project. 
It is a flask backend restful api, authentication using auth0 and you'll find some tests for the routes. The backend is deployed on heroku.


The project is implementing a Casting Agency and there are several roles in the agency.

1) Casting Assistant
2) Casting Director
3) Executive Producer

These roles are implemented using Auth0 roles. Each role gets a set of permissions.

- Casting Assistant
  - Can view actors and movies
- Casting Director
  - All permissions a Casting Assistant has and…
  - Add or delete an actor from the database
  - Modify actors or movies
- Executive Producer
  - All permissions a Casting Director has and…
  - Add or delete a movie from the database

---

# Running the Flask app

- Open a terminal and change directory to the project directory using ```cd```

- First, create a virtual environment called venv. I like using ```virtualenv```. You can install it globally like this:

```pip install virtualenv```

- Create the virtual environment for python packages

```
virtualenv venv
```

- Activate the virtualenv

```
source ./venv/bin/activate
```

- Install the project requirements

```
pip install -r requirements.txt
```
- Now to run the server use

```
flask run
```

- All the flask environment variables are kept in the ```.flaskenv``` file which flask looks for by default.

- Other environment variables should be kept in a ```.env``` file, or you could run the ```script.sh``` file like this

```
bash script.sh
```
---

# ```.env``` file

```
DATABASE_URL_TEST=postgresql://postgres:changeme@localhost:5432/capstonetest
DATABASE_URL=postgresql://postgres:changeme@localhost:5432/capstone
APP_SETTINGS=config.DevelopmentConfig
CAST_ASSIST_TOKEN=foo
CAST_DIR_TOKEN=foo
EXEC_PROD_TOKEN=foo
AUTH0_DOMAIN=alimoussa.eu.auth0.com
AUTH0_AUDIENCE=Capstone-Udacity
```

- Note I assume you have Postgres installed with 2 databases
1) capstone
2) capstonetest (test database)

You can create databases using ```psql``` using
```
create database capstone;
```

Or using pgadmin.

---

# Routes

---
```
GET /actors
  - Return a json array of objects, each object is an object of Actor model in the database
  - requires permission ```get:actors``` in RBAC Auth0
  - Example object
  {
    "name": "Ali",
    "age": 22,
    "gender": "male"
  }
```
---
```
POST /actors
  - posts an actor to database
  - json body should contain all the attributes
  - requires permission ```post:actors``` in RBAC Auth0
  {
    "name": "Ali",
    "age": 22,
    "gender": "male"
  }  
```
---
```
DELETE /actors/<int:key>
  - deletes the actor with primary key id of key
  - if not present returns a ```404``` response
  - return ```200``` OK if successful
  - requires permission ```delete:actors``` in RBAC Auth0

```
--- 
```
PATCH /actors/<int:key>
  - modifies the actor with primary key id of key
  - if not present returns a ```404``` response
  - return ```200``` OK if successful
  - requires a json body in the request of parameters to change
  - requires permission ```patch:actors``` in RBAC Auth0

  {
    "name": "Ali Moussa"
  }
```
---
```
GET /movies
  - Return a json array of objects, each object is an object of Movie model in the database
  - requires permission ```get:movies``` in RBAC Auth0
  - Example object
  {
    "id": 1
    "title": "Harry Potter and the Chamber of Secrets",
    "release_date": "...",
  }
```
---
```
POST /movies
  - posts a movie to database
  - json body should contain all the attributes
  - requires permission ```post:movies``` in RBAC Auth0
  - release_date is optional, defaults to whatever the day is
  {
    "title": "Harry Potter and the Chamber of Secrets",
  }  
```
---
```
DELETE /movies/<int:key>
  - deletes the movie with primary key id of key
  - if not present returns a ```404``` response
  - return ```200``` OK if successful
  - requires permission ```delete:movies``` in RBAC Auth0
```
--- 
```
PATCH /movies/<int:key>
  - modifies the movie with primary key id of key
  - if not present returns a ```404``` response
  - return ```200``` OK if successful
  - requires a json body in the request of parameters to change
  - requires permission ```patch:movies``` in RBAC Auth0

  {
    "name": "Ali Moussa"
  }
```
---
# Testing

- Tests are written in the ```test_app.py``` file.

Run them using

```
python test_app.py
```
---
# Database

initialize database

```
python manage.py db init
```

When changes are made to database models you must migrate

```
python manage.py db migrate
python manage.py db upgrade
```
---
# Creating tokens

Visit the link in an incognito tab in your browser
```
https://alimoussa.eu.auth0.com/authorize?audience=Capstone-Udacity&response_type=token&client_id=OFvbxKCedwCBGrWQAl5OUbQuRFVGmM17&redirect_uri=http://localhost:8080/login-results
```

- Casting Assistant token
  - email: castingassistant@gmail.com
  - password: MyPassword@2021
- Casting Director token
  - email: castingdirector@gmail.com
  - password: MyPassword@2021
- Executive Producer token
  - email: executiveproducer@gmail.com
  - password: MyPassword@2021

After signing in, you will be redirected to a link. Extract manually the token from the query parameters in the link.

- Example
```
http://localhost:8080/login-re`sults#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlE1TGhZdnV1QUhpeC1TR3d6Mjg4WiJ9.eyJpc3MiOiJodHRwczovL2FsaW1vdXNzYS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBjMGJlZmI4ODJmZjMwMDZmYzAzMzE1IiwiYXVkIjoiQ2Fwc3RvbmUtVWRhY2l0eSIsImlhdCI6MTYyMzI0OTE5NSwiZXhwIjoxNjIzMzM1NTk1LCJhenAiOiJPRnZieEtDZWR3Q0JHcldRQWw1T1ViUXVSRlZHbU0xNyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.krIiOdEg6Yh2PN6nSsJU0HwHoWSJqSfbE_T4rtSUcidPhUm__fK9qvnj9zjlbXFfCHus1_2-mbjTgYQC0jhazJNPqMtJrMEGnNWPEua432adv5xO8g487tQm61lw3OlWOkxDeaJ_k07DtE5iS3fLkc7YW_q4gAXK0cee5T3SfnG3gSVDDSpu22DcfnaWDd_XInelL_4fedD1LWAhWVHZjir5lxV74JWL6cN5yGnhuiKIgUXRSpPdenm1LId9ED3M9KgoALHYlUUxqmXS6vhhoXovdXGUAYS2d9sUGiH0HWL8kvNQaLtlKppEBHxCQJaTrwIF8u62dBR-fdIkb3Vc4g&expires_in=86400&token_type=Bearer
```

- acesss_token:
```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlE1TGhZdnV1QUhpeC1TR3d6Mjg4WiJ9.eyJpc3MiOiJodHRwczovL2FsaW1vdXNzYS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBjMGJlZmI4ODJmZjMwMDZmYzAzMzE1IiwiYXVkIjoiQ2Fwc3RvbmUtVWRhY2l0eSIsImlhdCI6MTYyMzI0OTE5NSwiZXhwIjoxNjIzMzM1NTk1LCJhenAiOiJPRnZieEtDZWR3Q0JHcldRQWw1T1ViUXVSRlZHbU0xNyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.krIiOdEg6Yh2PN6nSsJU0HwHoWSJqSfbE_T4rtSUcidPhUm__fK9qvnj9zjlbXFfCHus1_2-mbjTgYQC0jhazJNPqMtJrMEGnNWPEua432adv5xO8g487tQm61lw3OlWOkxDeaJ_k07DtE5iS3fLkc7YW_q4gAXK0cee5T3SfnG3gSVDDSpu22DcfnaWDd_XInelL_4fedD1LWAhWVHZjir5lxV74JWL6cN5yGnhuiKIgUXRSpPdenm1LId9ED3M9KgoALHYlUUxqmXS6vhhoXovdXGUAYS2d9sUGiH0HWL8kvNQaLtlKppEBHxCQJaTrwIF8u62dBR-fdIkb3Vc4g
```

Verify token in https://jwt.io
