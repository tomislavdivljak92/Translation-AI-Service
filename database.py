import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker





#load environment variables from .env file



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL_FASTAPI")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


print("SQLALCHEMY_DATABASE_URL:", SQLALCHEMY_DATABASE_URL)
