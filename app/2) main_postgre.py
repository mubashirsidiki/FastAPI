from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

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
def get_all_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {'data': posts}

# Route to retrieve a single post by its ID
@app.get("/posts/{id}")
def get_single_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} was not found")
    return {'post_detail': post}

# Route to create a new post
@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    connection.commit()
    return {'post_created': new_post}

# Route to delete a post by its ID
@app.delete("/deletepost/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    deleted_post = cursor.fetchone()
    connection.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} was not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Route to update a post by its ID
@app.put("/updatepost/{id}")
def update_post(id: int, updated_post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (updated_post.title, updated_post.content, updated_post.published, id))
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} was not found")
    connection.commit()
    return {"post_updated" : updated_post}
