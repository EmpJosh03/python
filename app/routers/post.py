from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from .. database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# Getting posts
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), user_id: int =  Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return  posts

#Posts 
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    #extract data from body
    # post_dict = new_post.dict()
    # post_dict['id'] = randrange(0, 1000000)
    # my_posts.append(post_dict)
    
    # CREATING POST WITH SQL and DATABASE
    # cursor.execute("""INSERT INTO posts (title, name, age) VALUES (%s, %s, %s) RETURNING *""",(new_post.title, new_post.name, new_post.age))
    # post_added = cursor.fetchone()
    # conn.commit()
    
    # CREATING WITH SQL ALCHEMY
    print(current_user.email)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_Post(id: int, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),)) 
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} deleted")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title = %s, name = %s, age = %s WHERE id = %s RETURNING *""", (post.title, post.name, post.age, str(id),))
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist.")

    post_query.update(updated_post.dict(), synchronize_session=False) # type: ignore
    db.commit()
    
    return post_query.first()