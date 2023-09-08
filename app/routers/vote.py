from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models,oauth2,database

router=APIRouter(
    prefix="/vote",
    tags=["Votes"]
)

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def vote(vote: schemas.Votes, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    #checks to see if post exists
    post_query=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with id {vote.post_id} DNE")
    #checks if submitting on vote on existing vote
    vote_query=db.query(models.Votes).filter(models.Votes.post_id == vote.post_id,models.Votes.user_id == current_user.id)
    found_vote=vote_query.first()
    if(vote.like_dislike == True):#likes post
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} already voted on post{vote.post_id}")
        new_vote=models.Votes(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return{"added:":"vote"}
    else:#dislike post aka remove vote
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="removed vote")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"bro":"deleted vote aka disliked post"}