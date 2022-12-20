
from ..utils import hash
from fastapi import  status,HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import  models,schemas, oauth2, database


router = APIRouter(
                prefix='/vote',
                tags=["Vote"]
                )

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db:Session = Depends(database.get_db), current_user:int=Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    
    # if post does not exists with post id raise 404 
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User and Post combination is incorrect does not exists")
    
    # check if userid, post id combination in vote table
    # if not raise exception
    # else follow instructions
    vote_query = db.query(models.Vote).\
                filter(models.Vote.post_id == vote.post_id,
                        models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()
    # if we are liking post 
    if vote.dir == 1:
        # if user has not already liked this post like it
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User has already liked this post")
        else:
            # user has not voted for this post
            # create new vote
            new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message": "Vote successfully added"}
    
    else:
        # if we are removing like from the post
        # if vote does not exists raise 404 not found
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found User has never liked it, so you can not remove like")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"deleted successfully"}

     
    
