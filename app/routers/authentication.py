from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, database, models, JWTtoken
from ..hashing import Hash
from sqlalchemy.orm import Session
from ..schemas import Token


router = APIRouter(
    tags = ['Authentication']
)

@router.post('/login')
def login(blog:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == blog.username).first()
    if  not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Invalid Credential")

    if not Hash.verify(user.password, blog.password):
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Incorrect Password")
    
    access_token = JWTtoken.create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")

