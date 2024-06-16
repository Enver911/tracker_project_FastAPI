from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pydantic import BaseModel

engine = create_engine("sqlite:///tracker.db")
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    linked_schema = BaseModel
    
    def set(self, model_dump):
        for key, value in model_dump.items():
            setattr(self, key, value)