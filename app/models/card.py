from backend.db import Base
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from schemas.card import CardSchemaRead

class Card(Base):
    __tablename__ = "card" 
    
    id = Column(Integer, primary_key=True)
    column_id = Column(Integer, ForeignKey("column.id"))
    
    title = Column(String(100), default="No name")
    description = Column(Text(1000), nullable=True)
    avatar = Column(String(100), nullable=True)
    background = Column(String(100), nullable=True)
    created = Column(DateTime, default=datetime.now())
    updated = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    deadline = Column(DateTime, nullable=True)
    
    column = relationship("Column", back_populates="cards")
    
    linked_schema = CardSchemaRead
    
