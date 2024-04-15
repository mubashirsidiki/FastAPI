from fastapi import FastAPI, Response, status, HTTPException, Depends , APIRouter
import sys
sys.path.append(r'C:\Users\rocky\Desktop\Stuff 2.0\Learning\Python API Development\FastAPI')
from app import models , schemas , oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# Route to retrieve all posts
@router.get("/" , response_model=List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts

# Route to retrieve a single post by its ID
@router.get("/{post_id}" , response_model=schemas.PostResponse)
def get_single_post(post_id: int, db: Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {post_id} was not found")
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="not authorized tp perform requested action")
    
    return post

# Route to create a new post
@router.post("/createpost", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):

    print(current_user.email)
    post_to_create = models.Post(owner_id = current_user.id , **new_post.dict())
    db.add(post_to_create)
    db.commit()
    db.refresh(post_to_create)
    return post_to_create

# Route to delete a post by its ID
@router.delete("/deletepost/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {post_id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="not authorized tp perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Route to update a post by its ID
@router.put("/updatepost/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):
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

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="not authorized tp perform requested action")

    post_query.update(updated_post.model_dump() , synchronize_session=False)

    db.commit()
    db.refresh(post)

    return post