from typing import Optional
from fastapi import FastAPI
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

#the decorator turns this function into a path/route operation (get HTTP method)
#extract data from the body of the payload.
@app.post("/posts")
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
    print(post)
    return {"post_detail": post}

#update post by id
#put needs all fields, patch just needs the field that gets updated.
@app.put("/posts/{id}")
def update_posts():
    pass

#delete post by id
@app.delete("/posts/{id}")
def delete_posts():
    pass