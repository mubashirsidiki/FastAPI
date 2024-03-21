from fastapi import FastAPI, Depends
import models
from database import engine , get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status" : "success"}
