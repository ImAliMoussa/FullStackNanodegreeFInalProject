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


