import imp
from os import access
from fastapi import APIRouter, status, HTTPException, Depends, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, oauth2
from sqlalchemy.orm import Session

from .. import utils

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(database.get_db)):
    print("login called",user_credentials )

    # user_credentials
    # {
    #     "username":"asdg",
    #     "password":"asdsf"
    # }
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
        detail=f"{user_credentials.email} not found in database")

    # if user found verify

    verified= utils.verify_pwd(user_credentials.password, user.password)

    if not verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="credentials not verified")

    # create token
    access_token = oauth2.get_jwt_token({"user_id":user.id,"user_email":user.email})

    return {
            "access_token":access_token,
            "token_type":"bearer"
    }
    

    