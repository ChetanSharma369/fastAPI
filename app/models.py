from .databases import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'details'

    id=Column(Integer, primary_key=True, nullable=False)
    title=Column(String, nullable=False) #name
    content=Column(String,nullable=False) #city
    published=Column(Boolean, server_default='FALSE',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    phone_number=Column(String)

    owner=relationship("Users")

class Users(Base):
    __tablename__ ='users'

    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__='votes'
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id=Column(Integer,ForeignKey("details.id",ondelete="CASCADE"),primary_key=True)


