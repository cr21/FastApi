from . import models
from .database import engine
from fastapi import FastAPI
# Database connection
from .config import settings
from .routers import post, user, auth, vote

# create automatic database table
# models.Base.metadata.create_all(bind=engine)



app = FastAPI(title="Social Media Fast API")
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root_route():
    return {"message":"  1.Hello world pushing to ubuntu and heroku restart fastapi service added"}
# title: str, content : str
# uvicorn app.main:app --reload