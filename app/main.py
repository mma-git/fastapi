from fastapi import FastAPI
from pydantic import BaseModel
from . import models
from .database import engine
from .routers import posts,user,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
# models.Base.metadata.create_all(bind=engine)
#tells sqlalchemy to run create sequence, not needed with alembic 
app = FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency, session object is responsible for talking to DB

#saves posts

# Post class utilizes pydantic library to set a schema/format for data to be sent.
# Definig our schema: title=str, content=str, category, etc.
class Post(BaseModel):
    title: str #will try to force input to str value
    content: str
    published: bool = True #defaulted to true
    #rating: Optional[int] = None #optional field that defaults to a value of none


app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# '''
# CRUD OPERATIONS 

# '''
# #USING ORM instead of direct SQL
# #testing query
# @app.get('/posts',response_model=List[schemas.PostResponse]) #decorator
# def test_posts(db: Session=Depends(get_db)):
#     #when using sqlalc, pass as parameter
#     #a dependency is used, makes a session for every request to the database
#     #the models represent the tables
#     posts=db.query(models.Post).all()
#     return posts
# '''

# CREATE 
#     #print(**post.dict())
#     #** unpacks dictionary into similar format
#     #title=post.title,content=post.content,published=post.published
# '''
# @app.post("/posts", status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
# def create_posts(post: schemas.CreatePost, db : Session=Depends(get_db)):
    
#     new_post=models.Post(**post.dict())
#     #remember to always committ when submitting changes
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)#retrieves new post made and stores it into new_post
#     return new_post
# '''

# GET ONE

# '''
# @app.get("/posts/{id}",response_model=schemas.PostResponse)
# def get_post(id: int, db: Session=Depends(get_db)): #fastapi verifies to int
#     fetch_one=db.query(models.Post).filter(models.Post.id==(id)).first()
#     print(fetch_one)
#     if not fetch_one:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail=f'post with id {id} not found')
#     return fetch_one
# '''

# DELETE 

# '''
# @app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session=Depends(get_db)):
#     deleted_post=db.query(models.Post).filter(models.Post.id==(id))
#     if deleted_post.first()==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail=f'post with id {id} not found') 
#     #my_posts.pop(deleted_post)
#     deleted_post.delete(synchronize_session=False)
#     db.commit()
#     #db.refresh(deleted_post)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
# '''
# UPDATE 

# '''
# @app.put('/posts/{id}',status_code=status.HTTP_200_OK,response_model=schemas.PostResponse)
# def update_post(id: int, updated_post:schemas.UpdatePost, db: Session= Depends(get_db) ):

#     post_query = db.query(models.Post).filter(models.Post.id==id)
#     post=post_query.first()
#     if post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail=f'post with id {id} not found') 
    
#     post_query.update(updated_post.dict(), synchronize_session=False)
#     db.commit()
#     return  post_query.first()

# '''
# NEW ACCOUNT CREATION
# '''
# @app.post('/newusers',status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
# def create_user(user: schemas.CreateUser, db:Session= Depends(get_db)):
#     #hash the password-user.password
#     hashed_password=utils.hash(user.password)
#     user.password=hashed_password
#     new_user=models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# '''
# Retreiving User's Info 
# '''
# @app.get('/users/{id}',response_model=schemas.UserOut)
# def get_user(id:int,db:Session = Depends(get_db)):
#     person=db.query(models.User).filter(models.User.id == id).first()
#     if not person:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id :{id} DNE")
#     return person






# -----------------------------------------------------------------------------------------------------
'''Crud Operations'''

# @app.get("/") #decorator, turns into actual path operation so endpoint can be hit. get is http method
# def root():
#     return {"message": "yuhyuh"}


#first path operation that matches is the one that runs. order matters


# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts""")#sql statements
#     posts = cursor.fetchall()
#     print(posts)
#     return{"data":posts}

#get retrieves from api server, post sends data 

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post): #payload: dict = Body(...) extracts fields from body, sets it to dictionary, saves it to variable payload
#     # print(post)
#     # print(post.dict())
#     # post_dict = post.dict()
#     # post_dict['id'] = randrange(0,10000000)
#     # my_posts.append(post_dict)
#     cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
#                    (post.title,post.content,post.published))
#     new_post=cursor.fetchone()
#     #HAVE TO COMMIT CHANGES TO DATABASES
#     conn.commit()
#     return{"data": new_post}
#usually data in body is stored ina  database to be retrieved from, 


#singular post,#extracts through path parameter always returned as a string.

# @app.get("/posts/{id}")
# def get_post(id: int, response:Response): #fastapi verifies to int
#     cursor.execute("""SELECT * FROM posts WHERE id = (%s)""",(id,)) #might need , later
#     fetch_1post=cursor.fetchone()
#     #post = find_post(id)
#     if not fetch_1post:
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return{'message': f'post with id: {id} not found'}
#     # print(type(id))
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail=f'post with id {id} not found')
#     return{"post_detail":fetch_1post} 

# @app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     #find index in the array that has required ID
#     #my_posts.pop(index)
#     cursor.execute("""DELETE FROM posts WHERE id = (%s) RETURNING *""",(str(id)))
#     #index = find_postindex(id)
#     deleted_post=cursor.fetchone()
#     conn.commit()
#     if deleted_post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail=f'post with id {id} not found') 
#     #my_posts.pop(deleted_post)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
# @app.put('/posts/{id}',status_code=status.HTTP_426_UPGRADE_REQUIRED)
# def update_post(id: int, post:Post ):
#     cursor.execute("""UPDATE posts SET title = (%s), content = (%s), 
#                    published=(%s) WHERE id = (%s) RETURNING *""",
#                    (post.title, post.content, post.published,id))
#     updated_post=cursor.fetchone()
#     #index = find_postindex(id)
#     conn.commit()
#     if updated_post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                         detail=f'post with id {id} not found') 
#     # post_dict=post.dict() # converts to dictionary #
#     # post_dict['id']= id
#     # my_posts[index] = post_dict
#     return {'data': updated_post}
# -----------------------------------------------------------------------------------------------------
#testing query
# @app.get('/sqlalchemy')
# def test_posts(db: Session=Depends(get_db)):\
#     #when using sqlalc, pass as parameter
#     #a dependency is used, makes a session for every request to the database
#     #the models represent the tables
#     posts=db.query(models.Post).all()
#     return{"data":posts}