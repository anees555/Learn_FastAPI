from pydantic import BaseModel
from typing import List, Optional

class  BlogCreate(BaseModel):
    title:str
    content:str



class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str
    class Config():
        from_attributes = True

class ShowBlog(BaseModel):
    title:str
    content:str

    creator: ShowUser
    class Config():
        from_attributes = True

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    email:Optional[str] = None