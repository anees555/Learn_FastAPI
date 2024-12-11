
from fastapi import FastAPI
from .routers import blog, user, authentication
from .database import engine
from . import models

app = FastAPI()

#Base.metadata.drop_all(bind=engine)

# Create tables in the database (if not already created)
models.Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)





    
    