# FastApi
Exploring FastAPI

# Minimal Social Media Specifications
     - Users can write Posts
     - Users can like/dislike posts
     - Basic Password Oauth2 Login authentication using JWT

## Models:
     1. Users with attributes email, password, phone_number
     2. Posts with attributes title and content, published, owner_id (who created this post)
     3. Votes with attribute post_id, user_id 
     
## Endpoints:
     GET /posts /posts/id  /users/id
     DELETE /posts/id
     POST /posts  /users /login /vote 
     PUT /posts/id
     

## Tests:
     Added tests for users, votes and posts




## Motivation
 It covers following technical topics in a single app:

1. **Database modeling** with **postgres & sqlalchemy** check -> database.py models.py schema.py

2. **REST API**  for CRUD Operations on database with **FastAPI**. check -> app.py and routers/post.py, routers/user.py,  routers/vote.py

3. **Automated unit testing** for test driven development **(TTD)** with **pytest** (check-> test/ directory)

4. **DataBase Migration Experience with alembic**

5. Authorization  with Auth0 (check routers/auth.py)

6. **Deployment on Heroku / ubuntu with github actions with CI/CD**


## Getting Started

### Installing Dependencies

#### Python 3 

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Example in my code :

python3 -m venv env
source env/bin/activate

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies 

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [FastAPI](https://fastapi.tiangolo.com/)  is backend microservices framework. FastAPI is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 


## Database Setup

Also set the following environmental variable for Auth0

```bash
# You can replace following with your details  This is my details and this token can be useful for running and testing my app, but this token might expired
export PG_DATABASE_HOST=<YOUR INPUT>
export PG_DATABASE_PORT=5432
export PG_DATABASE_PASSWORD=<YOUR INPUT>
export PG_DATABASE_USERNAME=<YOUR INPUT>
export PG_DATABASE_NAME=<YOUR INPUT>
export JWT_SECRET_KEY=<YOUR INPUT>
export JWT_ALGORITHM=HS256
export JWT_TOKEN_EXPIRED_MINUTES=60
```

please create database according to setting given or you can change accordingly 

- Other Deployment instructions are added in workflows, Procfile, gunicorn.service, nginx files, please see in repository

![FastAPI](https://i.imgur.com/mRJNMnW.png)
  
