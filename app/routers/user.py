
from fastapi import FastAPI, status, HTTPException, Response, APIRouter, Depends
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

# All users end points

router=APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password


    # cursor.execute("""INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *""", 
    #                (user.email, user.password))
    # new_user = cursor.fetchone()

    # # we need to commit to change into db
    # conn.commit()

    # keep password safe
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit() 
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""SELECT * FROM users WHERE id = {}""".format(str(id)))              
    # user = cursor.fetchone()

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user


