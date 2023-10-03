from typing import List

import bcrypt
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

import models
from auth_bearer import JWTBearer
from auth_handler import signJWT
from database import SessionLocal
from schemas import Post, PostView, User, UserLogin

app = FastAPI(title="Blog site")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/user", dependencies=[Depends(JWTBearer())], tags=['user'])
def get_user(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user


@app.post("/user", tags=['user'])
def create_user(user: User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=user.name, email=user.email,
        password=bcrypt.hashpw(
            user.password.encode(
                'utf-8'
            ), bcrypt.gensalt()
        ).decode('utf-8')
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return signJWT(user.email)


@app.post("/user_login", tags=['user'])
def login_user(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=data.email)
    if user:
        if bcrypt.checkpw(
                data.password.encode("utf-8"),
                user[0].password.encode("utf-8")
        ):
            return signJWT(data.email)
        else:
            return {"error": "Wrong credentials."}
    else:
        return {"error": "Please sign up."}


@app.get("/posts", response_model=List[PostView], tags=['post'])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).join(models.User).all()
    return posts


@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=['post'])
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


@app.patch("/posts/{id}", dependencies=[Depends(JWTBearer())], tags=['post'])
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    existing_post = db.query(models.Post).filter_by(id=id).first()
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    existing_post.title = post.title
    existing_post.content = post.content
    db.commit()
    db.refresh(existing_post)
    return existing_post


@app.delete("/posts/{id}", dependencies=[Depends(JWTBearer())], tags=['post'])
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter_by(id=id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}
