from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
# from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

#defining a post class. Exteneding BaseModel from pydantic, we are assigning they rules for post contents
#this is our schema
class Post(BaseModel):
    title: str
    content: str
    #setting a default value
    published: bool = True
    #this is an optional field. If the post request doesnt include a rating, it will not send one. Will throw an error is the value isnt an int.
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content" : "I like pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


#the decorator turns this function into a path/route operation (get HTTP method)
#extract data from the body of the payload.
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    #will convert the pydantic class into a dictionary 
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0,9999999)
    my_posts.append(post_dict)
    return {"dada": post_dict}
    

#get info about all posts
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

#get post by id (path parameter)
@app.get("/posts/{id}")
#this adds data validation and converts the string ID into an int so it can be compared properly in the find_post func
def get_post(id: int):
    post = find_post(id)
    #add a check for if the id was found.
    if not post:
        #if not, set status code to 404 (otherwise it will be 200 but return null)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Error 404: Post with id {id} was not found.")
    return {"post_detail": post}

#update post by id
#put needs all fields, patch just needs the field that gets updated.
@app.put("/posts/{id}")
def update_post():
    pass

#delete post by id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found.")
    my_posts.pop(index)
    #no data will be sent back because post was deleted.
    return Response(status_code=status.HTTP_204_NO_CONTENT)