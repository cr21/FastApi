from . import models
from .database import engine
from fastapi import FastAPI
# Database connection
from .config import settings
from .routers import post, user, auth, vote

# models.Base.metadata.create_all(bind=engine)



app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



# title: str, content : str
# uvicorn app.main:app --reload