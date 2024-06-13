from backend.db import Base
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy import Column as Col
from sqlalchemy.orm import relationship

class Column(Base):
    __tablename__ = "column" 
    
    id = Col(Integer, primary_key=True)
    board_id = Col(Integer, ForeignKey("board.id"))
    title = Col(String(100), default="No name")
    board = relationship("Board", back_populates="columns")
    
    def set(self, model_dump):
        for key, value in model_dump.items():
            setattr(self, key, value)
    
    
