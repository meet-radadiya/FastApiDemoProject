from typing import List

from pydantic import BaseModel


class User(BaseModel):
    name: str
    tags: set[str] = set()


class Post(BaseModel):
    title: str
    content: str
    user_id: int
    tags: set[str] = set()


class PostView(BaseModel):
    title: str
    content: str
    user: User
    tags: set[str] = set()
