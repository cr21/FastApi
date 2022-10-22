from calendar import c
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from jose import jwt, JWTError

from app.schemas import TokenData
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY='8390440305188503943062962101038105244839'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRATION_TIME=30

def get_jwt_token(data:dict):
    encoded_data = data.copy()
    encoded_data.update({"exp":datetime.utcnow()  + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_TIME) })
    
    encoded_jwt_token = jwt.encode(encoded_data,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt_token


def verify_token(token:str, credential_exception):
    try:
        payload=jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        print("token")
        # get whatever key you passed when you generated token initially
        user_id:str = payload.get("user_id")
        user_email:str = payload.get("user_email")

        if user_id is None:
            raise credential_exception
        
        token_data =  TokenData(id=user_id, email=user_email)

        return token_data
    except JWTError:
        raise credential_exception


def get_current_user(token:str=Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                            detail="Could not validate Credentials",
                                            headers={"WWW-Authenticate":"Bearer"}
                                        )

    return verify_token(token=token, credential_exception=credential_exception)