from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session 

router = APIRouter(
    prefix = "/blogs",
    tags = ['blogs']
)

get_db = database.get_db

@router.get('/', response_model = List[schemas.ShowBlog])
def get_blog(db: Session = Depends(get_db), current_user:schemas.User = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs

# POST endpoint to create a new blog post
@router.post("/", status_code = 201)
def create_blog(blog: schemas.BlogCreate, db: Session = Depends(get_db), current_user:schemas.User = Depends(oauth2.get_current_user)):
    new_blog = models.Blog(title=blog.title, content=blog.content, user_id = 1)
    db.add(new_blog)
    db.commit()  # Save the new blog post in the database
    db.refresh(new_blog)  # Reload the data to get the new `id` of the blog post
    return new_blog

@router.delete('/{id}', status_code = 204)
def delete_blog(id, db: Session = Depends(get_db), current_user:schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Blog with id:{id} not found.')
    blog.delete(synchronize_session = False)
    db.commit()
    return 'Done'

@router.put('/{id}', status_code = status.HTTP_202_ACCEPTED)
def update_blogs(id, blog: schemas.BlogCreate, db:Session = Depends(get_db), current_user:schemas.User = Depends(oauth2.get_current_user)):
    blog1 = db.query(models.Blog).filter(models.Blog.id ==  id)
    if not blog1.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Blog with id:{id} not found.')
    blog1.update(blog.dict(exclude_unset = True))
    db.commit()
    return 'Updated successfully'

# @app.get('/blogs', response_model = List[schemas.ShowBlog], tags = ['blogs'])
# def get_blog(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs

@router.get('/{id}', status_code= 200, response_model = schemas.ShowBlog)
def show(id, db: Session = Depends(get_db), current_user:schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
       raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'Blog with id: {id} is not available.')
    return blog