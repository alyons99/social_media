from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from .database import create_db_and_tables, get_session
from .models import Post, PostCreate, PostRead, PostUpdate

app = FastAPI(title="Social Media Posts API")

@app.on_event("startup")
async def on_startup():
    """Create database tables on startup"""
    create_db_and_tables()

@app.post("/posts/", response_model=PostRead)
def create_post(post: PostCreate, session: Session = Depends(get_session)):
    """Create a new post"""
    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@app.get("/posts/", response_model=List[PostRead])
def read_posts(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """Get all posts with pagination"""
    statement = select(Post).offset(skip).limit(limit)
    posts = session.exec(statement).all()
    return posts

@app.get("/posts/{post_id}", response_model=PostRead)
def read_post(post_id: int, session: Session = Depends(get_session)):
    """Get a specific post by ID"""
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.put("/posts/{post_id}", response_model=PostRead)
def update_post(post_id: int, post_update: PostUpdate, session: Session = Depends(get_session)):
    """Update a specific post"""
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post_data = post_update.model_dump(exclude_unset=True)
    for key, value in post_data.items():
        setattr(db_post, key, value)
    
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, session: Session = Depends(get_session)):
    """Delete a specific post"""
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    session.delete(post)
    session.commit()
    return {"message": "Post deleted successfully"}

@app.get("/")
def root():
    """Root endpoint"""
    return {"message": "Social Media Posts API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)