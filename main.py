from fastapi import Body, FastAPI , Response , status , HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published: bool = True
    rating: Optional[int] = None

class UpdatePost(BaseModel):
    title : str
    content : str


my_posts = [{'id' : 1 ,\
             'title' : 'title of post 1',\
             'content' : 'content of post 1'},\
            {'id' : 2 ,\
             'title' : 'fav foods',\
             'content' : 'zinger burger'}]

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == int(id):
#             return p

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_all_post():
    return {'data' : my_posts}

@app.get("/posts/{id}")
def get_single_post(id : int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id: {id} was not found")
        # #response.status_code = 404
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message' : f"post with id: {id} was not found"}

    return {'post_detail' : post}

@app.post("/createposts" , status_code=status.HTTP_201_CREATED)
def create_posts(post : Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {'post_created' : post_dict} 


def find_index_post(id):
    for i , p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.delete("/deletepost/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with id: {id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/updatepost/{id}")
def update_post(id : int , updated_post : UpdatePost):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,\
                             detail=f"post with id: {id} was not found")
    updated_post_dict = updated_post.model_dump()
    updated_post_dict['id'] = id
    my_posts[index] = updated_post_dict
    return {"data" : updated_post_dict}