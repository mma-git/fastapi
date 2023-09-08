from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func 
from ..database import get_db
from .. import schemas,models,oauth2
from typing import List, Optional



router=APIRouter(
    prefix="/posts",
    tags=["posts"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}},
)
'''

CRUD OPERATIONS 

'''
#USING ORM instead of direct SQL
#testing query
'''
option to return only all of your posts
added the query parameter ?etc. (?limit=4)
%20 means space in url
'''
@router.get('/',response_model=List[schemas.PostOut]) #decorator
def test_posts(db: Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),
               limit:int = 10,skip:int=0,search:Optional[str]=""):
    #when using sqlalc, pass as parameter
    #a dependency is used, makes a session for every request to the database
    #the models represent the tables
    # posts=db.query(models.Post).filter(models.Post.account_id==current_user.id).all()
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(limit)
    results=db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes,models.Votes.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    return results
'''

CREATE 
    #print(**post.dict())
    #** unpacks dictionary into similar format
    #title=post.title,content=post.content,published=post.published
    adding dependecy on oauth2 get user requires the post route to only work when logged in
'''
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post: schemas.CreatePost, db : Session=Depends(get_db), current_user: int=Depends(oauth2.get_current_user)):
    
    print(current_user.id)
    new_post=models.Post(account_id=current_user.id, **post.dict())
    #remember to always committ when submitting changes
    db.add(new_post)
    db.commit()
    db.refresh(new_post)#retrieves new post made and stores it into new_post
    return new_post
'''

GET ONE

'''
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int, db: Session=Depends(get_db),current_user_id:int=Depends(oauth2.get_current_user)): #fastapi verifies to int
    # fetch_one=db.query(models.Post).filter(models.Post.id==(id)).first()
    fetch_one=db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(
        models.Votes,models.Votes.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    # print(fetch_one)
    if not fetch_one:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'post with id {id} not found')
    return fetch_one
'''

DELETE 

'''
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    
    post_query=db.query(models.Post).filter(models.Post.id==(id))#query to find a post
    post=post_query.first() #checks if post is there
    
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'post with id {id} not found') 
    #my_posts.pop(deleted_post)
    if post.account_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f'Not Authorized, wrong user not the owner')
    post_query.delete(synchronize_session=False)
    db.commit()
    #db.refresh(deleted_post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
'''
UPDATE 

'''
@router.put('/{id}',status_code=status.HTTP_200_OK,response_model=schemas.PostResponse)
def update_post(id: int, updated_post:schemas.UpdatePost, db: Session= Depends(get_db),current_user:int=Depends(oauth2.get_current_user) ):

    post_query = db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'post with id {id} not found') 
    if post.account_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f'Not Authorized, wrong user not the owner')
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return  post_query.first()

