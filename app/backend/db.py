from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.orm.collections import InstrumentedList
from pydantic import BaseModel

engine = create_engine("sqlite:///tracker.db")
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    linked_schema = BaseModel
    
    def set(self, model_dump):
        for key, value in model_dump.items():
            setattr(self, key, value)
            
    def to_schema(self):
        data = {}
        
        for key in self.linked_schema.model_fields:
            value = getattr(self, key) # orm model value
            if issubclass(type(value), InstrumentedList): # one to many nested object
                data[key] = [orm_obj.to_schema() for orm_obj in value] # recursion for nested orm objects
            elif issubclass(type(value), Base): # one to one nested object
                data[key] = value.to_schema()
            else: # simple fields
                data[key] = value
            
        return self.linked_schema(**data)
        
