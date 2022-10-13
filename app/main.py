from curses.ascii import HT
from email.quoprimime import body_check
from statistics import mode
from . import models
from .utils import hash
from .database import engine, get_db
from random import randrange
from re import I
from typing import Optional, List
from fastapi import FastAPI, Response, status,HTTPException, Depends
from fastapi.params import Body
import psycopg2
import time
from sqlalchemy.orm import Session
from psycopg2.extras import RealDictCursor
# for Validation of Requests
from pydantic import BaseModel
from . import schemas
# Database connection
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)



app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)



# title: str, content : str
# uvicorn app.main:app --reload