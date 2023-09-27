from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    posts = relationship("Post")
