from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Post(SQLModel, table=True):
    """Post model for social media app"""
    __tablename__ = "posts"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(default=True)
    date_created: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class PostCreate(SQLModel):
    """Schema for creating a post"""
    title: str
    content: str
    published: Optional[bool] = True

class PostRead(SQLModel):
    """Schema for reading a post"""
    id: int
    title: str
    content: str
    published: bool
    #date_created: datetime

class PostUpdate(SQLModel):
    """Schema for updating a post"""
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None