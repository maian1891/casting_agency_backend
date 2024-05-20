# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.9

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/models/models.py`.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:
To run the server, execute:

```bash
gunicorn run:app
```

## Tasks

### Create a postgresql database connection

[Connect to a PostgreSQL database server](https://www.javatpoint.com/connect-to-a-postgresql-database-server)

### Create .env file

#### Create Environment Variables in Windows

```bash
export AUTH0_DOMAIN=
export ALGORITHMS=
export API_AUDIENCE=
export DATABASE_PATH=
export ASSISTANT_TOKEN=
export DIRECTOR_TOKEN=
export PRODUCER_TOKEN=
```

#### Create Environment Variables in MacOS

```bash
export AUTH0_DOMAIN=
export ALGORITHMS=
export API_AUDIENCE=
export DATABASE_PATH=
export ASSISTANT_TOKEN=
export DIRECTOR_TOKEN=
export PRODUCER_TOKEN=
```

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:actor-detail/:id`
   - `get:actors`
   - `post:actor`
   - `patch:actor`
   - `delete:actor`
   - `get:movie-detail/:id`
   - `get:movies`
   - `post:movie`
   - `patch:movie`
   - `delete:movie`
6. Create new roles for:
   - Casting Assistant: Can view actors and movies
     - can `get:actor-detail/:id`
     - can `get:actors`
     - can `get:movie-detail/:id`
     - can `get:movies`
   - Casting Director: Can view actors and movies. Can Add, Edit, Delete Actor
     - can `get:actor-detail/:id`
     - can `get:actors`
     - can `get:movie-detail/:id`
     - can `get:movies`
     - can `post:actor`
     - can `patch:actor`
     - can `delete:actor`
   - Executive Producer: Can do anything
     - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 3 users - assign the Casting Assistant role to one, Casting Director role to the other and Executive Producer role to the other.
   - Sign into each account and make note of the JWT.
   - Import the postman collection `./postman/udacity.postman_collection.json`
   - Edit variables in the postman collection:
     - value of url and token ./postman/variable.png

### Implement The Server

### Test notes

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

#### Migration and Insert dummy data into databases

```bash
dropdb casting_agency_test
createdb casting_agency_test
export FLASK_APP=api.py
flask db init
flask db migrate
flask db upgrade
flask shell
from databases.helper import UserHelper
UserHelper.add_dummy_actor_data()
UserHelper.add_dummy_movie_data()
exit()
```

```bash
python test_api.py
```

1. Migration and Insert dummy data into databases
2. frontend url: [https://casting-agency-frontend-4j8j.onrender.com](https://casting-agency-frontend-4j8j.onrender.com)
3. backend url: [https://coffee-shop-backend-5ei5.onrender.com](https://coffee-shop-backend-5ei5.onrender.com)
