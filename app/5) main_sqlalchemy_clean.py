from fastapi import FastAPI, Response, status, HTTPException, Depends
from database import engine, get_db
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import schemas
import models

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
