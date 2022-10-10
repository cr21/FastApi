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


models.Base.metadata.create_all(bind=engine)




app = FastAPI()


    





@app.get("/posts", response_model=List[schemas.Post])
async def get_posts(db:Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    all_posts=db.query(models.Post).all()
    return all_posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post : schemas.PostCreate, db:Session=Depends(get_db)):
    
    created_post = models.Post(**post.dict())

    db.add(created_post)
    db.commit()
    db.refresh(created_post)

    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES(%s,%s,%s) RETURNING *""",
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    return created_post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id:int, db:Session=Depends(get_db)):

    fetched_post = db.query(models.Post).filter(models.Post.id==id).first()
    

    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))

    # post=cursor.fetchone()
    # print("post", post)
    
    if not fetched_post:
        
        return HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    else:
        
        return fetched_post




@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute("""DELETE FROM posts  WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    
    # conn.commit()

    deleted_post_query = db.query(models.Post).filter(models.Post.id==id)
    if  deleted_post_query.first() == None :
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    
    status_code=status.HTTP_204_NO_CONTENT
    return {
        "message":"post deleted",
        "status_code":status_code   
    }

        

@app.put("/posts/{id}",status_code=status.HTTP_404_NOT_FOUND, response_model=schemas.Post)
def update_post(id:int, post:schemas.PostCreate, db:Session=Depends(get_db)) :
    # cursor.execute("""Update posts SET title = %s, content = %s, published = %s WHERE id = %sRETURNING *""",(post.title, post.content, post.published, id))
    # conn.commit()
    # updated_post = cursor.fetchone()
    updated_post_query= db.query(models.Post).filter(models.Post.id==id)
    
    updated_post = updated_post_query.first()
    
    if updated_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return updated_post_query.first()



@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user:schemas.UserCreate, db:Session=Depends(get_db)):

    # hash password
    
    hashed_pwd = hash(user.password)
    user.password =  hashed_pwd 

    created_users = models.User(**user.dict())
    
    
    db.add(created_users)
    db.commit()
    db.refresh(created_users)

    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES(%s,%s,%s) RETURNING *""",
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    return created_users



@app.get("/users/{id}/", response_model=schemas.UserOut)
def get_user(id:int, db:Session=Depends(get_db)):
    
    fetched_user = db.query(models.User).filter(models.User.id == int(id)).first()
    
    if not fetched_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} not found")
    return fetched_user



# title: str, content : str
# uvicorn main:app --reload