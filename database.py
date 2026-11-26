from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Base = declarative_base()


def get_db():
    with Session(engine) as db:
        yield db