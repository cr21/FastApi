
from ..utils import hash
from fastapi import  status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import  models
from .. import schemas
from ..database import get_db

router = APIRouter(
                prefix='/users',
                tags=["Users"]
                )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
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


@router.get("/{id}/", response_model=schemas.UserOut)
def get_user(id:int, db:Session=Depends(get_db)):
    
    fetched_user = db.query(models.User).filter(models.User.id == int(id)).first()
    
    if not fetched_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} not found")
    return fetched_user