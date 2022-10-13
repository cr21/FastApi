import imp
from fastapi import APIRouter, status, HTTPException, Depends, Response
from .. import database, schemas, models
from sqlalchemy.orm import Session

from .. import utils

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(user_credentials:schemas.UserLogin, db:Session=Depends(database.get_db)):
    print("login called",user_credentials )
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"{user_credentials.email} not found in database")

    # if user found verify

    verified= utils.verify_pwd(user_credentials.password, user.password)

    if not verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="credentials not verified")

    else:

        return {
                "message":"Welcome to Goa !!!"
        }

    