from fastapi import FastAPI, HTTPException, status, Depends, Response
from .schemas import Details,DetailsResponse,CreateUser
import time
from . import models, schemas, config
from .databases import engine, get_db
from sqlalchemy.orm import Session
from .routers import register, users, vote


models.Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
import psycopg2
from psycopg2.extras import RealDictCursor


origins = ["https://www.google.com","https://www.youtube.com/"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
###Using raw sql

#creating data base
db_prams={
    'host':'localhost',
    'database':'fastapi',
    'user':'postgres',
    'password':'root123',
    'port':'5432'
}
#connecting database
try:
    conn=psycopg2.connect(**db_prams,cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("connection sucessful")
except Exception as error:
    print("failed")
    print(error)
    time.sleep(3)



app.include_router(users.router)
app.include_router(register.router)
app.include_router(vote.router)

#### USERS module for get post put delete CRUD operations through raw sql
@app.get("/")
def get():
    return {"msg":"hello world"}

#POST
@app.post("/users/",status_code=status.HTTP_201_CREATED)
def get_items(detail : schemas.Details):
    cursor.execute("""INSERT INTO user_details (name,city) VALUES (%s,%s) RETURNING *""",(detail.name,detail.city))
    new_post = cursor.fetchone()
    conn.commit()
    return {"posted data":new_post}

#GET
@app.get("/users/")
def get():
    cursor.execute("""SELECT * FROM user_details""")
    posts = cursor.fetchall()
    return {"data":posts}

@app.get("/users/{id}")
def get(id):
    cursor.execute("""SELECT * FROM user_details WHERE id =(%s);""",(id))
    retrived_data= cursor.fetchone()
    if retrived_data is None:
        return {"msg":"id not found"}
    return retrived_data
    
#DELETE   
@app.delete("/users/{id}",status_code=203)
def delete(id:int):
    cursor.execute("""DELETE FROM user_details WHERE id = %s returning * ;""",(str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="user id not found")
    return {"deleted user":deleted_post}

#PUT
@app.put("/users/{id}",status_code=status.HTTP_202_ACCEPTED)
def put(id:int, detail:schemas.Details):
    cursor.execute("""UPDATE user_details SET name=%s,city=%s,published=%s WHERE id=%s returning *""",(detail.name,detail.city,detail.published,id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="user id not found")
    return {"details":updated_post}

