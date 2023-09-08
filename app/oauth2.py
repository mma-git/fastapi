from jose import JWTError, jwt
from datetime import datetime,timedelta
from . import schemas,database,models
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
#neeed
#secretkey, openssl rand -hex 32
#algo
#and expiration of token
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_mins
#JWT
def create_access_token(data:dict):
    to_encode=data.copy()
    expires=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expires}) 
    #making the token    
    encoded_jwt=jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #consists of payload secret key and algo
    return encoded_jwt
'''
verify token ensures the payload can be decoded correctly
returns the JWT, extracts the id, and validates against tokendata to ensure correct value

'''
# def verify_access_token(token: str, credentials_exception):

#     try:

#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         id: str = payload.get("user_id")
#         if id is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(id=id)
#     except JWTError:
#         raise credentials_exception

#     return token_data
def verify_access_token(token: str, credentials_exception):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    
        id:str = payload.get("user_id")
    
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
'''
calls the verify token command

'''
def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credentials_exception= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail=f"could not validate credentials",
                                         headers={"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    
    user = db. query(models.User).filter(models.User.id == token.id).first()
    
    return user