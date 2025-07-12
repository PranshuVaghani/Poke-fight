# Establishes a connection b/w the database.
# For management of the server only.

from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL = "postgresql://postgres:Pranshu%402431@localhost:5432/pokemon"

engine = create_engine(URL)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()