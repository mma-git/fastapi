from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .. import schemas,models,utils,database,oauth2


router=APIRouter(
    #  prefix='/login',
    tags=['authentication']
)

# @router.post('/login',response_model=schemas.Token)
# def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
#     '''{
#         "username":"ada"`
#         "password":adwa
#         }
#         '''
#     user=db.query(models.User).filter(models.User.email==user_credentials.username).first()
#     #in the password request form it only returns username and password so we have to check the email against the username
#     #since we dont have usernames setup we check against email
    
#     if not user:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
#     # verified=utils.verify(user_credentials.password, user.password)
#     if not utils.verify(user_credentials.password, user.password):
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
#     #create a token
#    #...
#     access_token=oauth2.create_access_token(data={"user_id":user.id})
#    #return token
#     return {"token": access_token,"tokentype":"bearer"} 

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    # return token

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}