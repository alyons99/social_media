from fastapi import FastAPI

app = FastAPI()

#the decorator turns this function into a path/route operation (get HTTP method)
@app.get("/")
def root():

    return {"message": "Hello World! I love FASTAPI!"}

@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}