from fastapi import FastAPI, Response, status, HTTPException, Depends
from database import engine, get_db
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import schemas
import models
import utils

# Create database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

# Route to root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the root endpoint!"}

# Route to retrieve all posts
@app.get("/posts" , response_model=List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# Route to retrieve a single post by its ID
@app.get("/posts/{post_id}" , response_model=schemas.PostResponse)
def get_single_post(post_id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {post_id} was not found")
    
    return post

# Route to create a new post
@app.post("/createpost", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_to_create = models.Post(**new_post.dict())
    db.add(post_to_create)
    db.commit()
    db.refresh(post_to_create)
    return post_to_create

# Route to delete a post by its ID
@app.delete("/deletepost/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {post_id} was not found")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Route to update a post by its ID
@app.put("/updatepost/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {post_id} was not found")
    
    # # Update post attributes
    # post.title = updated_post.title
    # post.content = updated_post.content
    # post.published = updated_post.published
    # post.created_at = datetime.now()

    post_query.update(updated_post.model_dump() , synchronize_session=False)

    db.commit()
    db.refresh(post)

    return post


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    user_db_query = db.query(models.User).filter(models.User.email == user.email)
    user_db = user_db_query.first()

    if user_db:
        raise HTTPException(status_code=status.HTTP_306_RESERVED,
                            detail=f"User with id: '{user.email}' already exist")

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get('/users/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user_db_query = db.query(models.User).filter(models.User.id == id)
    user_db = user_db_query.first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user_db