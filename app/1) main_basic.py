from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

# Initialize FastAPI
app = FastAPI()

# Define data model for creating posts
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# Define data model for updating posts
class UpdatePost(BaseModel):
    title: str
    content: str

# Sample data
posts_database = [
    {'id': 1, 'title': 'title of post 1', 'content': 'content of post 1'},
    {'id': 2, 'title': 'fav foods', 'content': 'zinger burger'}
]

# Function to find a post by its ID
def find_post_by_id(post_id):
    for post in posts_database:
        if post['id'] == post_id:
            return post

# Route to root endpoint
@app.get("/")
def root():
    return {"message": "Hello World"}

# Route to retrieve all posts
@app.get("/posts")
def get_all_posts():
    return {'data': posts_database}

# Route to retrieve a single post by its ID
@app.get("/posts/{id}")
def get_single_post(id: int):
    post = find_post_by_id(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} was not found")
    return {'post_detail': post}

# Route to create a new post
@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    posts_database.append(post_dict)
    return {'post_created': post_dict}

# Function to find index of a post by its ID
def find_post_index(post_id):
    for index, post in enumerate(posts_database):
        if post['id'] == post_id:
            return index

# Route to delete a post by its ID
@app.delete("/deletepost/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} was not found")
    posts_database.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Route to update a post by its ID
@app.put("/updatepost/{id}")
def update_post(id: int, updated_post: UpdatePost):
    index = find_post_index(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} was not found")
    updated_post_dict = updated_post.dict()
    updated_post_dict['id'] = id
    posts_database[index] = updated_post_dict
    return {"data": updated_post_dict}
