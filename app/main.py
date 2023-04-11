from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import expovariate, randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from . routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# database connection
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='root', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection established!')
        break
    except Exception as error:
        print('Error connecting to database')
        print('Error connecting was', error)
        time.sleep(2)

# Storing Posts
my_posts = [{"title":"title of post1", "content":"content of post1", "id": 1}, {"title":"title of post12", "content":"content of post2", "id": 2}]

# find post
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# Decorator 
@app.get("/")
def root():
    return {"message": "Welcome to the api"}

