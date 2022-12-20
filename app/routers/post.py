

from typing import  List
from fastapi import  status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Optional
from .. import  models, schemas, oauth2
from ..database import get_db


router = APIRouter(
        prefix="/posts",
        tags=["Posts"]
        
        )

@router.get("/", response_model=List[schemas.Post])
async def get_posts(db:Session=Depends(get_db),
                        limit:int=10, skip:int=0, search:Optional[str]= ""):
    
    all_posts=db.query(models.Post).\
                            filter(models.Post.title.contains(search)).\
                            limit(limit).\
                            offset(skip).\
                            all()
    return all_posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post : schemas.PostCreate, db:Session=Depends(get_db),current_user:schemas.UserOut=Depends(oauth2.get_current_user) ):
    # add owner_id field in payload
    
    created_post = models.Post(owner_id = current_user.id,**post.dict())
    
    
    print("created_post", create_post)
    db.add(created_post)
    db.commit()
    db.refresh(created_post)

    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES(%s,%s,%s) RETURNING *""",
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    return created_post


@router.get("/{id}", status_code=status.HTTP_404_NOT_FOUND,response_model=schemas.Post)
def get_post(id:int, db:Session=Depends(get_db),current_user:schemas.UserOut=Depends(oauth2.get_current_user) ):
    fetched_post = db.query(models.Post).filter(models.Post.id==id)
    if fetched_post.first() == None:
        
        return HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    else: 
        return fetched_post.first()




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:schemas.UserOut=Depends(oauth2.get_current_user) ):
    # cursor.execute("""DELETE FROM posts  WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if  post == None :
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to perform this action")

    post_query.delete(synchronize_session=False)
    db.commit()
    
    status_code=status.HTTP_204_NO_CONTENT
    return {
        "message":"post deleted",
        "status_code":status_code   
    }

        

@router.put("/{id}",status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id:int, post:schemas.PostCreate, db:Session=Depends(get_db), current_user:schemas.UserOut=Depends(oauth2.get_current_user) ):
    # cursor.execute("""Update posts SET title = %s, content = %s, published = %s WHERE id = %sRETURNING *""",(post.title, post.content, post.published, id))
    # conn.commit()
    # updated_post = cursor.fetchone()
    updated_post_query= db.query(models.Post).filter(models.Post.id==id)
    
    updated_post = updated_post_query.first()
    
    if updated_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorised to perform this action")

    updated_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return updated_post_query.first()
