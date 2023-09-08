from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models,utils


router=APIRouter(
    prefix="/users",
    tags=["users"]
    ) #router object
'''
NEW ACCOUNT CREATION
'''
@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.CreateUser, db:Session= Depends(get_db)):
    #hash the password-user.password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

'''
Retreiving User's Info 
'''
@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id:int,db:Session = Depends(get_db)):
    person=db.query(models.User).filter(models.User.id == id).first()
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id :{id} DNE")
    return person
