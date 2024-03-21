from fastapi import Body, FastAPI, Response, status, HTTPException , Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import models
from database import engine , get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

# Define data model for creating posts
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Attempt to connect to the PostgreSQL database
try:
    connection = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='admin', cursor_factory=RealDictCursor)
    cursor = connection.cursor()
    print("Database Connection Was Successful")
except Exception as error:
    print("Connecting To Database Failed")
    print("Error", error)

# Route to root endpoint
@app.get("/")
def root():
    return {"message": "Hello World"}

# Route to retrieve all posts
@app.get("/posts")
def get_all_posts(db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {'data': posts}

# Route to retrieve a single post by its ID
@app.get("/posts/{id}")
def get_single_post(id: int , db: Session = Depends(get_db)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} was not found")
    return {'post_detail': post}

# Route to create a new post
@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post , db: Session = Depends(get_db)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # connection.commit()
    #print(post.model_dump())
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {'post_created': new_post}

# Route to delete a post by its ID
@app.delete("/deletepost/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int , db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    # deleted_post = cursor.fetchone()
    # connection.commit()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} was not found")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
 
# Route to update a post by its ID
@app.put("/updatepost/{id}")
def update_post(id: int, updated_post: Post , db: Session = Depends(get_db)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (updated_post.title, updated_post.content, updated_post.published, id))
    # updated_post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} was not found")
    
    post_query.update(updated_post.model_dump() , synchronize_session=False)
    db.commit()
    return {"post_updated" : updated_post}
