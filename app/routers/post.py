
from fastapi import  status, HTTPException, Response, APIRouter, Depends
from typing import Optional, List
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db

# All post end points

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# , response_model=List[schemas.Post]
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user),
              limit: int = 10, skip: int= 0, search: Optional[str] = ""): 

    # Get data from DB by sql code
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # Get data from DB by slqalchemy models - only current user's posts
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # limit the number of posts with limit parameter
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, 
                       func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
                                                                            models.Vote.post_id == models.Post.id, 
                                                                            isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
 
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
  
    # not a good practice
    # cursor.execute(f"""INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content}, {post.published})""")
    
    # # db connection thru sql code.
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # # we need to commit to change into db
    # conn.commit()

    # this is to insert value into the fields in db
    # **post.model_dump() # unpack all fields in the post db so instead of putting all of them into models we can unpack fields

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post) # to add new post into db
    db.commit() # to commit changes into db
    db.refresh(new_post) # to refresh db for new post

    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db:Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    
    # # db connection thru sql code.
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    # post = find_post(id)

    # DB connection with sql alchemy
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, 
                       func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
                                                                            models.Vote.post_id == models.Post.id, 
                                                                            isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    # to check if post is exist
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    
    # # check the user's id matches with the post
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    #                         detail="Not authorized to perform")

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    #  # db connection thru sql code.
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    # index = find_index_post(id)

    # sqlalchemy db connection
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # Check whether the post is exist
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    # to check whether the owner performs the operation 
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, update_post: schemas.PostCreate,
                db:Session = Depends(get_db), 
                current_user: int= Depends(oauth2.get_current_user)):

    # # db connection thru sql code.
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
    #                (post.title,post.content,post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

   
    # sqlalchemy db connection
    post_query = db.query(models.Post).filter(models.Post.id == id) # Save query not runnig now
    post = post_query.first() # grab the the post if it is exist

    # Check whether the post is exist
    if post == None: # if the post is not exist
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    # to check whether the owner performs the operation 
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform")

    post_query.update(update_post.model_dump(), synchronize_session=False) # if the post is exist

    db.commit()

    return post_query.first()