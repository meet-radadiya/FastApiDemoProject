from pydantic import BaseModel, EmailStr


class User(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Post(BaseModel):
    title: str
    content: str
    user_id: int


class PostView(BaseModel):
    title: str
    content: str
    user: User
