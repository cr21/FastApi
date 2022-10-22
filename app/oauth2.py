from datetime import datetime, timedelta
from jose import jwt, JWTError

SECRET_KEY='8390440305188503943062962101038105244839'
ALGORITHM='HS256'
ACCESS_TOKEN_EXPIRATION_TIME=30

def get_jwt_token(data:dict):
    encoded_data = data.copy()
    encoded_data.update({"exp":datetime.now()  + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_TIME) })
    
    encoded_jwt_token = jwt.encode(encoded_data,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt_token

