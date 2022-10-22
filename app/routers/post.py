

from typing import  List
from fastapi import  status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import  models, schemas, oauth2
from ..database import get_db


router = APIRouter(
        prefix="/posts",
        tags=["Posts"]
        
        )

@router.get("/", response_model=List[schemas.Post])
async def get_posts(db:Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    all_posts=db.query(models.Post).all()
    return all_posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post : schemas.PostCreate, db:Session=Depends(get_db),user_token_info:schemas.TokenData=Depends(oauth2.get_current_user) ):
    
    created_post = models.Post(**post.dict())

    db.add(created_post)
    db.commit()
    db.refresh(created_post)

    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES(%s,%s,%s) RETURNING *""",
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    return created_post


@router.get("/{id}", status_code=status.HTTP_404_NOT_FOUND)
def get_post(id:int, db:Session=Depends(get_db),user_token_info:schemas.TokenData=Depends(oauth2.get_current_user) ):
    fetched_post = db.query(models.Post).filter(models.Post.id==id)
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))

    # post=cursor.fetchone()
    # print("post", post)
    print(fetched_post.first() == None)
    if fetched_post.first() == None:
        
        return HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    else:
        
        return fetched_post




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),user_token_info:schemas.TokenData=Depends(oauth2.get_current_user) ):
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

        

@router.put("/{id}",status_code=status.HTTP_404_NOT_FOUND, response_model=schemas.Post)
def update_post(id:int, post:schemas.PostCreate, db:Session=Depends(get_db), user_token_info:schemas.TokenData=Depends(oauth2.get_current_user) ):
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
