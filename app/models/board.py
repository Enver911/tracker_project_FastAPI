from backend.db import Base
from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.orm import relationship

class Board(Base):
    __tablename__ = "board" 
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), default="No name")
    description = Column(Text, nullable=True)
    avatar = Column(String, nullable=True)
    background = Column(String(100), nullable=True)
    columns = relationship("Column", back_populates="board")
    
    def set(self, model_dump):
        for key, value in model_dump.items():
            setattr(self, key, value)
    
    
