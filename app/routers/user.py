from fastapi import APIRouter
from ..  import database, schemas, models
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session 
from ..hashing import Hash


router = APIRouter(
    prefix = "/user",
    tags = ['users']
)

get_db = database.get_db

@router.post('/', response_model = schemas.ShowUser)
def create_user(blog: schemas.User, db: Session = Depends(get_db)):
    #hashedpassword = pwd_ctx.hash(blog.password)
    new_user = models.User(name=blog.name, email=blog.email, password=Hash.bcrypt(blog.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model = schemas.ShowUser)
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f'User with id: {id} is not available.')
    return user