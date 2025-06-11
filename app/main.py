from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
# from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

#defining a post class. Exteneding BaseModel from pydantic, we are assigning they rules for post contents
#this is our schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

def get_db():
    with psycopg.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        row_factory=dict_row
    ) as conn:
        yield conn


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
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: psycopg.Connection = Depends(get_db)):
    #will convert the pydantic class into a dictionary 
    with db.cursor() as cur:
        cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
        new_post = cur.fetchone()
        return{"data": new_post}

#get info about all posts
@app.get("/posts")
def get_posts(db: psycopg.Connection = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("""SELECT * FROM posts """)
        posts = cur.fetchall()
        print(posts)
        return {"posts": posts}

#get post by id (path parameter)
@app.get("/posts/{id}")
#this adds data validation and converts the string ID into an int
def get_post(id: int, db: psycopg.Connection = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("""SELECT * FROM posts WHERE id = %s """, (id,))
        post = cur.fetchone()
        print(post)
        #raise an error if not found
        if not post:
            raise HTTPException(status_code=404, detail="post not found")
        return {"post": post}

#update post by id
#put needs all fields, patch just needs the field that gets updated.
@app.put("/posts/{id}")
def update_post(id: int, post:Post, db: psycopg.Connection = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id))
        updated_post = cur.fetchone()

        if not updated_post:
            raise HTTPException(status_code=404, detail="post not found")
        return {"data": updated_post}
    

#delete post by id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: psycopg.Connection = Depends(get_db)):
    with db.cursor() as cur:
            cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
            deleted_post = cur.fetchone()

            #raise an error if not found
            if not deleted_post:
                raise HTTPException(status_code=404, detail="post not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)