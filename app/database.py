from sqlalchemy import create_engine
import sqlalchemy
from sqlalchemy.orm import sessionmaker , declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/fastapi"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base =  declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()