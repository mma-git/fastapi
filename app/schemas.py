from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
# Post class utilizes pydantic library to set a schema/format for data to be sent.
# Definig our schema: title=str, content=str, category, etc.
# here we have the required fields needed for a post
#pydantic works with dictionaries
#Sets format to follow


'''
USER ACCOUNT PORTION
'''
class CreateUser(BaseModel):
    email: EmailStr #ensures valid email is given
    password:str 
    #username:str
class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    class config():
        orm_mode=True
        
# class GetUser(UserOut):
#     pass

class UserLogin(BaseModel):
    email:EmailStr
    password:str
  
'''
DEFINING REQUESTS
'''
class Post(BaseModel):
    title: str #will try to force input to str value
    content: str
    published: bool = True #defaulted to true
    #rating: Optional[int] = None #optional field that defaults to a value of none

class PostBase(BaseModel):
    title: str 
    content: str
    published: bool = True
    
class PostOut(BaseModel):
    Post: Post
    votes:int
    
'''
POST RESPONSE PORTION
things we want to send back to the user after request is made
can specify what data to be sent back to user
'''

class PostResponse(PostBase):
    #inherits fields from PostBase
    id:int
    created_at:datetime
    account_id:int
    owner:UserOut
    class config():
        orm_mode=True   
'''
The PostCreate class not inherits the properties of the PostBase class

'''    
class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass


# '''
# POST RESPONSE PORTION
# things we want to send back to the user after request is made
# can specify what data to be sent back to user
# '''

# class PostResponse(PostBase):
#     #inherits fields from PostBase
#     id:int
#     created_at:datetime
    
#     class config():
#         orm_mode=True
        
  
'''
ACCESS TOKEN
'''
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None #changed from opt str to optional int 
    
'''
VOTING
can typecast to bool, want value to be either 0 or 1
can also typcase to conint(ge=0,le=1)//conint is from pydantic 
'''

class Votes(BaseModel):
    post_id:int
    like_dislike:bool