from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

# This file if for pydantic models which manages the input output data restrictions
# the class will specify what type of input we need --> See create_post()
# same schema can be used in update requests as well
    
class PostBase(BaseModel):
    title: str # set to validate or convert user input to str
    content: str 
    published: bool = True # if user don't provide value default value is True optional schema

   # rating: Optional[int] = None # fully optional field if not provided it is None, it also check the type
    
# inherit others from PostBase
# request model
class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # # To fix orm model issues??? 
    class Config:
        from_attributes = True

# response model
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut # to get user information

    # # To fix orm model issues??? 
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str

# to assess login tokens
class Token(BaseModel):
    access_token: str
    token_type: str

# token output
class TokenData(BaseModel):
    # id: Optional[str] = None
    id: int

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore
