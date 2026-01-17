from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

class CreateUser(BaseModel):
    email:EmailStr
    password:str

class ShowUser(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime

    model_config = {"from_attributes":True}


class LoginUser(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    acess_token:str
    token_type:str

class TokenData(BaseModel):
    email:Optional[str] = None


class Details(BaseModel):
    id:int
    title:str
    content:str
    published:bool= False

class DetailsResponse(Details):
    created_at:datetime
    owner_id:int
    owner: ShowUser
    
    model_config = {"from_attributes":True}

class PostVote(BaseModel):
    Post: DetailsResponse
    votes:int

    model_config = {"from_attributes":True}

class Vote(BaseModel):
    post_id:int
    dir: conint(le=1)


