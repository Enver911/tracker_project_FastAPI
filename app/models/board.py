from backend.db import Base
from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.orm import relationship

from schemas.board import BoardSchemaRead

class Board(Base):
    __tablename__ = "board" 
    
    id = Column(Integer, primary_key=True)
    
    title = Column(String(100), default="No name")
    description = Column(Text(1000), nullable=True)
    avatar = Column(String(100), nullable=True)
    background = Column(String(100), nullable=True)
    
    columns = relationship("Column", back_populates="board")
    
    linked_schema = BoardSchemaRead