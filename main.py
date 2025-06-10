from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

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

#the decorator turns this function into a path/route operation (get HTTP method)
@app.get("/")
def root():

    return {"message": "Hello World! I love FASTAPI!"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts."}

#extract data from the body of the payload. Tested using Postman.
@app.post("/posts")
def create_posts(new_post: Post):
    #each post should have title and content as str. Could add other stuff like Bool for draft, type, etc.
    print(f"Value: {new_post.rating}")
    #will convert the pydantic class into a dictionary 
    print(new_post.model_dump())
    return{"data": new_post}
    # return{"new_post": f"Title: {new_post.title}. Content: {new_post.content}. Published: {new_post.published}. Rating: {new_post.rating}"}