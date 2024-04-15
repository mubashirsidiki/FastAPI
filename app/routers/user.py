from fastapi import FastAPI, Response, status, HTTPException, Depends , APIRouter
from app import models , schemas , utils
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    user_db_query = db.query(models.User).filter(models.User.email == user.email)
    user_db = user_db_query.first()

    if user_db:
        raise HTTPException(status_code=status.HTTP_306_RESERVED,
                            detail=f"User with id: '{user.email}' already exist")

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user_db_query = db.query(models.User).filter(models.User.id == id)
    user_db = user_db_query.first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user_db