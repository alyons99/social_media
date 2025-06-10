from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

#the decorator turns this function into a path/route operation (get HTTP method)
@app.get("/")
def root():

    return {"message": "Hello World! I love FASTAPI!"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts."}

#extract data from the body of the payload. Tested using Postman.
@app.post("/posts")
def create_posts(body: dict = Body(...)):
    print(body)