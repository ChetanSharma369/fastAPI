from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, databases, models, config
from fastapi import Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme =OAuth2PasswordBearer(tokenUrl='userss/login')
#SECRET KEY
#ALGORITHM 
#EXPIRATION TIME

SECRET_KEY=config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes

def create_acess_token(data:dict):
    to_encode = data.copy()
    expires= datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expires})

    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt

def verify_acsess_token(token:str,credential_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id: str=payload.get("user_email")
    
        if id is None:
            raise credential_exception
        token_data=schemas.TokenData(email=id)
    except JWTError:
        raise credential_exception
    return token_data
    

def get_current_user(token: str=Depends(oauth2_scheme),db:Session=Depends(databases.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="could not validate credentials",headers={"WWW.Authenticate":"Bearer"})
    token=verify_acsess_token(token,credentials_exception)
    user= db.query(models.Users).filter(models.Users.email == token.email).first()
    return user


    