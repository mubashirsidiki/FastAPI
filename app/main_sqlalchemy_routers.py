from fastapi import FastAPI, Response, status, HTTPException, Depends
from database import engine, get_db
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import schemas
import models
import utils
from routers import post , user , auth

# Create database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# Route to root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the root endpoint!"}

