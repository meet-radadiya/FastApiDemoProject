from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

import models
from database import SessionLocal
from schemas import Post, User, PostView

app = FastAPI(title="Blog site")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/user", tags=['user'])
def get_user(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user


@app.post("/user", tags=['user'])
def create_user(user: User, db: Session = Depends(get_db)):
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return user


@app.get("/posts", response_model=List[PostView], tags=['post'])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).join(models.User).all()
    return posts


@app.post("/posts", tags=['post'])
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return post


@app.get("/posts/{id}", response_model=PostView, tags=['post'])
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).join(models.User).filter_by(id=id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.patch("/posts/{id}", tags=['post'])
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    existing_post = db.query(models.Post).filter_by(id=id).first()
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    existing_post.title = post.title
    existing_post.content = post.content
    db.commit()
    db.refresh(existing_post)
    return existing_post


@app.delete("/posts/{id}", tags=['post'])
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter_by(id=id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    db.refresh(post)
    return {"message": "Post deleted"}
