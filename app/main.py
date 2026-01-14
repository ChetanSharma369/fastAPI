from fastapi import FastAPI, HTTPException, status, Depends
import json
from pydantic import BaseModel
import time
from . import models
from .databases import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

myposts=[{'id':1,'name':'your name','city':'your city','age':12},{'id':2,'name':'chetan','city':'bhubaneshwar','age':23}]


app = FastAPI()
import psycopg2
from psycopg2.extras import RealDictCursor




#Defining the model
class Details(BaseModel):
    name:str
    city:str
    published:bool= False


#creating data base
db_prams={
    'host':'localhost',
    'database':'fastapi',
    'user':'postgres',
    'password':'root123',
    'port':'5432'
}

try:
    conn=psycopg2.connect(**db_prams,cursor_factory=RealDictCursor)
    cursor=conn.cursor()
    print("connection sucessful")
except Exception as error:
    print("failed")
    print(error)
    time.sleep(3)






def find_post(id):
    for i in myposts:
        if i['id'] == id:
            return i
    return None

def find_post_index(id):
    for i,p in enumerate(myposts):
        if p['id'] == id:
            return i
    return None


@app.get("/sqlalchemy")
def root(db: Session = Depends(get_db)):
    msg={
        'name':'chetan',
        'roll':22054279,
        'age':23,
        'city':'bhubaneshwar'
    }
    json_msg=json.dumps(msg)
    return json_msg


#### USERS module for get post put delete

#POST
@app.post("/users/",status_code=status.HTTP_201_CREATED)
def get_items(detail : Details):
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

print(myposts)
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
def put(id:int, detail:Details):
    cursor.execute("""UPDATE user_details SET name=%s,city=%s,published=%s WHERE id=%s returning *""",(detail.name,detail.city,detail.published,id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="user id not found")
    return {"details":updated_post}

    




